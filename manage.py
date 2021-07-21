#!/usr/bin/env python
import csv
import sys
from contextlib import contextmanager
from pathlib import Path

import click
import logging
import requests

basedir = Path(__file__).resolve().parent

formatter = logging.Formatter('%(levelname)s - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@contextmanager
def csv_dump(filename, fieldnames):
    """
    Writes CSV headers to the given filename, and yields a ``csv.writer``.
    """
    f = (basedir / 'codelists' / filename).open('w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fieldnames)
    try:
        yield writer
    finally:
        f.close()


def hl7(codelist):
    data = requests.get(f'https://terminology.hl7.org/CodeSystem-v3-{codelist}.json').json()

    multi_value_properties = ('subsumedBy', 'synonymCode')
    properties = set()

    # Transform the list of dicts into a dict.
    for code in data['concept']:
        code['properties'] = {}
        for prop in multi_value_properties:
            code['properties'][prop] = set()
        for prop in code['property']:
            properties.add(prop['code'])
            name, value = prop.values()
            if name in multi_value_properties:
                code['properties'][name].add(value)
            elif name in code['properties']:
                raise Exception(f"{name} set to {code['properties'][name]}, not {value}")
            else:
                code['properties'][name] = value

    not_selectable = {code['code'] for code in data['concept'] if code['properties'].get('notSelectable')}
    logger.info('%s properties: %s', codelist, sorted(properties))

    codes = []
    for code in data['concept']:
        if (
            not code['properties'].get('notSelectable')
            and code['properties']['status'] == 'active'
            and any(parent in not_selectable for parent in code['properties']['subsumedBy'])
        ):
            codes.append(code)

    return codes, not_selectable


@click.group()
def cli():
    pass


@cli.command()
def update_container():
    """
    Update schema/codelists/container.csv from HL7.
    """
    # https://terminology.hl7.org/CodeSystem/medicationknowledge-package-type/
    data = requests.get('https://terminology.hl7.org/CodeSystem-medicationknowledge-package-type.json').json()

    with csv_dump('container.csv', ['Code', 'Title']) as writer:
        writer.writerows([[code['code'], code['display']] for code in data['concept']])


@cli.command()
def update_administration_route():
    """
    Update schema/codelists/administrationRoute.csv.
    """
    # https://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration/
    data, not_selectable = hl7('RouteOfAdministration')

    # "definition" is not used for Description, because it is the same as the "display", except for:
    #
    # - "Inhalation, respiratory", "Inhalation, oral"
    # - "Injection, intrauterine", "Injection, intracervical (uterus)"
    # - "instillation, urethral", "Instillation, urethral" (lettercase change)
    # - "Topical application, vaginal", "Insertion, vaginal" (typographical error)

    with csv_dump('administrationRoute.csv', ['Code', 'Title']) as writer:
        for code in codes:
            if code['properties']['synonymCode']:
                # Prefer IPINHL to its synonyms.
                if code['code'] in ('ORINHL', 'RESPINHL'):
                    continue
                elif code['code'] != 'IPINHL':
                    logger.warning('RouteOfAdministration: unexpected synonymous code: %s', code)
            writer.writerow([code['code'], code['display'][0].upper() + code['display'][1:]])


@cli.command()
def update_dosage_form():
    """
    Update schema/codelists/dosageForm.csv from HL7.
    """
    # https://terminology.hl7.org/CodeSystem/v3-orderableDrugForm/
    codes, not_selectable = hl7('orderableDrugForm')

    with csv_dump('dosageForm.csv', ['Code', 'Title', 'Description']) as writer:
        for code in codes:
            if 'SPRY' in code['code'] or code['code'] != 'SPRY':
                continue
            writer.writerow([code['code'], code['display'], code.get('definition')])


@cli.command()
@click.pass_context
def update(ctx):
    """
    Update external codelists (administration route, container, dosage form).
    """
    ctx.invoke(update_administration_route)
    ctx.invoke(update_container)
    ctx.invoke(update_dosage_form)


if __name__ == '__main__':
    cli()

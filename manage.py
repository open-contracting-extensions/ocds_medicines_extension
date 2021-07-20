#!/usr/bin/env python
import csv
from contextlib import contextmanager
from pathlib import Path

import click
import requests

basedir = Path(__file__).resolve().parent


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


@click.group()
def cli():
    pass


@cli.command()
def update_administration_route():
    """
    Update schema/codelists/administrationRoute.csv.
    """
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
def update_dosage_form():
    """
    Update schema/codelists/dosageForm.csv from HL7.
    """
    # https://terminology.hl7.org/CodeSystem/v3-orderableDrugForm/
    data = requests.get('https://terminology.hl7.org/CodeSystem-v3-orderableDrugForm.json').json()

    # Transform the list of dicts into a dict.
    for code in data['concept']:
        code['properties'] = {'subsumedBy': set()}
        # The properties are: subsumedBy, notSelectable, status, internalId
        for prop in code['property']:
            name, value = prop.values()
            if name == 'subsumedBy':
                code['properties'][name].add(value)
            elif name in code['properties']:
                raise Exception(f"{name} set to {code['properties'][name]}, not {value}")
            else:
                code['properties'][name] = value

    not_selectable = {code['code'] for code in data['concept'] if code['properties'].get('notSelectable')}

    with csv_dump('dosageForm.csv', ['Code', 'Title', 'Description']) as writer:
        for code in data['concept']:
            if (
                code['properties'].get('notSelectable')
                or code['properties']['status'] != 'active'
                or 'SPRY' in code['code']
                and code['code'] != 'SPRY'
            ):
                continue
            # None of the top-level codes has a description.
            if any(parent in not_selectable for parent in code['properties']['subsumedBy']):
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

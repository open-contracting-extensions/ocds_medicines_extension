#!/usr/bin/env python
import csv
import os
import sys
from contextlib import contextmanager
from pathlib import Path

import click
import lxml.html
import requests

basedir = Path(__file__).resolve().parent


def parse(response):
    return lxml.html.fromstring(response.text)


def warn(message):
    click.secho(message, err=True, fg='yellow')


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


@contextmanager
def edqm(email, password, url):
    with requests.Session() as session:
        # Get the CSRF token.
        response = session.get('https://standardterms.edqm.eu/user/login')
        response.raise_for_status()

        formkey = parse(response).xpath('//input[@name="_formkey"]/@value')[0]

        # https://stackoverflow.com/a/12385661/244258
        response = session.post('https://standardterms.edqm.eu', files={
            'email': (None, email),
            'password': (None, password),
            '_formkey': (None, formkey),
            '_formname': (None, 'login'),
        })
        response.raise_for_status()

        # The "export" links do not include definitions, so we scrape the page.
        response = session.post(url)
        response.raise_for_status()

        writer = csv.writer(sys.stdout)
        for status in parse(response).xpath('//span[starts-with(@id, "status_0_")]'):
            if status.xpath('./span/text()')[0] != 'Current':
                continue

            response = session.post(f"https://standardterms.edqm.eu/browse/get_details/{status.attrib['id'][9:]}/en")
            response.raise_for_status()

            document = parse(response)
            keys = document.xpath('.//strong/text()')
            values = [value.strip() for value in document.xpath('.//span[@class="span6"]/text()')]
            properties = dict(zip(keys, values))

            if properties['Domain'] != 'Veterinary only':
                writer.writerow([properties['Term'], properties['Definition']])


def hl7(codelist):
    response = requests.get(f'https://terminology.hl7.org/CodeSystem-v3-{codelist}.json')
    response.raise_for_status()

    data = reponse.json()

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

    if codelist == 'RouteOfAdministration':
        expected = set(['internalId', 'notSelectable', 'status', 'subsumedBy', 'synonymCode'])
    elif codelist == 'orderableDrugForm':
        expected = set(['internalId', 'notSelectable', 'status', 'subsumedBy'])
    else:
        expected = set()

    difference = properties - expected
    if difference:
        warn(f'{codelist}: unexpected new properties: {sorted(difference)}')

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
    # Retain the descriptions from EDQM.
    descriptions = {}
    with (basedir / 'codelists' / 'container.csv').open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            descriptions[row['Code']] = row['Description']

    # https://terminology.hl7.org/CodeSystem/medicationknowledge-package-type/
    response = requests.get('https://terminology.hl7.org/CodeSystem-medicationknowledge-package-type.json')
    response.raise_for_status()

    data = response.json()

    with csv_dump('container.csv', ['Code', 'Title', 'Description']) as writer:
        writer.writerows([[code['code'], code['display'], descriptions[code['code']]] for code in data['concept']])


@cli.command()
def update_administration_route():
    """
    Update schema/codelists/administrationRoute.csv.
    """
    # https://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration/
    codes, not_selectable = hl7('RouteOfAdministration')

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
                    warn(f'RouteOfAdministration: unexpected synonymous code: {code}')
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
            if 'SPRY' in code['code'] and code['code'] != 'SPRY':
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


@cli.command()
@click.argument('email')
@click.argument('password')
def print_edqm_container(email, password):
    edqm(email, password, 'https://standardterms.edqm.eu/browse/get_back_links/en/PAC_PAC/786')


@cli.command()
@click.argument('email')
@click.argument('password')
def print_edqm_administration_route(email, password):
    edqm(email, password, 'https://standardterms.edqm.eu/browse/get_concepts/ROA')


@cli.command()
def download_inn_lists():
    os.makedirs('inn', exist_ok=True)

    response = requests.get('https://www.who.int/teams/health-product-and-policy-standards/inn/inn-lists')
    response.raise_for_status()

    hrefs = parse(response).xpath('//div[@id="PageContent_TA60FDAEF017_Col01"]//@href')
    basenames = [''.join(href.lower().split('-', 2)[1:]) + '.pdf' for href in hrefs]

    base_url = 'https://cdn.who.int/media/docs/default-source/international-nonproprietary-names-(inn)/'
    for basename in basenames:
        filename = os.path.join('inn', basename)
        if not os.path.exists(filename):
            click.echo(f'INFO - Downloading {basename}')
            with open(filename, 'wb') as f:
                response = requests.get(base_url + basename)
                response.raise_for_status()

                f.write(response.content)


if __name__ == '__main__':
    cli()

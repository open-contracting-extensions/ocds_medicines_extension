# Medicine extension

Add medicine attributes to the `items` object to describe specific details about a medicine item.

## Guidance

This extension is based on research with 4 data users and 6 data publishers including public entities, journalists, medicine price analysts and software developers for medicine purchase systems from 9 countries. There are some differences between the names of the attributes in those countries, but the fields in this extension are the most used and defined mainly by [ATC](https://www.whocc.no/atc_ddd_index/) and [Schema.org](https://schema.org/Drug).

This extension is intended to be used in the tender, award, or contract items that represent a medicine, to add more specific details that a medicine item may have. To use it, add the medicine attributes at the item level and set the properties that are known:

* active ingredient: chemical compounds and/or biological substances
* dosage form: dosage form in which this medicine is available
* container: container or presentation form of the medicine
* administration route: route by which this medicine can be given

For the active ingredient dosage and the container capacity, it’s recommended to use the [ATC](https://www.whocc.no/atc_ddd_index/) scheme in `capacity.unit` and `dosage.unit`.

If a contracting process is in the award or contract stage, it’s possible to know more information about the medicine, such as the brand, the manufacturer, the country of origin, the expiration date, if they must maintain a cold chain and all the other commercial, financial and logistical conditions. Use the [generic item attributes](https://gitlab.com/dncp-opendata/ocds_item_attributes_extension) extension for all the cases where the medicine item has other attributes not included in this extension.

If a medicine item has more than one active ingredient, add each one in the `activeIngredients` array.

If a medicine item is packaged in a multi-drug container, use `items.quantity` for the quantity in the container and `items.unit` for the unit.

## Codelists

The administrationRoute.csv codelist is based on the [ATC list](https://www.whocc.no/atc_ddd_index/) (see route of administration).

The dosageForm.csv codelist is based on the values in the list beginning on [Page 27 of the MSH International Medical Products Price Guide](https://www.msh.org/resources/international-medical-products-price-guide).

The container.csv codelist is based on the list on

## Examples

### One Active Ingredient

This is an [example](https://api.mercadopublico.cl/APISOCDS/ocds/tender/734-82-LP14) of an item of a drug procurement process in Chile, and its representation in the extension. 

| Description            | Minimum dispensing unit |
| -----------            |------------------------- |
| Acetilcisteina | ACETILCISTEINA-N 100 MG/ML SOLUCION PARA NEBULIZAR FRASCO 15-30 ML ENVASE INDIVIDUAL RESISTENTE CON SELLO QUE ASEGURE INVIOLABILIDAD DEL CONTENIDO |
```json
{
  "tender": {
    "items": [
      {
        "id": "1",
        "description": "Acetilcisteina",
        "classification": {
          "id": "51161701",
          "scheme": "UNSPSC",
          "uri": "https://apis.mercadopublico.cl/OCDS/data/productos/categoria/51161701"
        },
        "dosageForm": "liquid",
        "administrationRoute": "inhal",
        "container": {
          "name": "jar",
          "capacity": {
            "unit": {
              "scheme": "ATC",
              "id": "ml"
            },
            "quantity": "[15,30]"
          }
        },
        "activeIngredients": [
          {
            "name": "acetilcisteina",
            "dosage": {
              "unit": {
                "scheme": "ATC",
                "id": "ml"
              },
              "quantity": 100
            }
          }
        ]
      }
    ]
  }
}
```
This is an example of an item in the [UNOPS](https://datastudio.google.com/u/0/reporting/1lI9FpXAor0QmSmbZehZWmbrX4F-X1CLw/page/5UYMB?s=swplgxj_6no) system and how it would be represent with the extension.

| Description            | Minimum dispensing unit |
| -----------            |------------------------- |
| Midazolam 5mg / solucion Parenteral | Envase por un 1 ml |
```json
{
  "tender": {
    "items": [
      {
        "id": "1",
        "description": "Midazolam 5mg / solucion Parenteral",
        "dosageForm": "liquid",
        "administrationRoute": "P",
        "container": {
          "name": "jar",
          "capacity": {
            "unit": {
              "scheme": "ATC",
              "id": "ml"
            },
            "quantity": 1
          }
        },
        "activeIngredients": [
          {
            "name": "Midazolam",
            "dosage": {
              "unit": {
                "scheme": "ATC",
                "id": "mg"
              },
              "quantity": 5
            }
          }
        ]
      }
    ]
  }
}
```
### More than one Active Ingredient

This is an [example](https://www.contrataciones.gov.py/licitaciones/convocatoria/391507-adquisicion-medicamentos-hospital-clinicas-1.html#pliego) of an item of a drug procurement processes in Paraguay and how it would be represent with the extension.

| Description            | Technical specifications | Unit of measurement       |  Presentation         |  Delivery presentation |
| -----------            |------------------------- | -----------               |  -----------          | ----------------       |
| Clorhidrato de Bupivacaina Hiperbarica Inyectable     | clorhidrato de bupivacaina 25 mg. + dextrosa 82,5 mg. - solución inyectable | UNIDAD | VIAL | caja conteniendo 25 ampollas como minimo de ml. |
```json
{
  "tender": {
    "items": [
      {
        "id": "1",
        "dosageForm": "injection",
        "administrationRoute": "TD",
        "container": {
          "name": "blister",
          "capacity": {
            "unit": {
              "scheme": "ATC",
              "id": "ml"
            },
            "quantity": 4
          }
        },
        "activeIngredients": [
          {
            "name": "clorhidrato de bupivacaina",
            "dosage": {
              "unit": {
                "scheme": "ATC",
                "id": "mg"
              },
              "quantity": 250
            }
          },
          {
            "name": "dextrosa",
            "dosage": {
              "unit": {
                "scheme": "ATC",
                "id": "mg"
              },
              "quantity": 82.5
            }
          }
        ],
        "quantity": 25,
        "unit": {
          "id": "UNI",
          "name": "Unidad"
        }
      }
    ]
  }
}
```

## Related Standards

The fields, definitions and codelists used in this extension are based on the following standards that are commonly used in the data on public medicine purchases. Each standard is used for the classification, designation or listing of drugs in different countries.

| Standard        | Maintains       |  Purpose                        |
| -----------     | -----------    |  -----------                      |
| [ATC](https://www.whocc.no/atc_ddd_index/)   | [WHO](https://www.who.int/home)         | medicine classification|
| [Schema.org](https://schema.org/Drug)        | [SCHEMA.ORG COMMUNITY GROUP](https://www.w3.org/community/schemaorg/)         | medicine classification|
| [INN](https://www.who.int/teams/health-product-and-policy-standards/inn/)        | [WHO](https://www.who.int/home)         | medicine names|
| [MSH Products Price Guide](https://www.msh.org/resources/international-medical-products-price-guide)        | [Management Sciences for Health](https://www.msh.org/about-us)         | medicine list|
| [SNOMED-CT](https://bioportal.bioontology.org/ontologies/SNOMEDCT?p=classes&conceptid=410942007) | [National Center for Biomedical Ontology](https://ncbo.bioontology.org/about-ncbo) | medicine classification|
| [LME MSPY](https://www.mspbs.gov.py/dependencias/dggies/adjunto/db7bee-ListadodeMedicamentosEsenciales.pdf) | [Ministerio de Salud del Paraguay](https://www.mspbs.gov.py/index.php) | medicine list|
| [Catálogo CBM](http://www.csg.gob.mx/contenidos/priorizacion/cuadro-basico/med/catalogos.html)| [Consejo de Salubridad General de México](http://www.csg.gob.mx/index.html) | medicine list|
| [UNSPSC](https://ncbo.bioontology.org/about-ncbo) | [United Nations](https://www.un.org/en/) |classification of products and services|
| [Catálogo de Productos Farmacéuticos](http://observatorio.digemid.minsa.gob.pe/Precios/ProcesoL/Catalogo/CatalogoProductos.aspx)|[Ministerio de Salud de Perú](https://www.gob.pe/minsa/)| classification of products and services|

## Issues

Report issues for this extension in the [ocds-extensions repository](https://github.com/open-contracting/ocds-extensions/issues), putting the extension's name in the issue's title.

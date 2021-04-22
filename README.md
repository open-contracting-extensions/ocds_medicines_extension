# Medicine extension

Add medicine attributes to tender, award, or contract items to describe the drugs properties. 

## Guidance

Add the MedicineAttributes object and use the properties that are known according to the stage in which the contracting process is at:

* Tender: normally the active ingredient, dosage form, container, route of administration (all the medicine properties that describe the drug).
* Award or Contract: normally the brand, manufacturer, country of origin (commercial, financial and logistics conditions).

If a medicine have other attributes such as the expiration date, how the medicines have to be delivered, if they must maintain a cold chain, etc, use the generic [item attributes extension](https://gitlab.com/dncp-opendata/ocds_item_attributes_extension).

If a medicine has more than one active ingredient, add each one in the `activeIngredients` array.

If a medicine is packaged in a multi-drug container, use `items.quantity` for the quantity in the container and `items.unit` for the unit.

## Proposal

### Schema

* Dosage {Object}
    * numericValue (integer)
    * unit (string) (codelist)

* DosageForm (string) (codeList)

* RouteOfAdministration (string) (codelist)

* Container {Object}
    * id (string, integer)
    * name (string)
    * capacity 
        * $ref : #/definitions/Dosage

* ActiveIngredient {Object}
    * id (string, integer)
    * name (string)
    * dosage 
        * $ref : #/definitions/Dosage

* Item {Object}
    * MedicineAttributes {Object}
        * activeIngredients (array)
            * $ref : #/definitions/ActiveIngredient
        * dosageForm
            * $ref: #/definitions/DosageForm
        * routeOfAdministration 
            * $ref: #/definitions/RouteOfAdministration
        * container 
            * $ref: #/definitions/Container
        * brand
            * $ref: #/definitions/Brand
        * manufacturer
            * $ref: #/definitions/Manufacturer
        * countryOfOrigin
            * $ref: #/definitions/CountryOfOrigin

Where:

| Code                  | Title                     |  Description                                                 |
| -----------           | -----------               |  -----------                                                 |
| dosage                | Dosage                    | The value and unit of the Dosage, Concentration or Capacity  |
| numericValue          | Numeric Value             | The numeric value of the Dosage                              |
| unit                  | Unit                      | The unit of measurement of the Dosage                        |                           
| dosageForm            | Dosage Form               | A dosage form in which this medicine is available            |
| routeOfAdministration | Route of Administration   | A route by which this medicine can be given                  |
| container             | Container                 | The container or presentation form of the medicine  |
| id                    | Container ID              | An identifier for this Container |
| name                  | Container Name            | The name of the container |
| capacity              | Container Capacity        | The Capacity of the container |
| activeIngredient      | Active Ingredient         | Describe an Active Ingredient and dosage for the drug, generally chemical compounds and / or biological substances |
| id                    | Active Ingredient ID      | An identifier for this Active Ingredient |
| name                  | Active Ingredient Name    | The name of the Active Ingredient. It refers to the generic name as in the International Common Denomination (INN). This field is the same as the 'name' attribute in the ATC / DDD standard. Also known as: generic name, drug, substance name, active substance |
| medicineAttributes    | Medicine Attributes       | Describe the attributes and properties of chemical or biological substances used as medical therapy, which has a physiological effect on an organism. Here the term drug is used interchangeably with the term medicine, although clinical knowledge makes a clear difference between them |

## Examples

### One Active Ingredient

This is an [example](https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs=OE1kSVnLUBVxS5IkXPNLRQ==) of an item of a drug procurement process in Chile, and its representation in the extension. 

| Description            | Minimum dispensing unit |
| -----------            |------------------------- |
| Acetilcisteina | ACETILCISTEINA-N 100 MG/ML SOLUCION PARA NEBULIZAR FRASCO 15-30 ML ENVASE INDIVIDUAL RESISTENTE CON SELLO QUE ASEGURE INVIOLABILIDAD DEL CONTENIDO |
```json
{
  "tender": {
    "items": [
      {
        "id": "1",
        "medicineAttributes": {
          "dosageForm": "liquid",
          "routeOfAdministration": "inhal",
          "container": {
            "id": 1,
            "name": "jar",
            "capacity": {
              "numericValue": "15-30",
              "unit": "ml"
            }
          },
          "activeIngredients": [
            {
              "id": 1,
              "name": "acetilcisteina",
              "dosage": {
                "numericValue": 100,
                "unit": "ml"
              }
            }
          ]
        }
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
        "medicineAttributes": {
          "dosageForm": "liquid",
          "routeOfAdministration": "P",
          "container": {
            "id": 1,
            "name": "jar",
            "capacity": {
              "numericValue": 1,
              "unit": "ml"
            }
          },
          "activeIngredients": [
            {
              "id": 1,
              "name": "Midazolam",
              "dosage": {
                "numericValue": 5,
                "unit": "mg"
              }
            }
          ]
        }
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
        "medicineAttributes": {
          "dosageForm": "injection",
          "routeOfAdministration": "TD",
          "container": {
            "id": 1,
            "name": "blister",
            "capacity": {
              "numericValue": 4,
              "unit": "ml"
            }
          },
          "activeIngredients": [
            {
              "id": 2,
              "name": "clorhidrato de bupivacaina",
              "dosage": {
                "numericValue": 250,
                "unit": "mg"
              }
            },
            {
              "id": 3,
              "name": "dextrosa",
              "dosage": {
                "numericValue": 82.5,
                "unit": "mg"
              }
            }
          ]
        },
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

In addition, the following standards for the identification of drugs were analyzed:

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

Report issues for this extension 
in the [ocds-extensions repository](https://github.com/open-contracting/ocds-extensions/issues), 
putting the extension's name in the issue's title.

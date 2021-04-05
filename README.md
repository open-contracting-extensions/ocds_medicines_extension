# Medicine extension

## Description

In the framework of the pandemic, it was possible to observe how the purchase of prescribed drugs for the treatment of COVID-19 patients increased worldwide, including in some countries a result of them was achieved. Considering the supply of these drugs, in some cases prices increased by up to 400 percent.

Verifying the variation in the prices of the same medicine over time, or between countries, is not an easy task and this difficulty favors speculation on prices by the pharmaceutical industry.

Currently, many of the data on the drugs purchased are published in plain text format, or it is only possible to verify them in the terms of reference, which makes their analysis difficult. Publishing data against a single standard will be able to make high-quality price references for identical products, helping to meet the vital need for cross-country comparability that is not always seen in public procurement monitoring.

## Background

With the objective of developing an extension of the OCDS standard for public drug procurement processes, a study was carried out on the way in which drug purchase data is currently published in different countries, the use that users make of it, and the standards of medicines, substances and drugs that exist.

The study included interviews with 6 publishers and 4 users who relate to drug purchases in different ways such as: system maintenance, people who write the terms of reference for medicine purchases, data analysts, medicime price analyst, software developers for medicine purchase systems, advocacy and accountability groups, journalists

The most common questions related to medicine prices were:

<ul>
<li>Q1: How do we know if two products are comparable?</li>
<li>Q2: Is it possible to make price comparisons between different medicine vendors?</li>
<li>Q3: Are the products on the price reference list?</li>
<li>Q4: How much and at what price was it purchased and from whom?</li>
<li>Q5: Is there a noticeable difference between the market and awarded prices?</li>
<li>Q6: What is the average price of the public market in the last X months?</li>
<li>Q7: Who are the bidders and what are the purchase conditions?</li>
<li>Q8: Who was it bought from?</li>
<li>Q9: Who buys?</li>
<li>Q10: What is the relationship between suppliers, shareholders, laboratories and political finance?</li>
<li>Q11: What is the evolution of prices over time?</li>
<li>Q12: What is the manufacturer's quality, delivery time, and contract performance guarantee?</li>
<li>Q13: How much does what was spent on this input represent against the entity's budget?</li>
</ul>

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

This analysis resulted in the list of attributes of the extension.

## Proposal:

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
  
### Codelists

* Dosage Form
    * Tablet
    * Liquid
    * Suspension
    * Injection
    * Cream
    * Ear Drops
    * Gas
    * Gel
    * Inhaler
    * Powder
    * Lotion
    * Spray
    * Suppository
    * Test


* Route of Administration
    * Implant
    * Inhalation
    * Instillation
    * Nasal
    * Oral
    * Parenteral
    * Rectal
    * Sublingual / Buccal / Oromucosal
    * Transdermal
    * Vaginal
    

* Dosage Unit
    * Gram
    * Miligram
    * Microgram
    * Milliliter
    * Millimole
    * Unit
    * Thousand Units
    * Million Units


* Container
    * Jar
    * Blister
    * Blister Vial
    * Dropper Bottle
    * Pre-Filled Syringe
    * Tube
    * Compressed
    * Cartridge
  
### Examples

This is an example of an item in the UNOPS system and how it would be represent with the extension.

| Description            | Minimum dispensing unit |
| -----------            |------------------------- |
| Midazolam 5mg / solucion Parenteral | Envase por un 1 ml |
```
  "item" : {
    "medicineAttributes" : {   
      "dosageForm" :  "liquid",
      "routeOfAdministration" : "Parenteral",
      "container" : {
        "id" : 1
        "name" : "jar",
        "capacity: {
          "numericValue" : 1,
          "unit" : "ml"
        }
      },
      "activeIngredient" : [
        {
          "id" : 1,
          "name" : "Midazolam",
          "dosage" : {
            "numericValue" : 5,
            "unit" : "mg"
          }
        }
      ]        
    }
  }
```
This is an [example](https://www.contrataciones.gov.py/licitaciones/convocatoria/391507-adquisicion-medicamentos-hospital-clinicas-1.html#pliego) of an item of a drug procurement processes in Paraguay and how it would be represent with the extension.

| Description            | Technical specifications | Unit of measurement       |  Presentation         |  Delivery presentation |
| -----------            |------------------------- | -----------               |  -----------          | ----------------       |
| Clorhidrato de Bupivacaina Hiperbarica Inyectable     | clorhidrato de bupivacaina 25 mg. + dextrosa 82,5 mg. - solución inyectable | UNIDAD | VIAL | caja conteniendo 25 ampollas como minimo de ml. |
```
  "item" : {
    "medicineAttributes" : {   
      "dosageForm" :  "injection",
      "routeOfAdministration" : "TD",
      "container" : {
        "id" : 25
        "name" : "blister",
        "capacity: {
          "numericValue" : 4,
          "unit" : "ml"
        }
      },
      "activeIngredient" : [
        {
          "id" : 2,
          "name" : "clorhidrato de bupivacaina",
          "dosage" : {
            "numericValue" : 250,
            "unit" : "mg"
          }
        },
        {
          "id" : 3,
          "name" : "dextrosa",
          "dosage" : {
            "numericValue" : 82.5,
            "unit" : "mg"
          }
        }
      ]        
    }
  }
```


## Defining texts:

| Code                  | Title                     |  Description                                                 |
| -----------           | -----------               |  -----------                                                 |
| dosage                | Dosage                    | The value and unit of the Dosage, Concentration or Capacity  |
| numericValue          | Numeric Value             | The numeric value of the Dosage                              |
| unit                  | Unit                      | The unit of measurement of the Dosage                        |                           
| dosageForm            | Dosage Form               | A dosage form in which this medicine is available            |
| routeOfAdministration | Route of Administration   | A route by which this medicine can be given                  |
| container             | Container                 | The container or presentation form of the medicine  |
| id                    | ID                        | An identifier for this Container |
| name                  | Container Name            | The name of the container |
| capacity              | Container Capacity        | The Capacity of the container |
| activeIngredient      | Active Ingredient         | Describe an Active Ingredient and dosage for the drug, generally chemical compounds and / or biological substances |
| id                    | ID                        | An identifier for this Active Ingredient |
| name                  | Active Ingredient Name    | The name of the Active Ingredient. It refers to the generic name as in the International Common Denomination (INN). This field is the same as the 'name' attribute in the ATC / DDD standard. Also known as: generic name, drug, substance name, active substance |
| medicineAttributes    | Medicine Attributes       | Describe the attributes and properties of chemical or biological substances used as medical therapy, which has a physiological effect on an organism. Here the term drug is used interchangeably with the term medicine, although clinical knowledge makes a clear difference between them |


## Issues

Report issues for this extension 
in the [ocds-extensions repository](https://github.com/open-contracting/ocds-extensions/issues), 
putting the extension's name in the issue's title.

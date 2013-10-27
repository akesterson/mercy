import os
import nose
from nose.tools import raises
import mercy.models
import mercy.importers.fda
import mercy.exceptions

COMPARISON_KEYS={
    'productid': 'PRODUCTID',
    'ndc': 'PRODUCTNDC',
    'type': 'PRODUCTTYPENAME',
    'proprietaryName': 'PROPRIETARYNAME',
    'proprietaryNameSuffix': 'PROPRIETARYNAMESUFFIX',
    'genericName': 'NONPROPRIETARYNAME',
    'marketingCategoryName': 'MARKETINGCATEGORYNAME',
    'labelerName': 'LABELERNAME',
    'deaSchedule': 'DEASCHEDULE'
    }

CSV_KEYS=[
    'PRODUCTID',
    'PRODUCTNDC',
    'PRODUCTTYPENAME',
    'PROPRIETARYNAME',
    'PROPRIETARYNAMESUFFIX',
    'NONPROPRIETARYNAME',
    'DOSAGEFORMNAME',
    'ROUTENAME',
    'STARTMARKETINGDATE',
    'ENDMARKETINGDATE',
    'MARKETINGCATEGORYNAME',
    'APPLICATIONNUMBER',
    'LABELERNAME',
    'SUBSTANCENAME',
    'ACTIVE_NUMERATOR_STRENGTH',
    'ACTIVE_INGRED_UNIT',
    'PHARM_CLASSES',
    'DEASCHEDULE'
    ]

CANNED_ROWS=[
    {'PRODUCTID': '0002-3230_b1642902-4a44-495a-8790-39598b168276',
     'PRODUCTNDC': '0002-3230',
     'PRODUCTTYPENAME': 'HUMAN PRESCRIPTION DRUG',
     'PROPRIETARYNAME': 'Symbyax',
     'PROPRIETARYNAMESUFFIX': '',
     'NONPROPRIETARYNAME': 'Olanzapine and Fluoxetine hydrochloride',
     'DOSAGEFORMNAME': 'CAPSULE',
     'ROUTENAME': 'ORAL',
     'STARTMARKETINGDATE': '20070409',
     'ENDMARKETINGDATE': '',
     'MARKETINGCATEGORYNAME': 'NDA',
     'APPLICATIONNUMBER': 'NDA021520',
     'LABELERNAME': 'Eli Lilly and Company',
     'SUBSTANCENAME': 'FLUOXETINE HYDROCHLORIDE; OLANZAPINE',
     'ACTIVE_NUMERATOR_STRENGTH': '25; 3',
     'ACTIVE_INGRED_UNIT': 'mg/1; mg/1',
     'PHARM_CLASSES': 'Atypical Antipsychotic [EPC],Serotonin Reuptake Inhibitor [EPC],Serotonin Uptake Inhibitors [MoA]',
     'DEASCHEDULE': ''
     },
    {'PRODUCTID': '0002-3231_b1642902-4a44-495a-8790-39598b168276',
     'PRODUCTNDC': '0002-3231',
     'PRODUCTTYPENAME': 'HUMAN PRESCRIPTION DRUG',
     'PROPRIETARYNAME': 'Symbyax',
     'PROPRIETARYNAMESUFFIX': '',
     'NONPROPRIETARYNAME': 'Olanzapine and Fluoxetine hydrochloride',
     'DOSAGEFORMNAME': 'CAPSULE',
     'ROUTENAME': 'ORAL',
     'STARTMARKETINGDATE': '20070409',
     'ENDMARKETINGDATE': '',
     'MARKETINGCATEGORYNAME': 'NDA',
     'APPLICATIONNUMBER': 'NDA021521',
     'LABELERNAME': 'Eli Lilly and Company',
     'SUBSTANCENAME': 'FLUOXETINE HYDROCHLORIDE; OLANZAPINE',
     'ACTIVE_NUMERATOR_STRENGTH': '25; 6',
     'ACTIVE_INGRED_UNIT': 'mg/1; mg/1',
     'PHARM_CLASSES': 'Atypical Antipsychotic [EPC],Serotonin Reuptake Inhibitor [EPC],Serotonin Uptake Inhibitors [MoA]',
     'DEASCHEDULE': ''
     }
    ]

FIXTUREFILE=os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "fixtures",
        "fda_database.txt"
        )
    )

FIXTUREFILE_BAD=os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "fixtures",
        "fda_database_bad.txt"
        )
    )

def test_fda_import_populates_table():
    with open(FIXTUREFILE, 'w') as ofile:
        ofile.write("{}\n".format('\t'.join(CSV_KEYS)))
        for row in CANNED_ROWS:
            values = []
            for key in CSV_KEYS:
                values.append(row[key])
            ofile.write("{}\n".format('\t'.join(values)))
    importer = mercy.importers.fda.FDAImporter()
    importer.read(FIXTUREFILE)
    for row in CANNED_ROWS:
        product = mercy.models.fda.Product.query.filter_by(productid = row['PRODUCTID']).first()
        assert(product)
        for (k, v) in COMPARISON_KEYS.iteritems():
            assert(getattr(product, k) == row[v])
        mapquery = mercy.models.fda.ProductSubstanceMap.query
        substanceMaps = [x for x in mapquery.filter_by(product_id=product.id)]
        assert(len(substanceMaps) == len(row['ACTIVE_NUMERATOR_STRENGTH'].split(';')))
        # TO DO : This test doesn't look at the contents of the
        # substances or substance maps, only that the right
        # number of substance maps come out

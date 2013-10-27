import mercy.MercyApplication
import xml.etree.cElementTree as ET
from mercy.models.fda import Product
from mercy.models.fda import ProductSubstance
from mercy.models.fda import ProductSubstanceMap
from mercy.models.fda import PharmaceuticalClass
from mercy.models.fda import PharmaceuticalClassMap
import sqlalchemy.exc
import csv

class FDAImporter:
    def __init__(self, *args, **kwargs):
        self.__db = mercy.MercyApplication.get_db()

    def read(self, fname, startIdx=0):
        with open(fname, "r") as ifile:
            reader = csv.DictReader(ifile, delimiter="\t")
            idx = 0
            for row in reader:
                if idx < startIdx:
                    print "Skipping from {} to {}".format(idx, startIdx)
                    idx += 1
                    continue
                retries = 0
                print "{} : {}".format(idx, row)
                while retries < 3 :
                    try:
                        self._convert_row(row)
                        retries = 3
                    except sqlalchemy.exc.DatabaseError, e:
                        retries += 1
                        if retries == 3:
                            raise e
                        else:
                            continue
                idx += 1


    def _saveobj(self, obj):
        self.__db.session.add(obj)
        self.__db.session.commit()

    def _convert_row(self, row):
        # The FDA CSV is HIGHLY irregular. This function is needlessly large because of that/
        product = Product.query.filter_by(productid=row['PRODUCTID']).first()
        if not product:
            product = Product()
        product.productid = row['PRODUCTID']
        product.ndc = row['PRODUCTNDC']
        product.type = row['PRODUCTTYPENAME']
        product.proprietaryName = row['PROPRIETARYNAME']
        product.proprietaryNameSuffix = row['PROPRIETARYNAMESUFFIX']
        product.genericName = row['NONPROPRIETARYNAME']
        product.marketingCategoryName = row['MARKETINGCATEGORYNAME']
        product.labelerName = row['LABELERNAME']
        product.deaSchedule = (row['DEASCHEDULE'] if row['DEASCHEDULE'] else '')
        self._saveobj(product)

        # Strip the substances off of the product and make objects for them
        substanceNames = [x.strip().lstrip() for x in row['SUBSTANCENAME'].split(';')]
        tmpQtys = [x.strip().lstrip() for x in row['ACTIVE_NUMERATOR_STRENGTH'].split(';')]
        # The list addition here is to make sure we have an equal number of values in
        # quantities as we do in substance names, because the FDA CSV does not ensure
        # that all substance names have a quantity or unit listed. So unknown quantities
        # get entered as '0', unknown units of measure become '?'.
        substanceQtys = [(float(x) if x else 0.0) for x in tmpQtys] + ([0] * (len(substanceNames) - len(tmpQtys)))
        substanceUnits = [x.strip().lstrip() for x in row['ACTIVE_INGRED_UNIT'].split(';')]
        substanceUnits += (['?'] * (len(substanceNames) - len(substanceUnits)))

        for idx in range(0, len(substanceNames)):
            substance = None
            substanceName = substanceNames[idx]

            substance = ProductSubstance.query.filter_by(name=substanceName).first()
            if not substance:
                substance = ProductSubstance()
                substance.name = substanceName
                self._saveobj(substance)
            substanceMap = ProductSubstanceMap.query.filter_by(product_id=product.id,
                                                               substance_id=substance.id,
                                                               quantity=substanceQtys[idx],
                                                               units=substanceUnits[idx]).first()
            if not substanceMap:
                substanceMap = ProductSubstanceMap()
                substanceMap.product_id = product.id
                substanceMap.substance_id = substance.id
                substanceMap.quantity = substanceQtys[idx]
                substanceMap.units = substanceUnits[idx]
                self._saveobj(substanceMap)

        pharmaClassList = row.get('PHARM_CLASSES')
        pharmaClasses = [x.strip().lstrip() for x in (pharmaClassList if pharmaClassList else '').split(',')]
        for pharmaClass in pharmaClasses:
            pharmaObj = PharmaceuticalClass.query.filter_by(name=pharmaClass).first()
            if not pharmaObj:
                pharmaObj = PharmaceuticalClass()
                pharmaObj.name = pharmaClass
                self._saveobj(pharmaObj)
            mapObj = PharmaceuticalClassMap.query.filter_by(
                product_id=product.id,
                pharma_id=pharmaObj.id).first()
            if not mapObj:
                mapObj = PharmaceuticalClassMap()
                mapObj.product_id = product.id
                mapObj.pharma_id = pharmaObj.id
                self._saveobj(mapObj)
        return

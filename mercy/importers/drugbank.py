import mercy.MercyApplication
import xml.dom.pulldom
from mercy.models.drugbank import *
import sqlalchemy.exc
import xpath

class DrugBankImporter:
    def __init__(self, *args, **kwargs):
        self.__db = mercy.MercyApplication.get_db()

    def _saveobj(self, obj):
        self.__db.session.add(obj)
        self.__db.session.commit()

    def read(self, fname):
        events = xml.dom.pulldom.parse(fname)
        for event, node in events:
            if event == xml.dom.pulldom.START_ELEMENT and node.tagName == 'drug':
                events.expandNode(node)
                self.__convert_drug(node)

    def __convert_drug(self, node):
        drug = Drug()
        drug.name = xpath.findvalue('name', node)
        drug.indication = xpath.findvalue('indication', node)
        drug.fda_product_id = xpath.findvalue('external-identifiers/external-identifier[starts-with(resource, "National Drug Code Directory")]/identifier', node)
        drug.wikipedia = xpath.findvalue('external-links/external-link[starts-with(resource, "Wikipedia")]/url', node)
        if not drug.fda_product_id:
            return
        print str(drug)
        #self._saveobj(drug)

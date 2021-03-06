import sqlalchemy as sa
from mercy.models.simplemodel import SimpleModel
import mercy.MercyApplication
from mercy.models.fda import Product
import sqlalchemy.dialects.postgresql as pgdialect

db = mercy.MercyApplication.get_db()

class Drug(SimpleModel, db.Model):
    __tablename__ = "drugbank_drugs"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    dbid = sa.Column(sa.String, index=True, unique=True)
    name = sa.Column(sa.String, nullable=False, index=True)
    indication = sa.Column(sa.String, nullable=False)
    fda_product_id = sa.Column(sa.String, sa.ForeignKey(Product.productid), nullable=True)
    wikipedia = sa.Column(sa.String, nullable=True)

    __repr_keys__ = { 'id': basestring,
                      'name': basestring,
                      'fda_product_id': basestring,
                      'wikipedia': basestring
                      }

class Price(SimpleModel, db.Model):
    __tablename__ = "drugbank_prices"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    drug_id = sa.Column(sa.Integer, sa.ForeignKey(Drug.id), nullable=False)
    description = sa.Column(sa.String, nullable=False)
    currency = sa.Column(sa.String, nullable=False)
    cost = sa.Column(sa.Float, nullable=False, index=True)
    unit = sa.Column(sa.String, nullable=False)

class CategoryName(SimpleModel, db.Model):
    __tablename__ = "drugbank_categories"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sa.Column(sa.String, nullable=False, unique=True)

class CategoryMap(SimpleModel, db.Model):
    __tablename__ = "drugbank_category_maps"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    drug_id = sa.Column(sa.Integer, sa.ForeignKey(Drug.id), nullable=False)
    category_id = sa.Column(sa.Integer, sa.ForeignKey(CategoryName.id), nullable=False)

class Packager(SimpleModel, db.Model):
    __tablename__ = "drugbank_packagers"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sa.Column(sa.String, nullable=False, unique=True)
    url = sa.Column(sa.String, nullable=True)

class PackagerMap(SimpleModel, db.Model):
    __tablename__ = "drugbank_packager_maps"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    drug_id = sa.Column(sa.String, sa.ForeignKey(Drug.id), nullable=False)
    packager_id = sa.Column(sa.Integer, sa.ForeignKey(Packager.id), nullable=False)

class Manufacturer(SimpleModel, db.Model):
    __tablename__ = "drugbank_manufacturers"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sa.Column(sa.String, nullable=False, unique=True)

class ManufacturerMap(SimpleModel, db.Model):
    __tablename__ = "drugbank_manufacturer_maps"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    drug_id = sa.Column(sa.Integer, sa.ForeignKey(Drug.id), nullable=False)
    manufacturer_id = sa.Column(sa.Integer, sa.ForeignKey(Manufacturer.id), nullable=False)

class GenericName(SimpleModel, db.Model):
    __tablename__ = "drugbank_genericnames"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    drug_id = sa.Column(sa.Integer, sa.ForeignKey(Drug.id), nullable=False)
    name = sa.Column(sa.String, nullable=False)

class Synonym(SimpleModel, db.Model):
    __tablename__ = "drugbank_synonyms"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    drug_id = sa.Column(sa.Integer, sa.ForeignKey(Drug.id), nullable=False)
    name = sa.Column(sa.String, nullable=False)

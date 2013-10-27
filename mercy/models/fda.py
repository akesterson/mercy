import sqlalchemy as sa
from mercy.models.simplemodel import SimpleModel
import mercy.MercyApplication
import sqlalchemy.dialects.postgresql as pgdialect

db = mercy.MercyApplication.get_db()

class Product(SimpleModel, db.Model):
    __tablename__ = 'fda_products'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    productid = sa.Column(sa.String, index=True, unique=True, nullable=False)
    ndc = sa.Column(sa.String, index=True, nullable=False)
    type = sa.Column(sa.String, nullable=False)
    proprietaryName = sa.Column(sa.String, nullable=False, index=True)
    proprietaryNameSuffix = sa.Column(sa.String)
    genericName = sa.Column(sa.String, nullable=False, index=True)
    marketingCategoryName = sa.Column(sa.String, nullable=False)
    labelerName = sa.Column(sa.String, nullable=False)
    deaSchedule = sa.Column(sa.String, nullable=False)

    __repr_keys__ = { 'id': basestring,
                      'ndc': basestring,
                      'genericName': basestring,
                      'proprietaryName': basestring,
                      'proprietaryNameSuffix': basestring}

class ProductSubstance(SimpleModel, db.Model):
    __tablename__ = 'fda_product_substances'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sa.Column(sa.String, nullable=False)

class ProductSubstanceMap(SimpleModel, db.Model):
    __tablename__ = 'fda_product_substance_map'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    product_id = sa.Column(sa.Integer,
                           sa.ForeignKey(Product.id),
                           nullable=False)
    substance_id = sa.Column(sa.Integer,
                             sa.ForeignKey(ProductSubstance.id),
                             nullable=False,
                             index=True)
    quantity = sa.Column(sa.Float, nullable=False)
    units = sa.Column(sa.String, nullable=False)


class PharmaceuticalClass(SimpleModel, db.Model):
    __tablename__ = "fda_pharma_classes"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sa.Column(sa.String, nullable=False, unique=True)

class PharmaceuticalClassMap(SimpleModel, db.Model):
    __tablename__ = "fda_pharma_class_maps"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    product_id = sa.Column(sa.Integer,
                           sa.ForeignKey(Product.id),
                           nullable=False)
    pharma_id = sa.Column(sa.Integer,
                          sa.ForeignKey(PharmaceuticalClass.id),
                          primary_key=True,
                          nullable=False)

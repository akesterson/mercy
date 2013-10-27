import sqlalchemy as sa
from mercy.models.simplemodel import SimpleModel
import mercy.MercyApplication
import sqlalchemy.dialects.postgresql as pgdialect

db = mercy.MercyApplication.get_db()

class Product(SimpleModel, db.Model):
    __tablename__ = 'fda_products'

    id = sa.Column(sa.String, primary_key=True)
    ndc = sa.Column(sa.String, nullable=False)
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

    fda_product_id = sa.Column(sa.String,
                               sa.ForeignKey(Product.id),
                               primary_key=True,
                               nullable=False)
    substanceName = sa.Column(sa.String, nullable=False)
    strengthNumber = sa.Column(sa.Float, nullable=False)
    strengthUnit = sa.Column(sa.String, nullable=False)
    pharmaClasses = sa.Column(pgdialect.ARRAY(sa.String), nullable=False)

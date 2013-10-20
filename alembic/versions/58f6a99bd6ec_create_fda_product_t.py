"""create fda_product table

Revision ID: 58f6a99bd6ec
Revises: None
Create Date: 2013-10-19 21:21:03.977000

"""

# revision identifiers, used by Alembic.
revision = '58f6a99bd6ec'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'fda_products',
        sa.Column('id', sa.String, primary_key=True),
        sa.Column('ndc', sa.String, nullable=False),
        sa.Column('type', sa.String, nullable=False),
        sa.Column('proprietaryName', sa.String, nullable=False, index=True),
        sa.Column('proprietaryNameSuffix', sa.String),
        sa.Column('genericName', sa.String, nullable=False),
        sa.Column('marketingCategoryName', sa.String, nullable=False),
        sa.Column('labelerName', sa.String, nullable=False),
        sa.Column('deaSchedule', sa.String, nullable=False)
        )
    op.create_table(
        'fda_product_substances',
        sa.Column('fda_product_id',
                  sa.String,
                  sa.ForeignKey('fda_products.id'),
                  nullable=False),
        sa.Column('substanceName', sa.String, nullable=False),
        sa.Column('strengthNumber', sa.String, nullable=False),
        sa.Column('strengthUnit', sa.String, nullable=False),
        sa.Column('pharmaClasses', sa.String, nullable=False)
        )
    op.create_table(
        'drugbank_drugs',
        sa.Column('id', sa.String, primary_key=True, unique=True),
        sa.Column('name', sa.String, nullable=False, index=True),
        sa.Column('indication', sa.String, nullable=False),
        sa.Column('ndc_id', sa.String, sa.ForeignKey('fda_products.id'), nullable=True),
        sa.Column('wikipedia', sa.String, nullable=True)
        )
    op.create_table(
        'drugbank_prices',
        sa.Column('id', sa.String, sa.ForeignKey('drugbank_drugs.id'), nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('currency', sa.String, nullable=False),
        sa.Column('cost', sa.Float, nullable=False, index=True),
        sa.Column('unit', sa.String, nullable=False)
        )
    op.create_table(
        'drugbank_categories',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False)
        )
    op.create_table(
        'drugbank_drug_categories',
        sa.Column('id', sa.String, sa.ForeignKey('drugbank_drugs.id'), nullable=False),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('drugbank_categories.id'), nullable=False)
        )
    op.create_table(
        'drugbank_packagers',
        sa.Column('id', sa.String, sa.ForeignKey('drugbank_drugs.id'), nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('url', sa.String, nullable=False)
        )
    op.create_table(
        'drugbank_manufacturers',
        sa.Column('id', sa.String, sa.ForeignKey('drugbank_drugs.id'), nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('generic', sa.Boolean, nullable=False)
        )
    op.create_table(
        'drugbank_genericnames',
        sa.Column('id', sa.String, sa.ForeignKey('drugbank_drugs.id'), nullable=False),
        sa.Column('name', sa.String, index=True, nullable=False)
        )
    op.create_table(
        'drugbank_synonyms',
        sa.Column('id', sa.String, sa.ForeignKey('drugbank_drugs.id'), nullable=False),
        sa.Column('name', sa.String, index=True, nullable=False)
        )

def downgrade():
    pass

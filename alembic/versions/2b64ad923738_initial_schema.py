"""Initial schema

Revision ID: 2b64ad923738
Revises: None
Create Date: 2013-10-27 11:46:11.475707

"""

# revision identifiers, used by Alembic.
revision = '2b64ad923738'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fda_products',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('productid', sa.String(), index=True, unique=True, nullable=False),
    sa.Column('ndc', sa.String(), index=True, nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('proprietaryName', sa.String(), nullable=False),
    sa.Column('proprietaryNameSuffix', sa.String(), nullable=True),
    sa.Column('genericName', sa.String(), nullable=False),
    sa.Column('marketingCategoryName', sa.String(), nullable=False),
    sa.Column('labelerName', sa.String(), nullable=False),
    sa.Column('deaSchedule', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('drugbank_packagers',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('drugbank_manufacturers',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('fda_pharma_classes',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('fda_product_substances',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('drugbank_categories',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('fda_pharma_class_maps',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('pharma_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pharma_id'], ['fda_pharma_classes.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['fda_products.id'], ),
    sa.PrimaryKeyConstraint('id', 'pharma_id')
    )
    op.create_table('drugbank_drugs',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('dbid', sa.String(), unique=True, nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('indication', sa.String(), nullable=False),
    sa.Column('fda_product_id', sa.String(), nullable=True),
    sa.Column('wikipedia', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['fda_product_id'], ['fda_products.productid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fda_product_substance_map',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('substance_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('units', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['fda_products.id'], ),
    sa.ForeignKeyConstraint(['substance_id'], ['fda_product_substances.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('drugbank_synonyms',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('drug_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['drug_id'], ['drugbank_drugs.id'], ),
    sa.PrimaryKeyConstraint('drug_id')
    )
    op.create_table('drugbank_packager_maps',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('drug_id', sa.Integer(), nullable=False),
    sa.Column('packager_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['drug_id'], ['drugbank_drugs.id'], ),
    sa.ForeignKeyConstraint(['packager_id'], ['drugbank_packagers.id'], ),
    sa.PrimaryKeyConstraint('drug_id')
    )
    op.create_table('drugbank_genericnames',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('drug_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['drug_id'], ['drugbank_drugs.id'], ),
    sa.PrimaryKeyConstraint('drug_id')
    )
    op.create_table('drugbank_prices',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('drug_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('currency', sa.String(), nullable=False),
    sa.Column('cost', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['drug_id'], ['drugbank_drugs.id'], ),
    sa.PrimaryKeyConstraint('drug_id')
    )
    op.create_table('drugbank_manufacturer_maps',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('drug_id', sa.Integer(), nullable=False),
    sa.Column('manufacturer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['drug_id'], ['drugbank_drugs.id'], ),
    sa.ForeignKeyConstraint(['manufacturer_id'], ['drugbank_manufacturers.id'], ),
    sa.PrimaryKeyConstraint('drug_id')
    )
    op.create_table('drugbank_category_maps',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('drug_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['drugbank_categories.id'], ),
    sa.ForeignKeyConstraint(['drug_id'], ['drugbank_drugs.id'], ),
    sa.PrimaryKeyConstraint('drug_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('drugbank_category_maps')
    op.drop_table('drugbank_manufacturer_maps')
    op.drop_table('drugbank_prices')
    op.drop_table('drugbank_genericnames')
    op.drop_table('drugbank_packager_maps')
    op.drop_table('drugbank_synonyms')
    op.drop_table('fda_product_substance_map')
    op.drop_table('drugbank_drugs')
    op.drop_table('fda_pharma_class_maps')
    op.drop_table('drugbank_categories')
    op.drop_table('fda_product_substances')
    op.drop_table('fda_pharma_classes')
    op.drop_table('fda_products')
    op.drop_table('drugbank_manufacturers')
    op.drop_table('drugbank_packagers')
    ### end Alembic commands ###
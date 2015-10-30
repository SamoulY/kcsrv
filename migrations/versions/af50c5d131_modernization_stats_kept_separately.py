"""modernization stats kept separately

Revision ID: af50c5d131
Revises: 83e8534880
Create Date: 2015-10-24 23:31:17.217936

"""

# revision identifiers, used by Alembic.
revision = 'af50c5d131'
down_revision = '83e8534880'

from alembic import op
import sqlalchemy as sa


def upgrade():
### commands auto generated by Alembic - please adjust! ###
    op.add_column('kanmusu', sa.Column('modern_stats_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_kanmusu_modern_stats_id'), 'kanmusu', ['modern_stats_id'], unique=False)
    op.create_foreign_key(None, 'kanmusu', 'stats', ['modern_stats_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'kanmusu', type_='foreignkey')
    op.drop_index(op.f('ix_kanmusu_modern_stats_id'), table_name='kanmusu')
    op.drop_column('kanmusu', 'modern_stats_id')
    ### end Alembic commands ###
"""changing id type

Revision ID: 673ab038dcab
Revises: 81ec7c9b7e7e
Create Date: 2020-11-01 23:05:23.354937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '673ab038dcab'
down_revision = '81ec7c9b7e7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.alter_column('budget_type',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.alter_column('budget_type',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)

    # ### end Alembic commands ###
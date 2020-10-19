"""Initial

Revision ID: a2a73fc5d6b4
Revises: 
Create Date: 2020-10-19 10:06:49.150262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2a73fc5d6b4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)

    # ### end Alembic commands ###

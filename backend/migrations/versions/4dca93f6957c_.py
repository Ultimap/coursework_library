"""empty message

Revision ID: 4dca93f6957c
Revises: 83ed8e5dbc19
Create Date: 2023-10-05 18:41:43.709045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4dca93f6957c'
down_revision: Union[str, None] = '83ed8e5dbc19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Authors', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Authors', 'birth_data',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('Authors', 'death_data',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('Books', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Books', 'count',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Books', 'age_restriction',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Users', 'age',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Users', 'age',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Books', 'age_restriction',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Books', 'count',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Books', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('Authors', 'death_data',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('Authors', 'birth_data',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('Authors', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
"""empty message

Revision ID: 3fdf4777fb8d
Revises: 
Create Date: 2023-10-04 16:56:38.784322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fdf4777fb8d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Authors',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('birth_data', sa.TIMESTAMP(), nullable=True),
    sa.Column('death_data', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Style',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Books',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('img', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('style', sa.Integer(), nullable=True),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.Column('age_restriction', sa.Integer(), nullable=True),
    sa.Column('release_date', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['Authors.id'], ),
    sa.ForeignKeyConstraint(['style'], ['Style.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role'], ['Roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('Accounting',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('book', sa.Integer(), nullable=True),
    sa.Column('unique_key', sa.String(), nullable=True),
    sa.Column('availability', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['book'], ['Books.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('UsersBooks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user', sa.UUID(), nullable=True),
    sa.Column('book', sa.Integer(), nullable=True),
    sa.Column('date_receipt', sa.TIMESTAMP(), nullable=True),
    sa.Column('date_return', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['book'], ['Books.id'], ),
    sa.ForeignKeyConstraint(['user'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('UsersBooks')
    op.drop_table('Accounting')
    op.drop_table('Users')
    op.drop_table('Books')
    op.drop_table('Style')
    op.drop_table('Roles')
    op.drop_table('Authors')
    # ### end Alembic commands ###
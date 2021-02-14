"""init

Revision ID: 2059673a8e9e
Revises: 
Create Date: 2021-02-14 18:44:19.521502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2059673a8e9e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('players',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=225), nullable=True),
    sa.Column('twitch_followers_count', sa.Integer(), nullable=True),
    sa.Column('instagram_followers_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('players')
    # ### end Alembic commands ###
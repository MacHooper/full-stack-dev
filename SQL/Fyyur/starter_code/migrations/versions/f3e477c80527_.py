"""empty message

Revision ID: f3e477c80527
Revises: 199af702c4eb
Create Date: 2020-05-08 12:11:48.262277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3e477c80527'
down_revision = '199af702c4eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', sa.String(), nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('web_link', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'web_link')
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'genres')
    # ### end Alembic commands ###

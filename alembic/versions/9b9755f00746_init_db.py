"""init_db

Revision ID: 9b9755f00746
Revises: 
Create Date: 2024-05-05 20:26:28.991883

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b9755f00746'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('models',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('task_name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('input_type', sa.String(length=255), nullable=False),
    sa.Column('output_type', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['task_name'], ['tasks.name'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('models')
    op.drop_table('tasks')
    # ### end Alembic commands ###
"""create tasks table"""

from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('priority', sa.Integer(), server_default='3'),
        sa.Column('completed', sa.Boolean(), server_default=sa.text('FALSE')),
        sa.Column('parent_id', sa.String(length=36), sa.ForeignKey('tasks.id'), nullable=True),
    )


def downgrade():
    op.drop_table('tasks')

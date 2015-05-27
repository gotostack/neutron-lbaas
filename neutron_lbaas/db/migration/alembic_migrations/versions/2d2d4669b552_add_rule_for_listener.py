"""add rule for listener

Revision ID: 2d2d4669b552
Revises: kilo
Create Date: 2015-05-27 12:01:36.339093

"""

# revision identifiers, used by Alembic.
revision = '2d2d4669b552'
down_revision = 'kilo'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'lbaas_rules',
        sa.Column('tenant_id', sa.String(36), nullable=True),
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('listener_id', sa.String(36), nullable=True),
        sa.Column('rule', sa.String(1024), nullable=False),
        sa.Column('admin_state_up', sa.Boolean(), nullable=False),
        sa.Column('provisioning_status', sa.String(16), nullable=False),
        sa.Column('operating_status', sa.String(16), nullable=False),

        sa.ForeignKeyConstraint(['listener_id'],
                                ['lbaas_listeners.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('lbaas_rules')

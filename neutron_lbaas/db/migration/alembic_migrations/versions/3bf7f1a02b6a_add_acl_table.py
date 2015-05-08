# Copyright 2015 Letv Cloud Computing
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""add acl table

Revision ID: 3bf7f1a02b6a
Revises: 4ba00375f715
Create Date: 2015-04-17 18:00:01.760041

"""

# revision identifiers, used by Alembic.
revision = '3bf7f1a02b6a'
down_revision = 'kilo'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'lbaas_acls',
        sa.Column('tenant_id', sa.String(36), nullable=True),
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('listener_id', sa.String(36), nullable=True),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('action', sa.String(255), nullable=True),
        sa.Column('condition', sa.String(255), nullable=True),
        sa.Column('acl_type', sa.String(255), nullable=True),
        sa.Column('operator', sa.String(255), nullable=True),
        sa.Column('match', sa.String(255), nullable=True),
        sa.Column('match_condition', sa.String(255), nullable=True),
        sa.Column('admin_state_up', sa.Boolean(), nullable=False),
        sa.Column('provisioning_status', sa.String(16), nullable=False),
        sa.Column('operating_status', sa.String(16), nullable=False),

        sa.ForeignKeyConstraint(['listener_id'],
                                ['lbaas_listeners.id']),
        sa.UniqueConstraint('listener_id', 'name',
                            name='uniq_resource_to_name'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('lbaas_acls')

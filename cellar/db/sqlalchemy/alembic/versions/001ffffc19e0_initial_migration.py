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

"""initial_migration

Revision ID: 001ffffc19e0
Revises:
Create Date: 2016-10-04 09:52:43.720618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001ffffc19e0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'resources',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(length=36), nullable=True),
        sa.Column('type', sa.String(length=50), nullable=True),
        sa.Column('attributes', sa.Text(), nullable=True),
        sa.Column('foreign_tracking', sa.String(length=36), nullable=True),
        sa.Column('relations', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('uuid', name='uniq_resources0uuid'),
        mysql_ENGINE='InnoDB',
        mysql_DEFAULT_CHARSET='UTF8'
    )

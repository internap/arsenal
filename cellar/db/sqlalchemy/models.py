# -*- encoding: utf-8 -*-
#
# Copyright 2013 Hewlett-Packard Development Company, L.P.
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

"""
SQLAlchemy models for baremetal data.
"""

from oslo_db import options as db_options
from oslo_db.sqlalchemy import models
from oslo_db.sqlalchemy import types as db_types
import six.moves.urllib.parse as urlparse
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import schema, String
from sqlalchemy.ext.declarative import declarative_base
from cellar.conf import CONF

_DEFAULT_SQL_CONNECTION = 'sqlite:///cellar.sqlite'


db_options.set_defaults(CONF, _DEFAULT_SQL_CONNECTION, 'cellar.sqlite')


def table_args():
    engine_name = urlparse.urlparse(CONF.database.connection).scheme
    if engine_name == 'mysql':
        return {'mysql_engine': CONF.database.mysql_engine,
                'mysql_charset': "utf8"}
    return None


class CellarBase(models.TimestampMixin,
                 models.ModelBase):

    metadata = None

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = self[c.name]
        return d


Base = declarative_base(cls=CellarBase)


class Resource(Base):
    """Represents any resource."""

    __tablename__ = 'resources'
    __table_args__ = (
        schema.UniqueConstraint('uuid', name='uniq_resources0uuid'),
        table_args()
    )
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36))
    type = Column(String(36))
    attributes = Column(db_types.JsonEncodedDict)
    foreign_tracking = Column(String(36))
    relations = Column(db_types.JsonEncodedDict)

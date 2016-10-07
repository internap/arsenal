# -*- encoding: utf-8 -*-
#
# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""
Base classes for storage engines
"""

import abc

from oslo_config import cfg
from oslo_db import api as db_api
import six


_BACKEND_MAPPING = {'sqlalchemy': 'cellar.db.sqlalchemy.api'}
IMPL = db_api.DBAPI.from_config(cfg.CONF, backend_mapping=_BACKEND_MAPPING,
                                lazy=True)


def get_instance():
    """Return a DB API instance."""
    return IMPL


@six.add_metaclass(abc.ABCMeta)
class Connection(object):
    """Base class for storage system connections."""

    @abc.abstractmethod
    def __init__(self):
        """Constructor."""

    @abc.abstractmethod
    def create_resource(self, values):
        """Creates a resource

        :param values:
        :return:
        """

    @abc.abstractmethod
    def get_resource_by_uuid(self, uuid):
        """Returns the resource with the matching uuid

        :param uuid:
        :return:
        """

    @abc.abstractmethod
    def get_resource_list(self):
        """Returns all resources

        :return:
        """

    @abc.abstractmethod
    def update_resource(self, id, values):
        """Updates a resource

        :param id:
        :param values:
        :return:
        """

    @abc.abstractmethod
    def delete_resource(self, id):
        """Deletes a resource

        :param id:
        :return:
        """

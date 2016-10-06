# -*- coding: utf-8 -*-

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
from cellar import Model
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class ResourceType(Model):
    def __init__(self, name):
        self.name = name


class ResourceTypeFactory(object):
    def __init__(self):
        self.resource_types = {}

    def register(self, name):
        LOG.info('Registering {} as a new resource type'.format(name))

        if name in self.resource_types:
            raise ResourceTypeAlreadyExist("Resource type already defined: {}".format(name))

        self.resource_types[name] = ResourceType(name)

    def get(self, name):
        if name not in self.resource_types:
            raise UnknownResourceType("Unknown resource type: {}".format(name))

        return self.resource_types[name]

    def list(self):
        return [v for k, v in sorted(self.resource_types.items())]


class UnknownResourceType(Exception):
    pass


class ResourceTypeAlreadyExist(Exception):
    pass

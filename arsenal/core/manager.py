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

import uuid

from arsenal import adapters


class Manager(object):
    def __init__(self, datastore, resource_synchronizer):
        self.datastore = datastore
        self.resource_synchronizer = resource_synchronizer

    def create_resource(self, resource):
        resource.uuid = uuid.uuid4()
        self.datastore.save(resource)
        self.synchronize_resource(resource.uuid)
        return resource

    def list_resources(self):
        return self.datastore.load_all()

    def get_resource(self, resource_uuid):
        try:
            return self.datastore.load(resource_uuid)
        except adapters.ResourceNotFound as e:
            raise ResourceNotFound() from e

    def synchronize_resource(self, resource_uuid):
        resource = self.datastore.load(resource_uuid)
        self.resource_synchronizer.sync_node(resource)
        self.datastore.save(resource)

class ResourceNotFound(Exception):
    pass

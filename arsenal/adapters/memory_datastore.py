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
from arsenal import adapters


class MemoryDatastore(object):

    def __init__(self):
        self.resources = {}

    def save(self, resource):
        self.resources[resource.uuid] = resource

    def load(self, uuid):
        try:
            return self.resources[uuid]
        except KeyError as e:
            raise adapters.ResourceNotFound() from e

    def load_all(self):
        return list(self.resources.values())

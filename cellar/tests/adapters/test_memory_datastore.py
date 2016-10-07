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
from cellar import adapters
from cellar.adapters.memory_datastore import MemoryDatastore
from cellar.core.resource import Resource
from cellar.core.resource_type import ResourceType
from oslotest import base


class TestManager(base.BaseTestCase):
    def setUp(self):
        super().setUp()
        self.datastore = MemoryDatastore()

    def test_save_and_load_a_resource(self):
        resource = Resource("uuid", resource_type=ResourceType('pdu'), attributes={'ironic_driver': 'test'})
        self.datastore.save(resource)

        self.assertEqual(resource, self.datastore.load("uuid"))
        self.assertEqual([resource], self.datastore.load_all())

    def test_resource_not_found(self):
        self.assertRaises(adapters.ResourceNotFound,
                          self.datastore.load, 'something that doesnt exist')

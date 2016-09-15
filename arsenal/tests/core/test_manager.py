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
from arsenal.core.manager import Manager
from arsenal.core.resource import Resource
import mock
from oslotest import base


class TestManager(base.BaseTestCase):
    def setUp(self):
        super().setUp()
        self.datastore = mock.Mock()
        self.manager = Manager(datastore=self.datastore)

    @mock.patch('uuid.uuid4')
    def test_creating_one_resource_returns_it_with_a_uuid_and_saves_it(self, uuid4_mock):
        uuid4_mock.return_value = mock.sentinel.a_uuid
        origin_resource = Resource(uuid=None, ironic_driver='hello')

        created_resource = self.manager.create_resource(origin_resource)

        self.assertEqual(mock.sentinel.a_uuid, created_resource.uuid)
        self.datastore.save.assert_called_with(created_resource)

    def test_fetching_one_resource_returns_it_from_the_datastore(self):
        resource = Resource(uuid=mock.sentinel.a_uuid, ironic_driver='hello')
        self.datastore.load.return_value = resource

        loaded_resource = self.manager.get_resource(mock.sentinel.a_uuid)

        self.assertEqual(resource, loaded_resource)
        self.datastore.load.assert_called_with(mock.sentinel.a_uuid)

    def test_fetching_all_resources_returns_it_from_the_datastore(self):
        resourceA = Resource(uuid=mock.sentinel.a_uuid, ironic_driver='hello')
        resourceB = Resource(uuid=mock.sentinel.another_uuid, ironic_driver='hello')
        self.datastore.load_all.return_value = [resourceA, resourceB]

        loaded_resources = self.manager.list_resources()

        self.assertEqual([resourceA, resourceB], loaded_resources)
        self.datastore.load_all.assert_called_with()

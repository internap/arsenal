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
from arsenal.core import manager
from arsenal.core.manager import Manager, InvalidUpdate
from arsenal.core.resource import Resource
import mock
from oslotest import base


class TestManager(base.BaseTestCase):
    def setUp(self):
        super().setUp()
        self.datastore = mock.Mock()
        self.resource_synchronizer = mock.Mock()
        self.manager = Manager(datastore=self.datastore, resource_synchronizer=self.resource_synchronizer)

    @mock.patch('uuid.uuid4')
    def test_creating_one_resource_returns_it_with_a_uuid_and_saves_it(self, uuid4_mock):
        uuid4_mock.return_value = 'new-uuid'
        origin_resource = Resource(uuid=None, type='switch', attributes={})
        self.manager.synchronize_resource = mock.Mock()

        created_resource = self.manager.create_resource(origin_resource)

        self.assertEqual('new-uuid', created_resource.uuid)
        self.datastore.save.assert_called_with(created_resource)
        self.manager.synchronize_resource.assert_called_with('new-uuid')

    def test_fetching_one_resource_returns_it_from_the_datastore(self):
        resource = Resource(uuid=mock.sentinel.a_uuid, type='firewall', attributes={})
        self.datastore.load.return_value = resource

        loaded_resource = self.manager.get_resource(mock.sentinel.a_uuid)

        self.assertEqual(resource, loaded_resource)
        self.datastore.load.assert_called_with(mock.sentinel.a_uuid)

    def test_fetching_one_resource_not_found(self):
        self.datastore.load.side_effect = adapters.ResourceNotFound

        self.assertRaises(manager.ResourceNotFound, self.manager.get_resource, 'a uuid')

    def test_fetching_all_resources_returns_it_from_the_datastore(self):
        resourceA = Resource(uuid=mock.sentinel.a_uuid, type='', attributes={})
        resourceB = Resource(uuid=mock.sentinel.another_uuid, type='', attributes={})
        self.datastore.load_all.return_value = [resourceA, resourceB]

        loaded_resources = self.manager.list_resources()

        self.assertEqual([resourceA, resourceB], loaded_resources)
        self.datastore.load_all.assert_called_with()

    def test_synchronizing_one_resource_saves_changes_by_the_synchronizer(self):
        origin_resource = Resource(uuid='my-uuid')
        self.datastore.load.return_value = origin_resource
        self.resource_synchronizer.sync_node.side_effect = \
            lambda r: r.foreign_tracking.update({'ironic': 'ironic-uuid'})

        self.manager.synchronize_resource('my-uuid')

        self.resource_synchronizer.sync_node.assert_called_with(origin_resource)
        self.datastore.save.assert_called_with(
            Resource(uuid='my-uuid', foreign_tracking={'ironic': 'ironic-uuid'}))

    def test_update_resource(self):
        origin_resource = Resource(uuid='my-uuid')
        self.datastore.load.return_value = origin_resource

        change = mock.Mock()

        self.manager.update_resource('my-uuid', [change])
        self.datastore.save.assert_called_with(origin_resource)
        self.resource_synchronizer.sync_node.assert_called_with(origin_resource)

    def test_update_resource_fails_if_the_patching_returns_an_error(self):
        origin_resource = Resource(uuid='my-uuid')
        self.datastore.load.return_value = origin_resource

        change = mock.Mock()

        change.apply.side_effect = AttributeError
        self.assertRaises(InvalidUpdate, self.manager.update_resource, 'my-uuid', [change])

        change.apply.side_effect = TypeError
        self.assertRaises(InvalidUpdate, self.manager.update_resource, 'my-uuid', [change])

        change.apply.side_effect = KeyError
        self.assertRaises(InvalidUpdate, self.manager.update_resource, 'my-uuid', [change])

        self.assertFalse(self.datastore.save.called)

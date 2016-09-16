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
from ironicclient.v1.node import Node

from arsenal.drivers.ironic_synchronizer import IronicSynchronizer
from arsenal.core.resource import Resource
from mock import mock
from oslotest import base


class TestIronicSynchronizer(base.BaseTestCase):
    def test_ironic_synchronizer_synchronizes_servers(self):
        ironicclient = mock.Mock()
        ironicclient.node.create.return_value = Node(None, {'uuid': mock.sentinel.ironic_uuid})

        synchronizer = IronicSynchronizer(ironicclient)

        resource = Resource(type='server',
                            attributes=dict(
                                ironic_driver='test',
                                cpu_count=2,
                                cpu_cores=4,
                                ram=2048,
                                disk=480)
                            )
        synchronizer.synchronize(resource)

        ironicclient.node.create.assert_called_with(driver='test',
                                                    properties={'memory_mb': 2048,
                                                                'local_gb': 480,
                                                                'cpus': 8})
        self.assertEqual(mock.sentinel.ironic_uuid, resource.foreign_tracking.get('ironic'))

    def test_ironic_synchronizer_doesnt_synchronizes_any_resource_type(self):
        ironicclient = mock.Mock()
        ironicclient.node.create.return_value = Node(None, {'uuid': mock.sentinel.ironic_uuid})

        synchronizer = IronicSynchronizer(ironicclient)

        resource = Resource(type='pdu',
                            attributes=dict(
                                ironic_driver='test',
                                hostname='pdu.invalid',
                                username='user',
                                password='pass',
                                community='snmp')
                            )
        synchronizer.synchronize(resource)

        self.assertEqual(False, ironicclient.node.create.called)

    def test_ironic_synchronizer_synchronizes_a_node_and_store_its_uuid(self):
        ironicclient = mock.Mock()
        ironicclient.node.create.return_value = Node(None, {'uuid': mock.sentinel.ironic_uuid})

        synchronizer = IronicSynchronizer(ironicclient)

        resource = Resource(type='server',
                            attributes=dict(
                                ironic_driver='test',
                                cpu_count=2,
                                cpu_cores=4,
                                ram=2048,
                                disk=480)
                            )
        synchronizer.synchronize(resource)

        ironicclient.node.create.assert_called_with(driver='test',
                                                    properties={'memory_mb': 2048,
                                                                'local_gb': 480,
                                                                'cpus': 8})
        self.assertEqual(mock.sentinel.ironic_uuid, resource.foreign_tracking.get('ironic'))

    def test_ironic_synchronizer_updates_a_node_when_it_has_a_uuid_already(self):
        ironicclient = mock.Mock()
        ironicclient.node.create.return_value = Node(None, {'uuid': mock.sentinel.ironic_uuid})

        synchronizer = IronicSynchronizer(ironicclient)

        resource = Resource(type='server',
                            attributes=dict(
                                ironic_driver='test',
                                cpu_count=2,
                                cpu_cores=4,
                                ram=2048,
                                disk=480),
                            foreign_tracking=dict(ironic='ironic-uuid'))
        synchronizer.synchronize(resource)

        ironicclient.node.update.assert_called_with('ironic-uuid', [
            {'op': 'add', 'path': '/driver', 'value': 'test'},
            {'op': 'add', 'path': '/properties/memory_mb', 'value': 2048},
            {'op': 'add', 'path': '/properties/local_gb', 'value': 480},
            {'op': 'add', 'path': '/properties/cpus', 'value': 8},
        ])

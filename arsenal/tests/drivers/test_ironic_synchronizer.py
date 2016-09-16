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
    def test_ironic_synchronizer_synchronizes_a_node_and_store_its_uuid(self):
        ironicclient = mock.Mock()
        ironicclient.node.create.return_value = Node(None, {'uuid': mock.sentinel.ironic_uuid})

        synchronizer = IronicSynchronizer(ironicclient)

        resource = Resource(ironic_driver='test')
        synchronizer.sync_node(resource)

        ironicclient.node.create.assert_called_with(driver='test')
        self.assertEqual(mock.sentinel.ironic_uuid, resource.foreign_tracking.get('ironic'))

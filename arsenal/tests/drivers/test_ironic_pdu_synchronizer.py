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

from arsenal.core.resource import Resource
from arsenal.drivers.ironic_pdu_synchronizer import IronicPduSynchronizer
from mock import mock
from oslotest import base


class TestIronicPduSynchronizer(base.BaseTestCase):
    def test_creating_a_pdu(self):
        ironicclient = mock.Mock()
        synchronizer = IronicPduSynchronizer(ironicclient)
        pdu = Resource(type='pdu',
                       attributes=dict(snmp_driver='apc_rackpdu',
                                       snmp_address='127.0.0.1',
                                       snmp_port=1161))

        synchronizer.synchronize(pdu)
        self.assertEqual(False, ironicclient.node.create.called)
        self.assertEqual(False, ironicclient.node.update.called)

    def test_creating_a_pdu_with_a_relation(self):
        ironicclient = mock.Mock()

        synchronizer = IronicPduSynchronizer(ironicclient)

        server = Resource(type='server',
                          foreign_tracking={'ironic': 'bleh'})

        pdu = Resource(type='pdu',
                       attributes=dict(snmp_driver='apc_rackpdu',
                                       snmp_address='127.0.0.1',
                                       snmp_port='1161'),
                       relations={'1': server}
                       )
        synchronizer.synchronize(pdu)

        ironicclient.node.update.assert_called_with('bleh', [
            {'op': 'add', 'path': '/driver_info/snmp_driver',
             'value': 'apc_rackpdu'},
            {'op': 'add', 'path': '/driver_info/snmp_address',
             'value': '127.0.0.1'},
            {'op': 'add', 'path': '/driver_info/snmp_port', 'value': '1161'},
            {'op': 'add', 'path': '/driver_info/snmp_outlet', 'value': '1'},
        ])

    def test_wont_synchronize_a_different_type(self):
        ironicclient = mock.Mock()

        synchronizer = IronicPduSynchronizer(ironicclient)

        resource = Resource(type='server', relations={'1': Resource()})
        synchronizer.synchronize(resource)

        self.assertEqual(False, ironicclient.node.create.called)

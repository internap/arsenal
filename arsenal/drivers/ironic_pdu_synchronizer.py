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

from arsenal.drivers import Synchronizer


class IronicPduSynchronizer(Synchronizer):
    def __init__(self, ironicclient):
        self.ironicclient = ironicclient

    def synchronize(self, resource):
        if resource.type != 'pdu':
            return

        for connector, relation in resource.relations.items():
            ironic_node_uuid = relation.foreign_tracking['ironic']

            self.ironicclient.node.update(ironic_node_uuid, [
                {'op': 'add', 'path': '/driver_info/snmp_driver', 'value': resource.attributes['snmp_driver']},
                {'op': 'add', 'path': '/driver_info/snmp_address', 'value': resource.attributes['snmp_address']},
                {'op': 'add', 'path': '/driver_info/snmp_port', 'value': resource.attributes['snmp_port']},
                {'op': 'add', 'path': '/driver_info/snmp_outlet', 'value': connector},
            ])

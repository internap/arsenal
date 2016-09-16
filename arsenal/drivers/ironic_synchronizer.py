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


class IronicSynchronizer(object):
    def __init__(self, ironicclient):
        self.ironicclient = ironicclient

    def sync_node(self, resource):
        if 'server' not in resource.type:
            return

        ironic_node = self.ironicclient.node.create(
            driver=resource.attributes['ironic_driver'],
            properties={'memory_mb': resource.attributes['ram'],
                        'local_gb': resource.attributes['disk'],
                        'cpus': resource.attributes['cpu_count'] * resource.attributes['cpu_cores']})
        resource.foreign_tracking['ironic'] = ironic_node.uuid

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

from arsenal.ironic_synchronizer import IronicSynchronizer
from arsenal.resource import Resource
from arsenal.tests import base
from mock import mock


class TestIronicSynchronizer(base.TestCase):
    def test_ironic_synchronizer_synchronizes_a_node(self):
        ironicclient = mock.Mock()
        synchronizer = IronicSynchronizer(ironicclient)

        resource = Resource(ironic_driver='test')
        synchronizer.sync_node(resource)

        ironicclient.node.create.assert_called_with(driver='test')

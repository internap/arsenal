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

from arsenal.core.shipper import Shipper
from mock import Mock, sentinel, call
from oslotest import base


class TestShipper(base.BaseTestCase):
    def setUp(self):
        super().setUp()

        self.datasource = Mock()
        self.synchronizer = Mock()
        self.shipper = Shipper(self.datasource, self.synchronizer)

    def test_can_ship_one_resource(self):
        self.datasource.get_resources.return_value = [sentinel.shizzle]

        self.shipper.ship()

        self.synchronizer.synchronize.assert_called_with(sentinel.shizzle)

    def test_can_ship_several_resources(self):
        self.datasource.get_resources.return_value = [sentinel.resource1,
                                                      sentinel.resource2,
                                                      sentinel.resource3]

        self.shipper.ship()

        self.synchronizer.synchronize.assert_has_calls([
            call(sentinel.resource1),
            call(sentinel.resource2),
            call(sentinel.resource3),
        ])

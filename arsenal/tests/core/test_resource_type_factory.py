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
from arsenal.core.resource_type import ResourceTypeFactory, ResourceTypeAlreadyExist, UnknownResourceType
from oslotest import base


class TestResourceTypeFactory(base.BaseTestCase):
    def setUp(self):
        super().setUp()

        self.factory = ResourceTypeFactory()

    def test_register_and_obtain_a_type(self):
        self.factory.register("resource_type_name")

        resource_type = self.factory.get("resource_type_name")

        self.assertEqual("resource_type_name", resource_type.name)

    def test_an_unknown_type_raises(self):
        self.assertRaises(UnknownResourceType, self.factory.get, "unknown_type")

    def test_registering_the_same_resource_type_twice_raises(self):
        self.factory.register("resource_type_name")

        self.assertRaises(ResourceTypeAlreadyExist, self.factory.register, "resource_type_name")

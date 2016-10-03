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
import tempfile
import textwrap

from cellar.adapters.resource_type_yaml_parser import ResourceTypeYamlParser
from cellar.core.resource_type import ResourceTypeFactory
from oslotest import base


class TestResourceTypeYamlParser(base.BaseTestCase):
    def setUp(self):
        super().setUp()
        self.factory = ResourceTypeFactory()
        self.parser = ResourceTypeYamlParser(self.factory)

    def test_read_some_types(self):
        with tempfile.NamedTemporaryFile("w") as tempf:
            with open(tempf.name, 'w') as f:
                f.write(textwrap.dedent("""
                    resource-types:
                        server:
                        switch:
                """))

            self.parser.configure_factory_from(tempf.name)

        self.assertEqual("server", self.factory.get("server").name)
        self.assertEqual("switch", self.factory.get("switch").name)

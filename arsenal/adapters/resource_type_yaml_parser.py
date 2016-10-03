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

import yaml


class ResourceTypeYamlParser(object):

    def __init__(self, resource_type_factory):
        self.resource_type_factory = resource_type_factory

    def configure_factory_from(self, filename):
        with open(filename) as f:
            file_content = f.read()
            content = yaml.load(file_content)

            for name, specs in content["resource-types"].items():
                self.resource_type_factory.register(name)

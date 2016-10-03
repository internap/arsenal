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

import sys

from cellar.adapters.memory_datastore import MemoryDatastore
from cellar.adapters.resource_type_yaml_parser import ResourceTypeYamlParser
from cellar.core.manager import Manager
from cellar.core.resource_type import ResourceTypeFactory
from cellar.interfaces.api import Api
from flask import Flask
from ironicclient import client
from lazy_object_proxy import Proxy
from oslo_config import cfg

cfg.CONF.register_opts([
    cfg.StrOpt('type_definition_file', default="cellar.conf",
               help="The type definition file to use"),
])


def make_ironicclient():
    return client.get_client(
        "1",
        os_username="admin",
        os_password="password",
        os_tenant_name="admin",
        os_auth_url="http://172.27.59.42:5000/v2.0/",
        os_region_name="RegionOne"
    )

ironicclient = Proxy(make_ironicclient)


def wire_stuff(app):
    resource_type_factory = ResourceTypeFactory()

    resource_type_yaml_parser = ResourceTypeYamlParser(resource_type_factory)
    resource_type_yaml_parser.configure_factory_from(cfg.CONF.find_file(cfg.CONF.type_definition_file))

    datastore = MemoryDatastore()
    Api(app,
        manager=Manager(datastore, []),
        resource_type_factory=resource_type_factory)


def get_app():
    app = Flask(__name__)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    return app


app = get_app()


def run():
    cfg.CONF.register_cli_opt(cfg.IntOpt('port', metavar='PORT', short='p', help="Port to run on"))
    cfg.CONF(sys.argv[1:])

    wire_stuff(app)
    app.run(port=cfg.CONF.port)


if __name__ == "__main__":
    app.run()

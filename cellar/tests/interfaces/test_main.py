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
import json
import os
import random
import subprocess
import sys

import requests
import requests.exceptions
from cellar.tests import ROOT_DIR
from decorator import contextmanager
from oslotest import base
from retry.api import retry_call


class TestMain(base.BaseTestCase):
    def test_types_are_loaded_from_configured_types_file(self):
        with app_running("cellar.test.conf") as base_url:
            result = requests.get("{}/v1/resource-types".format(base_url))

            self.assertEqual(200, result.status_code)
            self.assertEqual({
                "resource_types": [
                    {"name": "server"},
                    {"name": "switch"}
                ]
            }, result.json())

    def test_can_save_resources_in_configured_datastore(self):
        with app_running("cellar.test.conf") as base_url:
            result = requests.post("{}/v1/resources".format(base_url),
                                   headers={"content-type": "application/json"},
                                   data=json.dumps({
                                       'type': 'server',
                                       'attributes': {}
                                   }))
            created_uuid = result.json()["uuid"]

            result = requests.get("{}/v1/resources/{}".format(base_url, created_uuid))
            fetched_uuid = result.json()["uuid"]

            self.assertEqual(created_uuid, fetched_uuid)


@contextmanager
def app_running(config_file):
    port = random.randint(30000, 60000)
    env = os.environ.copy()
    p = subprocess.Popen([sys.executable,
                          _get_entry_point_path('cellar'),
                          '--port',
                          str(port),
                          '--config-file',
                          os.path.join(ROOT_DIR, config_file)
                          ],
                         env=env, cwd=ROOT_DIR)

    base_url = _wait_until_app_is_ready(port)

    try:
        yield base_url
    finally:
        p.kill()


def _wait_until_app_is_ready(port):
    base_url = "http://localhost:{}".format(port)
    retry_call(requests.get, fargs=[base_url], tries=50, delay=0.1,
               exceptions=requests.exceptions.ConnectionError)
    return base_url


def _get_entry_point_path(entry_point):
    return os.path.join(os.path.dirname(sys.executable), entry_point)

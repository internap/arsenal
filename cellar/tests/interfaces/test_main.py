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

    def test_application_is_starting(self):
        with app_running("cellar.test.conf") as port:
            def test():
                r = requests.get("http://localhost:{}/v1/resource-types".format(port))
                self.assertEqual(200, r.status_code)
                return r

            result = retry_call(test, tries=50, delay=0.1,
                                exceptions=requests.exceptions.ConnectionError)

            self.assertEqual({
                "resource_types": [
                    {"name": "server"},
                    {"name": "switch"}
                ]
            }, result.json())


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

    try:
        yield port
    finally:
        p.kill()


def _get_entry_point_path(entry_point):
    return os.path.join(os.path.dirname(sys.executable), entry_point)

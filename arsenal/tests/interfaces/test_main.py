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

import subprocess
import unittest

import sys

import os
import random
import requests
import requests.exceptions
from decorator import contextmanager
from oslotest import base
from retry.api import retry_call


@unittest.skip
class TestMain(base.BaseTestCase):

    def test_application_is_starting(self):
        with app_running() as port:
            def test():
                r = requests.get("http://localhost:{}".format(port))
                self.assertEqual(404, r.status_code)

            retry_call(test, tries=50, delay=0.1,
                       exceptions=requests.exceptions.ConnectionError)

    def test_application_serving_the_api(self):
        with app_running() as port:
            def test():
                r = requests.post("http://localhost:{}/v1/resources".format(port))
                self.assertEqual(500, r.status_code)

            retry_call(test, tries=50, delay=0.1,
                       exceptions=requests.exceptions.ConnectionError)


@contextmanager
def app_running():
    port = random.randint(30000, 60000)
    env = os.environ.copy()
    env.update(dict(
        FLASK_APP="arsenal.interfaces.main:app"
    ))
    p = subprocess.Popen([sys.executable,
                          _get_entry_point_path('flask'),
                          'run',
                          '--port',
                          str(port)],
                         env=env)

    try:
        yield port
    finally:
        p.kill()


def _get_entry_point_path(entry_point):
    return os.path.join(os.path.dirname(sys.executable), entry_point)

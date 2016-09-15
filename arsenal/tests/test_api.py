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

from arsenal.api import Api
from arsenal.kiwi import Kiwi
from arsenal.tests import base
from flask import Flask
from mock import mock


class TestAPI(base.TestCase):
    def setUp(self):
        super().setUp()
        self.app = Flask("test")
        self.manager = mock.Mock()
        Api(self.app, manager=self.manager)

    def test_creating_a_kiwi(self):
        with self.app.test_client() as http_client:
            result = http_client.post("/kiwis", headers={"content-type": "application/json"}, data=json.dumps({
                'ironic_driver': 'hello'
            }))
            self.assertEqual(201, result.status_code)
            self.assertIn('Location', result.headers)
            self.assertIn('/kiwis/', result.headers['Location'])

            self.manager.create_kiwi.assert_called_with(Kiwi(uuid=None, ironic_driver='hello'))

    def test_fetching_a_kiwi(self):
        with self.app.test_client() as http_client:
            uuid = "cecc2a85-3d6b-461c-a8f3-f4a370f3b10c"

            self.manager.get_kiwi.return_value = Kiwi(ironic_driver='wow',
                                                      uuid=uuid)

            result = http_client.get("/kiwis/{}".format(uuid),
                                     headers={"content-type": "application/json"})
            self.assertEqual(200, result.status_code)
            self.assertEqual('application/json', result.content_type)
            self.assertEqual({'uuid': uuid, 'ironic_driver': 'wow'},
                             json.loads(result.data.decode(result.charset)))


            self.manager.get_kiwi.assert_called_with('%s' % uuid)


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

from arsenal.core.manager import ResourceNotFound, InvalidUpdate
from arsenal.core.patch import Replace
from arsenal.core.resource import Resource
from arsenal.core.resource_type import ResourceTypeFactory
from arsenal.interfaces.api import Api
from arsenal.interfaces.main import get_app
from mock import mock
from oslotest import base

API_ROOT = "/v1"

json_content_type = {"content-type": "application/json"}


class TestAPI(base.BaseTestCase):
    def setUp(self):
        super().setUp()
        self.manager = mock.Mock()
        self.resource_type_factory = ResourceTypeFactory()
        self.app = get_app()
        Api(self.app, manager=self.manager, resource_type_factory=self.resource_type_factory)

    def test_creating_a_resource_returns_a_location(self):
        with self.app.test_client() as http_client:
            resource = Resource(uuid='some-uuid', type='server',
                                attributes={'ironic_driver': 'hello'},
                                relations={
                                    "port1": Resource("uuid1"),
                                    "port2": Resource("uuid2"),
                                })
            self.manager.create_resource.return_value = resource

            self.manager.get_resource.side_effect = lambda uuid: Resource(uuid)

            result = http_client.post("{}/resources".format(API_ROOT),
                                      headers=json_content_type,
                                      data=json.dumps({
                                          'type': 'server',
                                          'attributes': {'ironic_driver': 'hello'},
                                          'relations': {
                                              "port1": "uuid1",
                                              "port2": "uuid2",
                                          }
                                      }))
            self.assertEqual(201, result.status_code)
            self.assertEqual('application/json', result.headers['Content-Type'])

            self.assertDictEqual(
                json.loads(result.data.decode(result.charset)),
                {
                    "uuid": "some-uuid",
                    "type": "server",
                    "attributes": {"ironic_driver": "hello"},
                    "relations": {
                        "port1": "uuid1",
                        "port2": "uuid2",
                    }
                }
            )
            self.assertIn('Location', result.headers)
            self.assertIn('{}/resources/some-uuid'.format(API_ROOT),
                          result.headers['Location'])

            self.manager.create_resource.assert_called_with(
                Resource(uuid=None,
                         type='server',
                         attributes={'ironic_driver': 'hello'},
                         relations={
                             "port1": Resource("uuid1"),
                             "port2": Resource("uuid2"),
                         }))

    def test_fetching_a_resource(self):
        with self.app.test_client() as http_client:
            uuid = "cecc2a85-3d6b-461c-a8f3-f4a370f3b10c"

            self.manager.get_resource.return_value = Resource(
                uuid=uuid,
                type='server',
                attributes=dict(ironic_driver='wow'),
                relations={
                    "port1": Resource("uuid1"),
                    "port2": Resource("uuid2"),
                }
            )

            result = http_client.get("{}/resources/{}".format(API_ROOT, uuid),
                                     headers=json_content_type)
            self.assertEqual(200, result.status_code)
            self.assertEqual('application/json', result.content_type)
            self.assertEqual({
                'uuid': uuid,
                'type': 'server',
                'attributes': {'ironic_driver': 'wow'},
                'relations': {
                    "port1": "uuid1",
                    "port2": "uuid2",
                }}, json.loads(result.data.decode(result.charset)))

            self.manager.get_resource.assert_called_with('%s' % uuid)

    def test_fetching_a_resource_404_does_not_exist(self):
        with self.app.test_client() as http_client:
            uuid = "cecc2a85-3d6b-461c-a8f3-f4a370f3b10c"

            self.manager.get_resource.side_effect = ResourceNotFound

            result = http_client.get("{}/resources/{}".format(API_ROOT, uuid),
                                     headers=json_content_type)
            self.assertEqual(404, result.status_code)

    def test_fetch_all_resources_empty_list(self):
        with self.app.test_client() as http_client:
            self.manager.list_resources.return_value = []

            result = http_client.get("{}/resources".format(API_ROOT),
                                     headers=json_content_type)
            self.assertEqual(200, result.status_code)
            self.assertEqual('application/json', result.content_type)
            self.assertEqual({"resources": []}, json.loads(result.data.decode(result.charset)))

    def test_fetch_all_resources_two_items(self):
        with self.app.test_client() as http_client:
            self.manager.list_resources.return_value = [
                Resource(uuid='14', type='server', attributes=dict(ironic_driver='yes')),
                Resource(uuid='15', type='server', attributes=dict(ironic_driver='no'),
                         relations={"port1": Resource("uuid1")})
            ]

            result = http_client.get("{}/resources/".format(API_ROOT),
                                     headers=json_content_type)
            self.assertEqual(200, result.status_code)
            self.assertEqual('application/json', result.content_type)
            self.assertEqual({"resources": [
                {
                    'uuid': '14',
                    'type': 'server',
                    'attributes': {'ironic_driver': 'yes'},
                    'relations': {}
                },
                {
                    'uuid': '15',
                    'type': 'server',
                    'attributes': {'ironic_driver': 'no'},
                    'relations': {"port1": "uuid1"}
                }
            ]}, json.loads(result.data.decode(result.charset)))

    def test_updating_a_resource_returns_the_updated_resource(self):
        with self.app.test_client() as http_client:
            resource = Resource(uuid='some-uuid',
                                type='',
                                attributes={'ironic_driver': 'changed'})

            self.manager.update_resource.return_value = resource

            result = http_client.patch(
                "{}/resources/some-uuid".format(API_ROOT),
                headers=json_content_type,
                data=json.dumps(
                    [{"value": "changed",
                      "path": "/attributes/ironic_driver",
                      "op": "replace"}
                     ]
                )
            )

            self.assertEqual(200, result.status_code)
            self.assertEqual('application/json', result.headers['Content-Type'])
            self.assertDictEqual(
                json.loads(result.data.decode(result.charset)),
                {
                    "uuid": "some-uuid",
                    "type": "",
                    "attributes": {"ironic_driver": "changed"},
                    "relations": {}
                }
            )
            self.assertIn('Location', result.headers)
            self.assertIn('{}/resources/some-uuid'.format(API_ROOT),
                          result.headers['Location'])

            self.manager.update_resource.assert_called_with(
                'some-uuid',
                changes=[
                    Replace(["attributes", "ironic_driver"], "changed")
                ]
            )

    def test_updating_a_resource_with_an_unknown_attribute_says_bad_request(self):
        with self.app.test_client() as http_client:
            self.manager.update_resource.side_effect = InvalidUpdate

            result = http_client.patch(
                "{}/resources/some-uuid".format(API_ROOT),
                headers=json_content_type,
                data=json.dumps(
                    [{"value": "changed",
                      "path": "/attributes/trololololo",
                      "op": "replace"}
                     ]
                )
            )

            self.assertEqual(400, result.status_code)

    def test_listing_all_supported_resource_types(self):
        self.resource_type_factory.register("resource_type_A")
        self.resource_type_factory.register("resource_type_B")

        with self.app.test_client() as http_client:
            result = http_client.get("{}/resource-types".format(API_ROOT))

        self.assertEqual(200, result.status_code)
        self.assertEqual({
            "resource_types": [
                {"name": "resource_type_A"},
                {"name": "resource_type_B"}
            ]
        }, json.loads(result.data.decode(result.charset)))

    def test_fetch_all_accept_html(self):
        with self.app.test_client() as http_client:
            self.manager.list_resources.return_value = [
                Resource(uuid='14', attributes=dict(ironic_driver='yes')),
                Resource(uuid='15', attributes=dict(ironic_driver='no'))
            ]

            result = http_client.get("{}/resources".format(API_ROOT),
                                     headers={'Accept': 'text/html'})

            self.assertEqual(200, result.status_code)
            self.assertIn('text/html', result.content_type)

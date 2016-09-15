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

from arsenal.core.resource import Resource
from flask import make_response
from flask import request


class Api(object):
    def __init__(self, app, manager=None):
        super().__init__()

        self.manager = manager

        app.add_url_rule('/v1/resources',
                         view_func=self.create_resource,
                         methods=['POST'])

        app.add_url_rule('/v1/resources',
                         view_func=self.get_all_resources,
                         methods=['GET'])

        app.add_url_rule('/v1/resources/<uuid>',
                         view_func=self.get_resource,
                         methods=['GET'])

    def create_resource(self):
        response = make_response('', 201)
        request_data = request.json

        resource = self.manager.create_resource(
            Resource(ironic_driver=request_data['ironic_driver']))
        response.headers['Location'] = '/v1/resources/{}'.format(resource.uuid)

        return response

    def get_all_resources(self):
        resources = self.manager.list_resources()

        api_response = []
        for resource in resources:
            api_response.append(resource_to_api(resource))

        response = make_response(json.dumps(api_response), 200)
        response.headers['Content-Type'] = 'application/json'

        return response

    def get_resource(self, uuid):
        resource = self.manager.get_resource(uuid)

        data = resource_to_api(resource)

        response = make_response(json.dumps(data), 200)
        response.headers['Content-Type'] = 'application/json'

        return response


def resource_to_api(resource):
    data = {'ironic_driver': resource.ironic_driver,
            'uuid': resource.uuid}
    return data

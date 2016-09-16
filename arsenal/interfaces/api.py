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
from arsenal.core.patch import Replace, Create, Remove
from arsenal.core.resource import Resource
from flask import make_response
from flask import request
from flask import render_template


class Api(object):
    def __init__(self, app, manager=None):
        super().__init__()

        self.manager = manager

        app.add_url_rule('/v1/resources',
                         view_func=self.create_resource,
                         methods=['POST'])

        app.add_url_rule('/v1/resources/<uuid>',
                         view_func=self.update_resource,
                         methods=['PATCH'])

        app.add_url_rule('/v1/resources',
                         view_func=self.get_all_resources,
                         methods=['GET'])

        app.add_url_rule('/v1/resources/<uuid>',
                         view_func=self.get_resource,
                         methods=['GET'])

    def create_resource(self):
        request_data = request.json

        resource = self.manager.create_resource(
            Resource(type=request_data['type'],
                     attributes=request_data['attributes']))
        response = make_response(json.dumps(resource_to_api(resource)), 201)
        response.headers['Location'] = '/v1/resources/{}'.format(resource.uuid)

        return response

    def update_resource(self, uuid):
        request_data = request.json
        changes = request_to_patch_operation(request_data)

        try:
            resource = self.manager.update_resource(uuid, changes=changes)
        except InvalidUpdate:
            return make_response('', 400)

        response = make_response(json.dumps(resource_to_api(resource)), 201)
        response.headers['Location'] = '/v1/resources/{}'.format(resource.uuid)

        return response

    def get_all_resources(self):
        resources = self.manager.list_resources()

        if 'text/html' in request.accept_mimetypes:
            response = make_response('', 200)
            response.headers['Content-Type'] = 'text/html'
            return render_template('resources.html', resources=resources)
        else:
            api_response = []
            for resource in resources:
                api_response.append(resource_to_api(resource))

            response = make_response(json.dumps({"resources": api_response}), 200)
            response.headers['Content-Type'] = 'application/json'

            return response

    def get_resource(self, uuid):
        try:
            resource = self.manager.get_resource(uuid)
        except ResourceNotFound:
            return make_response('', 404)

        data = resource_to_api(resource)

        response = make_response(json.dumps(data), 200)
        response.headers['Content-Type'] = 'application/json'

        return response


def request_to_patch_operation(request):
    patch_operations = {
        'replace': Replace,
        'add': Create,
        'remove': Remove
    }
    return [patch_operations.get(change['op'])(change['path'].split('/')[1:], change['value']) for change in request]


def resource_to_api(resource):
    return {'uuid': resource.uuid,
            'type': resource.type,
            'attributes': resource.attributes}

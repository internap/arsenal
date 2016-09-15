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

from arsenal.kiwi import Kiwi
from flask import make_response
from flask import request

class Api(object):
    def __init__(self, app, manager=None):
        super().__init__()

        self.manager = manager

        app.add_url_rule('/kiwis', view_func=self.create_kiwi, methods=['POST'])
        app.add_url_rule('/kiwis/<uuid>', view_func=self.get_kiwi, methods=['GET'])

    def create_kiwi(self):
        response = make_response('', 201)
        response.headers['Location'] = '/kiwis/'
        request_data = request.json

        self.manager.create_kiwi(Kiwi(ironic_driver=request_data['ironic_driver']))
        return response

    def get_kiwi(self, uuid):
        kiwi = self.manager.get_kiwi(uuid)

        data = {'ironic_driver': kiwi.ironic_driver,
                'uuid': kiwi.uuid}

        response = make_response(json.dumps(data), 200)
        response.headers['Content-Type'] = 'application/json'

        return response

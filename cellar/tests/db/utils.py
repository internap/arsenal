#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from cellar.db import api as db_api


def get_test_resource(**kw):
    attributes = {
        "cpu_arch": "x86_64",
        "cpus": "8",
        "local_gb": "10",
        "memory_mb": "4096",
    }
    return {
        'id': kw.get('id', 123),
        'uuid': kw.get('uuid', '136dd5db-efed-4b2b-bbe5-55da154e2b0c'),
        'type': kw.get('type', 'server'),
        'attributes': kw.get('attributes', attributes),
        'foreign_tracking': kw.get('foreign_tracking',
                                   'ffc8027f-b271-4f8e-859e-0391ec61a4ef'),
        'relations': kw.get('relations', {})
    }


def create_test_resource(**kw):
    res = get_test_resource(**kw)
    # Let DB generate ID if it isn't specified explicitly
    if 'id' not in kw:
        del res['id']

    dbapi = db_api.get_instance()
    return dbapi.create_resource(res)

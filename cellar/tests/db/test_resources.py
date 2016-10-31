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
import uuid

from cellar.common import exception
from cellar.core.resource import Resource
from cellar.tests.db import base
from cellar.tests.db import utils


class DbResourceTestCase(base.DbTestCase):
    def test_create_test_resource(self):
        utils.create_test_resource(id=123)

    def test_create_resource_already_exists(self):
        utils.create_test_resource(id=123)
        self.assertRaises(exception.ResourceAlreadyExists,
                          utils.create_test_resource, id=123)

    def test_get_resource(self):
        utils.create_test_resource(id=123, uuid=self._uuidgen())
        expected = utils.create_test_resource(id=234,
                                              uuid=self._uuidgen())
        actual = self.dbapi.get_resource_by_uuid(expected.uuid)
        self.assertEqual(expected.uuid, actual.uuid)

    def test_resource_that_does_not_exists(self):
        self.assertRaises(exception.ResourceNotFound,
                          self.dbapi.get_resource_by_uuid,
                          uuid=self._uuidgen())

    def test_resource_list(self):
        utils.create_test_resource(id=123, uuid=self._uuidgen())
        utils.create_test_resource(id=234, uuid=self._uuidgen())
        resources = self.dbapi.get_resource_list()
        self.assertEqual(2, len(resources))

    def test_update_resource(self):
        res = utils.create_test_resource(id=123, uuid=self._uuidgen())
        expected_ft = self._uuidgen()
        self.dbapi.update_resource(res.id, {'foreign_tracking': expected_ft})
        actual_res = self.dbapi.get_resource_by_uuid(uuid=res.uuid)
        self.assertEqual(expected_ft, actual_res.foreign_tracking)

    def test_update_resource_that_does_not_exists(self):
        res = Resource()
        res.id = 123
        expected_ft = self._uuidgen()
        self.assertRaises(exception.ResourceNotFound,
                          self.dbapi.update_resource,
                          res.id, {'foreign_tracking': expected_ft})

    def test_delete_resource(self):
        res = utils.create_test_resource(
            uuid=self._uuidgen())
        self.dbapi.delete_resource(res.id)

    def test_delete_resource_that_does_not_exists(self):
        res = Resource()
        res.id = 123
        self.assertRaises(exception.ResourceNotFound,
                          self.dbapi.delete_resource, res.id)

    def _uuidgen(self):
        return str(uuid.uuid4())

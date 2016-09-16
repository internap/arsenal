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
from arsenal.core.patch import Create, Replace, Remove
from arsenal.core.resource import Resource
from oslotest import base


class TestCreate(base.BaseTestCase):
    def setUp(self):
        super().setUp()
        self.resource = Resource(
            uuid='1234', attributes={'one': {
                'one-one': {}, 'one-two': {'one-two-tree': ''}}},
            foreign_tracking={}
        )

    def test_adding_to_existent_dictionary(self):
        operation = Create(['attributes', 'one', 'one-one', 'new-field'], 'my-value')

        operation.apply(self.resource)

        self.assertEqual(Resource(
            uuid='1234', attributes={'one': {
                'one-one': {'new-field': 'my-value'},
                'one-two': {'one-two-tree': ''}}},
            foreign_tracking={}
        ), self.resource)

    def test_adding_to_new_dictionary(self):
        operation = Create(['foreign_tracking', 'one', 'one-tree', 'one-tree-one', 'new-field'], 'my-value')

        operation.apply(self.resource)

        self.assertEqual(Resource(
            uuid='1234', attributes={'one': {
                'one-one': {}, 'one-two': {'one-two-tree': ''}}},
            foreign_tracking={'one': {'one-tree': {
                'one-tree-one': {'new-field': 'my-value'}}}}
        ), self.resource)

    def test_adding_from_invalid_attribute_fails(self):
        operation = Create(['invalid', 'one', 'one-tree', 'one-tree-one', 'new-field'], 'my-value')

        self.assertRaises(AttributeError, operation.apply, self.resource)


class TestUpdate(base.BaseTestCase):
    def setUp(self):
        super().setUp()
        self.resource = Resource(
            uuid='1234', attributes={'one': {
                'one-one': {}, 'one-two': {'one-two-tree': ''}}},
            foreign_tracking={}
        )

    def test_replacing_to_existent_dictionary(self):
        operation = Replace(['attributes', 'one', 'one-one', 'new-field'], 'my-value')

        operation.apply(self.resource)

        self.assertEqual(Resource(
            uuid='1234', attributes={'one': {
                'one-one': {'new-field': 'my-value'},
                'one-two': {'one-two-tree': ''}}},
            foreign_tracking={}
        ), self.resource)

    def test_replacing_to_new_dictionary_fails(self):
        operation = Replace(['foreign_tracking', 'one', 'one-tree', 'one-tree-one', 'new-field'], 'my-value')

        self.assertRaises(KeyError, operation.apply, self.resource)

    def test_adding_from_invalid_attribute_fails(self):
        operation = Replace(['invalid', 'one', 'one-tree', 'one-tree-one', 'new-field'], 'my-value')

        self.assertRaises(AttributeError, operation.apply, self.resource)


class TestRemove(base.BaseTestCase):
    def setUp(self):
        super().setUp()
        self.resource = Resource(
            uuid='1234', attributes={'one': {
                'one-one': {}, 'one-two': {'one-two-tree': ''}}},
            foreign_tracking={}
        )

    def test_removing_an_existent_dictionary(self):
        operation = Remove(['attributes', 'one', 'one-two'])

        operation.apply(self.resource)

        self.assertEqual(Resource(
            uuid='1234', attributes={'one': {
                'one-one': {}}},
            foreign_tracking={}
        ), self.resource)

    def test_removing_from_an_existent_dictionary(self):
        operation = Remove(['attributes', 'one', 'one-two', 'one-two-tree'])

        operation.apply(self.resource)

        self.assertEqual(Resource(
            uuid='1234', attributes={'one': {
                'one-one': {}, 'one-two': {}}},
            foreign_tracking={}
        ), self.resource)

    def test_removing_from_an_inexistent_path_fails(self):
        operation = Remove(['attributes', 'four', 'four-two'])

        self.assertRaises(KeyError, operation.apply, self.resource)

    def test_removing_an_attribute_fails(self):
        operation = Remove(['foreign_tracking'])

        self.assertRaises(TypeError, operation.apply, self.resource)

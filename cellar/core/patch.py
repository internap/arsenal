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
from cellar import Model


class Operation(Model):
    def __init__(self, path, value=None):
        self.path = path
        self.value = value

    def apply(self, model):
        pass


class Create(Operation):
    def apply(self, model):
        base = _get_base(self.path[:-1], model, create=True)
        field = self.path[-1]
        if isinstance(base, dict):
            base[field] = self.value
        else:
            setattr(base, field, self.value)


class Replace(Operation):
    def apply(self, model):
        base = _get_base(self.path[:-1], model, create=False)
        field = self.path[-1]
        if isinstance(base, dict):
            base[field] = self.value
        else:
            setattr(base, field, self.value)


class Remove(Operation):
    def apply(self, model):
        base = _get_base(self.path[:-1], model, create=False)
        field = self.path[-1]
        del base[field]


def _get_base(path, base, create=False):
    for field in path:
        if isinstance(base, dict):
            if create:
                base = base.setdefault(field, {})
            else:
                base = base[field]
        else:
            base = getattr(base, field)
    return base

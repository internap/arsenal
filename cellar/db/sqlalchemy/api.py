# -*- encoding: utf-8 -*-
#
# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
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

"""SQLAlchemy storage backend."""

import threading

from cellar.common import exception
from oslo_config import cfg
from oslo_db import exception as db_exc
from oslo_db.sqlalchemy import enginefacade
from oslo_db.sqlalchemy import utils as db_utils
from oslo_utils import strutils
from oslo_utils import uuidutils
from cellar.db import api
from cellar.db.sqlalchemy import models
from sqlalchemy.orm.exc import NoResultFound

CONF = cfg.CONF

_CONTEXT = threading.local()


def get_backend():
    """The backend is this module itself."""
    return Connection()


def _session_for_read():
    return enginefacade.reader.using(_CONTEXT)


def _session_for_write():
    return enginefacade.writer.using(_CONTEXT)


def model_query(model, *args, **kwargs):
    """Query helper for simpler session usage.

    :param session: if present, the session to use
    """

    with _session_for_read() as session:
        query = session.query(model, *args)
        return query


def _paginate_query(model, limit=None, marker=None, sort_key=None,
                    sort_dir=None, query=None):

    if not query:
        query = model_query(model)
    sort_keys = ['id']
    if sort_key and sort_key not in sort_keys:
        sort_keys.insert(0, sort_key)
    try:
        query = db_utils.paginate_query(query, model, limit, sort_keys,
                                        marker=marker, sort_dir=sort_dir)
    except db_exc.InvalidSortKey:
        raise exception.InvalidParameterValue(
            _('The sort_key value "%(key)s" is an invalid field for sorting')
            % {'key': sort_key})
    return query.all()


def add_identity_filter(query, value):
    """Adds an identity filter to a query.

    Filters results by ID, if supplied value is a valid integer.
    Otherwise attempts to filter results by UUID.

    :param query: Initial query to add filter to.
    :param value: Value for filtering results by.
    :return: Modified query.
    """
    if strutils.is_int_like(value):
        return query.filter_by(id=value)
    elif uuidutils.is_uuid_like(value):
        return query.filter_by(uuid=value)
    else:
        raise exception.InvalidIdentity()


class Connection(api.Connection):
    """SqlAlchemy connection."""

    def __init__(self):
        pass

    def model_query(model, *args, **kwargs):
        """Query helper for simpler session usage.

        :param session: if present, the session to use
        """

        with _session_for_read() as session:
            query = session.query(model, *args)
            return query

    def create_resource(self, values):
        if 'uuid' not in values:
            values['uuid'] = uuidutils.generate_uuid()
        if 'type' not in values:
            values[type] = ''
        if 'attributes' not in values:
            values['attributes'] = {}
        if 'foreign_tracking' not in values:
            values['foreign_tracking'] = ''
        if 'relations' not in values:
            values['relations'] = {}

        res = models.Resource()
        res.update(values)
        with _session_for_write() as session:
            try:
                session.add(res)
                session.flush()
            except db_exc.DBDuplicateEntry:
                raise exception.ResourceAlreadyExists()
            return res

    def get_resource_by_uuid(self, uuid):
        query = model_query(models.Resource)
        query = add_identity_filter(query, uuid)
        try:
            return query.one()
        except NoResultFound:
            raise exception.ResourceNotFound()

    def get_resource_list(self):
        query = model_query(models.Resource)
        try:
            return query.all()
        except NoResultFound:
            raise exception.ResourceNotFound

    def update_resource(self, id, values):
        if 'uuid' in values:
            raise exception.InvalidParameterValue()

        with _session_for_write():
            query = model_query(models.Resource)
            query = add_identity_filter(query, id)

            try:
                ref = query.with_lockmode('update').one()
            except Exception:
                raise exception.ResourceNotFound()

            ref.update(values)
        return ref

    def delete_resource(self, id):
        with _session_for_write():
            query = model_query(models.Resource)
            query = add_identity_filter(query, id)
            count = query.delete()
            if count == 0:
                raise exception.ResourceNotFound

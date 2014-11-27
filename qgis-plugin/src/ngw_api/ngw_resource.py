# -*- coding: utf-8 -*-
"""
/***************************************************************************
    NextGIS WEB API
                              -------------------
        begin                : 2014-11-19
        git sha              : $Format:%H$
        copyright            : (C) 2014 by NextGIS
        email                : info@nextgis.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

RESOURCE_URL = lambda res_id: '/api/resource/%d' % res_id
COLLECTION_URL = '/api/resource/'


class Wrapper():
    def __init__(self, **params):
        self.__dict__.update(params)

DICT_TO_OBJ = lambda d: Wrapper(**d)


class NGWResource():

    def __init__(self, ngw_connection, resource_id):
        """
        Init resource and receive it from server
        :param ngw_connection: connection to the server
        :param resource_id: id of the resource
        """
        self._id = resource_id
        self._conn = ngw_connection
        self._json = None
        self._receive_obj()
        self._construct()

    def __init__(self, ngw_resource):
        """
        Init resource from other resource instance
        :param ngw_resource: any ngw_resource
        """
        self._id = ngw_resource._id
        self._conn = ngw_resource._conn
        self._json = ngw_resource._json
        self._construct()

    def _receive_obj(self):
        self._json = self._conn.get(RESOURCE_URL(self._id))

    def _construct(self):
        #resource
        """
        Construct resource from self._json
        Can be overridden in a derived class
        """
        self.common = DICT_TO_OBJ(self._json['resource'])
        if self.common.parent:
            self.common.parent = DICT_TO_OBJ(self.common.parent)
        if self.common.owner_user:
            self.common.owner_user = DICT_TO_OBJ(self.common.owner_user)
        #resmeta
        self.metadata = DICT_TO_OBJ(self._json['resmeta'])
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
from ngw_resource import NGWResource
from ngw_connection import NGWConnection
from ngw_error import NGWError


class NGWResourceFactory():

    def __init__(self, conn_settings):
        self.__conn = NGWConnection(conn_settings)

    def get_resource(self, resource_id):
        return NGWResource(self.__conn, resource_id)

    def get_root_resource(self):
        return NGWResource(self.__conn, 0)


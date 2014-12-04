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

import requests
import json
from ngw_error import NGWError


class NGWConnection():

    def __init__(self):
        self.server_url = None
        self.__session = requests.Session()

    def __init__(self, conn_settings):
        self.server_url = None
        self.__session = requests.Session()
        self.set_from_settings(conn_settings)

    def set_from_settings(self, conn_settings):
        self.server_url = conn_settings.server_url
        self.set_auth(conn_settings.username, conn_settings.password)

    def set_auth(self, username, password):
        self.__session.auth = (username, password)

    def __request(self, url, method, params=None, **kwargs):
        payload = None
        if params:
            payload = json.dumps(params)

        if 'data' in kwargs:
            payload = kwargs['data']

        req = requests.Request(method, self.server_url + url, data=payload)
        prep = self.__session.prepare_request(req)

        try:
            resp = self.__session.send(prep)
        except requests.exceptions.RequestException, e:
            raise NGWError(e.message.args[0])

        if resp.status_code / 100 != 2:
            raise NGWError(resp.content)

        return resp.json()

    def get(self, url, params=None, **kwargs):
        return self.__request(url, 'GET', params, **kwargs)

    def post(self, url, params=None, **kwargs):
        return self.__request(url, 'POST', params, **kwargs)

    def put(self, url, params=None, **kwargs):
        return self.__request(url, 'PUT', params, **kwargs)
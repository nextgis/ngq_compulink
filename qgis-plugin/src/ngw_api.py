# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ngw_api.py
                                 A QGIS plugin
 Compulink QGIS tools
                             -------------------
        begin                : 2014-10-31
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

__author__ = 'NextGIS'
__date__ = 'October 2014'
__copyright__ = '(C) 2014, NextGIS'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import re
import json
import datetime

import requests

from utils import *


class NGWConnectionSettings():
    def __init__(self, connection_name=None, url=None, user=None, password=None):
        self.connection_name = connection_name
        self.url = url
        self.user = user
        self.password = password


class NGWError(Exception):
    def __init__(self, message):
        self.message = unicode(message, 'utf-8')

    def __str__(self):
        return self.message

class NGWResource():
    def __init__(self):
        pass


class NGWApi:
    def __init__(self):
        self.url = None
        self.session = requests.Session()

    def setUrl(self, url):
        self.url = url

    def setAuth(self, user, password):
        self.session.auth = (user, password)

    def listResourceGroups(self):
        url = self.url + '/resource/0/child/'

        response = self._request(url, 'GET')

        groups = dict()
        groups[0] = '<root group>'
        for i in xrange(len(response)):
            item = response[i]['resource']
            if item['cls'] == 'resource_group':
                groups[item['id']] = item['display_name']
        return groups

    def addResourceGroup(self, parent, name):
        url = '{}/resource/{}/child/'.format(self.url, parent)

        params = dict(resource=dict(cls='resource_group', display_name=name))

        return self._request(url, 'POST', params)

    def addPostGISLayer(self, parent, name, layer):
        metadata = layer.source().split(' ')

        regex = re.compile('^host=.*')
        pos = metadata.index(
            [m.group(0) for l in metadata for m in [regex.search(l)] if m][0])
        tmp = metadata[pos]
        pos = tmp.find('=')
        host = tmp[pos + 1:]

        regex = re.compile('^dbname=.*')
        pos = metadata.index(
            [m.group(0) for l in metadata for m in [regex.search(l)] if m][0])
        tmp = metadata[pos]
        pos = tmp.find('=')
        dbname = tmp[pos + 2:-1]

        regex = re.compile('^user=.*')
        pos = metadata.index(
            [m.group(0) for l in metadata for m in [regex.search(l)] if m][0])
        tmp = metadata[pos]
        pos = tmp.find('=')
        userName = tmp[pos + 2:-1]

        regex = re.compile('^password=.*')
        pos = metadata.index(
            [m.group(0) for l in metadata for m in [regex.search(l)] if m][0])
        tmp = metadata[pos]
        pos = tmp.find('=')
        password = tmp[pos + 2:-1]

        regex = re.compile('^key=.*')
        pos = metadata.index(
            [m.group(0) for l in metadata for m in [regex.search(l)] if m][0])
        tmp = metadata[pos]
        pos = tmp.find('=')
        key = tmp[pos + 2:-1]

        regex = re.compile('^srid=.*')
        pos = metadata.index(
            [m.group(0) for l in metadata for m in [regex.search(l)] if m][0])
        tmp = metadata[pos]
        pos = tmp.find('from urllib2 import Request, urlopen
import base64=')
        srid = tmp[pos + 1:]

        regex = re.compile('^table=.*')
        pos = metadata.index(
            [m.group(0) for l in metadata for m in [regex.search(l)] if m][0])
        tmp = metadata[pos]
        pos = tmp.find('=')
        tmp = tmp[pos + 2:-1].split('.')
        schema = tmp[0][:-1]
        table = tmp[1][1:]

        regex = re.compile('^\(.*\)')
        pos = metadata.index(
            [m.group(0) for l in metadata for m in [regex.search(l)] if m][0])
        column = metadata[pos][1:-1]

        url = '{}/resource/{}/child/'.format(self.url, parent)

        connName = '{}-{}-{}'.format(
            host, dbname, datetime.datetime.now().isoformat())

        params = dict(
            resource=dict(
                cls='postgis_connection',
                display_name=connName),
            postgis_connection=dict(
                hostname=host, database=dbname, username=userName,
                password=password))

        conn = self._request(url, 'POST', params)

        params = dict(
            resource=dict(cls='postgis_layer', display_name=name),
            postgis_layer=dict(
                srs=dict(id=3857), fields='update', connection=conn,
                table=table, schema=schema, column_id=key,
                column_geom=column))
        return self._request(url, 'POST', params)

    def addWMSLayer(self, parent, name, layer):
        metadata = layer.source()

        regex = re.compile('format=.*?&')
        m = regex.search(metadata)
        tmp = metadata[m.start():m.end() - 1]
        pos = tmp.find('=')
        imgFormat = tmp[pos + 1:]

        regex = re.compile('layers=.*?&')
        m = regex.findall(metadata)
        tmp = []
        for i in m:
            pos = i.find('=')
            tmp.append(i[pos+1:-1])
        layers = ','.join(tmp)

        regex = re.compile('url=.*')
        m = regex.search(metadata)
        tmp = metadata[m.start():m.end()]
        pos = tmp.find('=')
        uri = tmp[pos + 1:]

        regex = re.compile('//.*/')
        m = regex.search(uri)
        host = uri[m.start():m.end()][2:-1]

        url = '{}/resource/{}/child/'.format(self.url, parent)

        connName = '{}-{}'.format(host, datetime.datetime.now().isoformat())

        params = dict(
            resource=dict(cls='wmsclient_connection',
                          display_name=connName),
            wmsclient_connection=dict(
                url=uri, version='1.1.1', capcache='query'))

        conn = self._request(url, 'POST', params)

        params = dict(
            resource=dict(cls='wmsclient_layer',
                          display_name=name),
            wmsclient_layer=dict(srs=dict(id=3857), wmslayers=layers,
                imgformat=imgFormat, connection=conn))

        return self._request(url, 'POST', params)

    def addVectorLayer(self, parent, name, layer):
        if (layer.source().startswith('/vsizip') or
                layer.storageType() != 'ESRI Shapefile'):
            source = exportToShapeFile(layer)
        else:
            source = layer.source()

        filePath = compressShapeFile(source)

        fileResource = self._uploadFile(filePath)

        url = '{}/resource/{}/child/'.format(self.url, parent)

        params = dict(
            resource=dict(
                cls='vector_layer', display_name=name),
            vector_layer=dict(srs=dict(id=3857), source=fileResource))

        layerResource = self._request(url, 'POST', params)

        return layerResource

    def addRasterLayer(self, parent, name, layer):
        filePath = layer.source()
        fileResource = self._uploadFile(filePath)

        url = '{}/resource/{}/child/'.format(self.url, parent)

        params = dict(
            resource=dict(
                cls='raster_layer', display_name=name),
            raster_layer=dict(srs=dict(id=3857), source=fileResource))

        layerResource = self._request(url, 'POST', params)

        return layerResource

    def addVectorStyle(self, layer, layerId):
        tmp = tempFileName('.qml')
        msg, saved = layer.saveNamedStyle(tmp)
        if not saved:
            raise NGWError(msg)

        styleFile = self._uploadFile(tmp)

        styleName = '{}-style'.format(layer.name())

        url = self.url + '/mapserver/qml-transform'
        params = dict(file=dict(upload_meta=[styleFile]))

        ngwStyle = self._request(url, 'POST', params)

        url = '{}/resource/{}/child/'.format(self.url, layerId)

        params = dict(
            resource=dict(
                cls='mapserver_style', display_name=styleName,
                parent=dict(id=layerId)),
            mapserver_style=dict(xml=ngwStyle))

        return self._request(url, 'POST', params)

    def addRasterStyle(self, layer, layerId):
        styleName = '{}-style'.format(layer.name())

        url = '{}/resource/{}/child/'.format(self.url, layerId)

        params = dict(
            resource=dict(
                cls='raster_style', display_name=styleName,
                parent=dict(id=layerId)))

        return self._request(url, 'POST', params)

    def addWebMap(self, parent, mapName, extent, tree):
        mapTree = self._paramsFromLayerTree(tree)

        url = '{}/resource/{}/child/'.format(self.url, parent)

        params = dict(
            resource=dict(
                cls='webmap', display_name=mapName, parent=dict(id=parent)),
            webmap=dict(
                extent_left=extent.xMinimum(), extent_right=extent.xMaximum(),
                extent_top=extent.yMaximum(), extent_bottom=extent.yMinimum(),
                root_item=dict(item_type='root', children=mapTree)))

        return self._request(url, 'POST', params)

    def _uploadFile(self, filePath):
        url = self.url + '/file_upload/upload'

        with open(filePath, 'rb') as f:
            result = self._request(url, 'PUT', data=f)
        return result

    def _request(self, url, method, params=None, **kwargs):
        #print ">>> %s %s" % (method, url)
        #print ">>> %s" % json.dumps(params, ensure_ascii=False)

        if params:
            payload = json.dumps(params)

        if 'data' in kwargs:
            payload = kwargs['data']

        req = requests.Request(method, url, data=payload)
        prep = self.session.prepare_request(req)

        try:
            resp = self.session.send(prep)
        except requests.exceptions.RequestException, e:
            raise NGWError(e.message)

        #print resp.status_code
        #print resp.content

        if resp.status_code / 100 != 2:
            raise NGWError(resp.content)

        #print resp.json()

        return resp.json()

    def _paramsFromLayerTree(self, tree):
        params = []
        for item in tree:
            if item['itemType'] == 'layer':
                layer = dict(
                    item_type='layer', display_name=item['name'],
                    layer_style_id=item['styleId'],
                    layer_enabled=item['enabled'], layer_adapter='image',
                    children=[])
                params.append(layer)
            elif item['itemType'] == 'group':
                group = dict(item_type='group', display_name=item['name'],
                    group_expanded=item['open'],
                    children=self._paramsFromLayerTree(item['layers']))
                params.append(group)
        return params

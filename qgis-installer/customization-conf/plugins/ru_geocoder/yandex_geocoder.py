"""
/***************************************************************************
 RuGeocoder
                                 A QGIS plugin
 Geocode your csv files to shp
                             -------------------
        begin                : 2012-02-20
        copyright            : (C) 2012 by Nikulin Evgeniy
        email                : nikulin.e at gmail
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
import json
import urllib2
import urllib
from qgis.core import QgsPoint

from base_geocoder import BaseGeocoder


class YandexGeocoder(BaseGeocoder):
    url = 'http://geocode-maps.yandex.ru/1.x/?key=APbJTE8BAAAAwUV4ZgIAWchAMdqatI8n3SLIv26SUw2telQAAAAAAAAAAABJnzuIcf3RGjjl50cTEPtvjEbW8w==&format=json&geocode='

    def geocode_components(self, region, rayon, city, street, house_number):
        full_addr = self._construct_reverse_search_str(region, rayon, city, street, house_number)
        return self.geocode(full_addr)

    def geocode_components_multiple_results(self, region, rayon, city, street, house_number):
        full_addr = self._construct_reverse_search_str(region, rayon, city, street, house_number)
        return self.geocode_multiple_results(full_addr)

    def geocode(self, search_str):
        res = self.geocode_multiple_results(search_str)
        if len(res) > 0:
            return res[0]
        else:
            return (QgsPoint(0, 0), 'Not found')

    def geocode_multiple_results(self, search_str):
        full_addr = urllib.quote(search_str.encode('utf-8'))
        if not full_addr:
            return []
        full_url = unicode(self.url) + unicode(full_addr, 'utf-8')

        f = urllib2.urlopen(full_url.encode('utf-8'))
        resp_str = unicode(f.read(),  'utf-8')
        resp_json = json.loads(resp_str)

        result = []
        if resp_json['response']['GeoObjectCollection']['featureMember']:
            for feat_mem in resp_json['response']['GeoObjectCollection']['featureMember']:
                pt_str = feat_mem['GeoObject']['Point']['pos']
                pt = QgsPoint(float(pt_str.split(' ')[0]), float(pt_str.split(' ')[1]))
                result.append((pt, feat_mem['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']))

        return result


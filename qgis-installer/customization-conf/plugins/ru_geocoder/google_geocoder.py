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
import time
import urllib2
import urllib
from qgis.core import QgsPoint
#from PyQt4.QtGui import QMessageBox

from base_geocoder import BaseGeocoder


class GoogleGeocoder(BaseGeocoder):
    url = 'http://maps.googleapis.com/maps/api/geocode/json?&language=ru&sensor=false&address='

    def geocode_components(self, region, rayon, city, street, house_number):
        full_addr = self._construct_search_str(region, rayon, city, street, house_number)
        return self.geocode(full_addr)

    def geocode_components_multiple_results(self, region, rayon, city, street, house_number):
        full_addr = self._construct_search_str(region, rayon, city, street, house_number)
        return self.geocode_multiple_results(full_addr)

    def geocode(self, search_str):
        res = self.geocode_multiple_results(search_str)
        if len(res) > 0:
            return res[0]
        else:
            return (QgsPoint(0, 0), 'Not found')

    def geocode_multiple_results(self, search_str):
        time.sleep(0.5)  # antiban
        full_addr = urllib.quote(search_str.encode('utf-8'))
        full_url = unicode(self.url) + unicode(full_addr, 'utf-8')
        print full_url

        f = urllib2.urlopen(full_url.encode('utf-8'))
        resp_str = unicode(f.read(),  'utf-8')
        resp_json = json.loads(resp_str)

        results = []
        if resp_json['results']:
            for res in resp_json['results']:
                pt = QgsPoint(float(res['geometry']['location']['lng']), float(res['geometry']['location']['lat']))
                desc = res['formatted_address']
                results.append((pt, desc))

        return results
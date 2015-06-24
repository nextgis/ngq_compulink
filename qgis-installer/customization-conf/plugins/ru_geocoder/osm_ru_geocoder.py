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
#from PyQt4.QtGui import QMessageBox

from base_geocoder import BaseGeocoder


class OsmRuGeocoder(BaseGeocoder):
    url = 'http://www.openstreetmap.ru/api/search?q='

    def _search(self, region, rayon, city, street, house_number):
        full_addr = self._construct_reverse_search_str(region, rayon, city, street, house_number)
        full_addr = urllib.quote(full_addr.encode('utf-8'))
        if not full_addr:
            #empty address
            return None
        full_url = unicode(self.url) + unicode(full_addr, 'utf-8')
        #QMessageBox.information(None, 'Geocoding debug', full_url)
                
        f = urllib2.urlopen(full_url.encode('utf-8'))
        resp_str = unicode(f.read(),  'utf-8')
        resp_json = json.loads(resp_str)
                
        if not resp_json['find']:
            #0 results
            return None
        else:
            #hm... no way to find right result :( weight, addr_type_it, this_poi????
            #now get first
            res0 = resp_json['matches'][0]
            pt = QgsPoint(float(res0['lon']), float(res0['lat']))
            return pt, res0['display_name']

    # TODO: need REFACTORING! strategy(opt/pis) and retrun None/[] not QgsPoint()
    def geocode_components(self, region, rayon, city, street, house_number):
        #try to search as is
        res = self._search(region, rayon, city, street, house_number)
        if res is not None:
            return res  
        
        #try to search street:
        res = self._search(region, rayon, city, street, None)
        if res is not None:
            return res
        
        #try to search settlement:
        res = self._search(region, rayon, city, None, None)
        if res is not None:
            return res
        
        #try to search district:
        res = self._search(region, rayon, None, None, None)
        if res is not None:
            return res
        
        #try to search region:
        res = self._search(region, None, None, None, None)
        if res is not None:
            return res
        
        #hm. wtf?
        pt = QgsPoint(0, 0)
        return pt, 'Not found'

    def geocode_components_multiple_results(self, region, rayon, city, street, house_number):
        raise NotImplementedError

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

        results = []
        if resp_json['find']:
            for res in resp_json['matches']:
                pt = QgsPoint(float(res['lon']), float(res['lat']))
                desc = res['display_name']
                results.append((pt, desc))

        return results
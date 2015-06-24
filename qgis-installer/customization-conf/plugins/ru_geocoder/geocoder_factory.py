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
from exceptions import ValueError
from osm_geocoder import OsmGeocoder
from osm_ru_geocoder import OsmRuGeocoder
from google_geocoder import GoogleGeocoder
from beta_osm_ru_geocoder import BetaOsmRuGeocoder
from yandex_geocoder import YandexGeocoder


geocoders = {
    'OSM': OsmGeocoder,
    'OSM.RU': OsmRuGeocoder,
    'BETA.OSM.RU': BetaOsmRuGeocoder,
    'Google': GoogleGeocoder,
    'Yandex': YandexGeocoder
}


class GeocoderFactory():

    @staticmethod
    def get_geocoder(geocoder_name):
        if geocoder_name in geocoders.keys():
            return geocoders[unicode(geocoder_name)]()
        else:
            raise ValueError('Unknown geocoder name')

    @staticmethod
    def get_geocoders_names():
        return geocoders.keys()
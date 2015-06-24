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
#from PyQt4.QtGui import QMessageBox


class BaseGeocoder():
    url = None

    def __init__(self):
        pass

    def geocode_components(self, region, rayon, city, street, house_number):
        raise NotImplementedError

    def geocode_components_multiple_results(self, region, rayon, city, street, house_number):
        raise NotImplementedError

    def geocode(self, search_str):
        raise NotImplementedError

    def geocode_multiple_results(self, search_str):
        raise NotImplementedError

    def _construct_search_str(self, region, rayon, city, street, house_number):
        search_str = ''
        if house_number:
            search_str += house_number + ', '
        if street:
            search_str += street + ', '
        if city:
            search_str += city + ', '
        if rayon:
            search_str += rayon + ', '
        if region:
            search_str += region
        search_str = search_str.rstrip().rstrip(',')
        return search_str

    def _construct_reverse_search_str(self, region, rayon, city, street, house_number):
        search_str = ''
        if region:
            search_str += region + ', '
        if rayon:
            search_str += rayon + ', '
        if city:
            search_str += city + ', '
        if street:
            search_str += street + ', '
        if house_number:
            search_str += house_number
        search_str = search_str.rstrip().rstrip(',')
        return search_str

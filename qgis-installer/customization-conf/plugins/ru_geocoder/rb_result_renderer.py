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

from PyQt4.QtGui import QColor
from qgis.gui import QgsRubberBand
from qgis.core import QGis, QgsRectangle, QgsCoordinateReferenceSystem, QgsCoordinateTransform


class RubberBandResultRenderer():

    def __init__(self, iface):
        self.iface = iface
        self.rb = QgsRubberBand(self.iface.mapCanvas(), QGis.Point)
        self.rb.setColor(QColor('magenta'))
        self.rb.setIconSize(12)

        self.srs_wgs84 = QgsCoordinateReferenceSystem(4326)
        self.transformation = QgsCoordinateTransform(self.srs_wgs84, self.srs_wgs84)

    def show_point(self, point, center=False):
        #check srs
        if self.need_transform():
            point = self.transform_point(point)

        self.rb.addPoint(point)
        if center:
            self.center_to_point(point)

    def clear(self):
        self.rb.reset(QGis.Point)

    def need_transform(self):
        return self.iface.mapCanvas().mapRenderer().destinationCrs().postgisSrid() != 4326

    def transform_point(self, point):
        dest_srs_id = self.iface.mapCanvas().mapRenderer().destinationCrs().srsid()
        self.transformation.setDestCRSID(dest_srs_id)
        try:
            return self.transformation.transform(point)
        except:
            print 'Error on transform!'  # DEBUG! need message???
            return

    def center_to_point(self, point):
        canvas = self.iface.mapCanvas()
        new_extent = QgsRectangle(canvas.extent())
        new_extent.scale(1, point)
        canvas.setExtent(new_extent)
        canvas.refresh()

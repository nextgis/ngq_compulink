# -*- coding: utf-8 -*-
"""
/***************************************************************************
 utils.py
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

import os
import glob
import uuid
import tempfile
import zipfile

from qgis.core import QgsVectorFileWriter


def tempFileName(suffix):
    fName = os.path.join(
        tempfile.gettempdir(), unicode(uuid.uuid4()).replace('-', '') + suffix)
    return fName


def exportToShapeFile(layer):
    tmp = tempFileName('.shp')
    QgsVectorFileWriter.writeAsVectorFormat(layer, tmp, 'utf-8', layer.crs())
    return tmp


def compressShapeFile(filePath):
    tmp = tempFileName('.zip')
    basePath = os.path.splitext(filePath)[0]
    baseName = os.path.splitext(os.path.basename(filePath))[0]

    zf = zipfile.ZipFile(tmp, 'w')
    for i in glob.iglob(basePath + '.*'):
        ext = os.path.splitext(i)[1]
        zf.write(i, baseName + ext)

    zf.close()
    return tmp

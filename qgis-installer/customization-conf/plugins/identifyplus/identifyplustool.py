# -*- coding: utf-8 -*-

#******************************************************************************
#
# IdentifyPlus
# ---------------------------------------------------------
# Extended identify tool. Supports displaying and modifying photos
#
# Copyright (C) 2012-2013 NextGIS (info@nextgis.org)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
#******************************************************************************

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

import resources_rc

class IdentifyPlusTool(QgsMapTool):
  used = pyqtSignal(QgsPoint)
  def __init__(self, canvas):
    QgsMapTool.__init__(self, canvas)
    self.canvas = canvas
    self.cursor = QCursor(QPixmap(":/icons/cursor.png"), 1, 1)
  
  def activate(self):
    self.canvas.setCursor(self.cursor)

  def canvasReleaseEvent(self, event):
    QApplication.setOverrideCursor(Qt.WaitCursor)
    self.used.emit( QgsPoint(event.x(), event.y()) )
    QApplication.restoreOverrideCursor()

  def isAvalable(self):
      return len(self.canvas.layers()) != 0

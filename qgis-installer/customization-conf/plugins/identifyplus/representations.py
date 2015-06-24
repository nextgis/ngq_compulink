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
#******************************************************************************eimport time

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

from ngw_external_api_python.core.ngw_utils import ngw_resource_from_qgs_map_layer

from representation_qgis import QGISAttributesModel, QGISAttributesView
from representation_ngw import NGWImagesModel, NGWImagesView

class DataProvider(object):
    def __init__(self, name, priority):
        self.__name = name
        self.__priority = priority
    
    def __str__(self):
        return self.__name + " data provider"
    def __repr__(self):
        return self.__name + " data provider"
    
    @property
    def name(self):
        return self.__name
    
    @property
    def priority(self):
        return self.__priority
    
class QGISDataProvider(DataProvider):
    def __init__(self):
        DataProvider.__init__(self, "qgis", 0)

class NGWDataProvider(DataProvider):
    def __init__(self, ngw_resource):
        DataProvider.__init__(self, "ngw", 1)
        self.__ngw_resource = ngw_resource
        
    @property
    def ngw_resource(self):
        return self.__ngw_resource
    
def provider_definition(qgsMapLayer):
    provides = [ QGISDataProvider() ]
    
    #if qgsMapLayer.type() == QgsMapLayer.RasterLayer:
    #    provides.append(GDALDataProvider())
        
    if qgsMapLayer.type() == QgsMapLayer.VectorLayer:
        
        ngw_resource = ngw_resource_from_qgs_map_layer(qgsMapLayer)        
        if ngw_resource is not None:            
            provides.append(NGWDataProvider(ngw_resource))
    
    return provides

class RepresentationsCache(object):
    def __init__(self):
        self.repr_variants = list()
        self.indexes = list()
        self.correspondences = dict()
        
    def save(self, representations, index):
        if representations not in self.repr_variants:
            self.repr_variants.append(representations)
        
        reprs_index = self.repr_variants.index(representations)
        self.correspondences.update({reprs_index:index})
    
    def getIndex(self, representations):
        if representations in self.repr_variants:
            return self.correspondences[self.repr_variants.index(representations)]
        else:
            return 0

class RepresentationContainer(QTabWidget):
    def __init__(self, parent = None):
        QTabWidget.__init__(self, parent)
        self.threades = list()
        
        self.reprs_cashe = RepresentationsCache()
    
        self.currentChanged.connect(self.tabChangedHandle)
    
    def allReprs(self):
        reprs = []
        for i in range( 0, self.count() ):
            reprs.append(type(self.widget(i)))
        return reprs
    
    def tabChangedHandle(self, index):
        self.reprs_cashe.save(self.allReprs(), index) 
    
    def takeControl(self, obj):
        self.clear()
        for provider in obj.providers:
            if isinstance(provider, QGISDataProvider):
                repr_widget = QGISAttributesView(self)                
                repr_widget.setModel(QGISAttributesModel(obj))
                tab_index = self.addTab(repr_widget, self.tr("Attributes"))
            
            if isinstance(provider, NGWDataProvider):
                #startTime = time.time()
                
                repr_widget = NGWImagesView(self)
                tab_index = self.addTab(repr_widget, self.tr("Photos") + " (ngw)")
                model = NGWImagesModel(obj, provider.ngw_resource)                                  
                repr_widget.setModel( model )
            
        self.setCurrentIndex(self.reprs_cashe.getIndex(self.allReprs()))
            
    def clear(self):
        for i in range( 0, self.count() ):
            self.widget(0).hide()
            self.widget(0).close()
            self.removeTab(0)
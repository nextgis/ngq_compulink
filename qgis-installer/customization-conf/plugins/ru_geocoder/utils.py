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

from qgis.core import QgsMapLayerRegistry, QgsMapLayer


def get_layer_all_fields(layer):
    """
    Return all fields for layer
    Use fTools code
    """
    return layer.dataProvider().fieldNameMap().keys()


def get_layer_str_fields(layer):
    """
    Return only string fields for layer
    Use fTools code
    """
    fields = layer.dataProvider().fields()
    field_list = []
    for field in fields:
        if field.typeName() == 'String':
            field_list.append(unicode(field.name()))
    return field_list  # sorted( field_list, cmp=locale.strcoll )
     

def get_layer_names(types):
    """
    Return list of names of all layers in QgsMapLayerRegistry
    Use fTools code
    """
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    layers_list = []
    if types == "all":
        for name, layer in layermap.iteritems():
            layers_list.append(unicode(layer.name()))
    else:
        for name, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer:
                if layer.geometryType() in types:
                    layers_list.append(unicode(layer.name()))
            elif layer.type() == QgsMapLayer.RasterLayer:
                if "Raster" in types:
                    layers_list.append(unicode(layer.name()))
    return layers_list


def get_vector_layer_by_name(lyr_name):
    """
    Return QgsVectorLayer from a layer name ( as string )
    Use fTools code
    """
    layers_map = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layers_map.iteritems():
        if layer.type() == QgsMapLayer.VectorLayer and layer.name() == lyr_name:
            if layer.isValid():
                return layer
            else:
                return None

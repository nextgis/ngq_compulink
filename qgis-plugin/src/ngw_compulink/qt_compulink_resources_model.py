# -*- coding: utf-8 -*-
"""
/***************************************************************************
    NextGIS WEB Compulink API
                              -------------------
        begin                : 2014-11-19
        git sha              : $Format:%H$
        copyright            : (C) 2014 by NextGIS
        email                : info@nextgis.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
!!!
Элемент модели дерева для NGW Compulink.
Строит дерево сразу с фильтрацией по типам и правам
Запрос дочерних элементов только для одного уровня иерархии
!!!
"""
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QIcon

from ..ngw_api.ngw_group_resource import NGWGroupResource
from ..ngw_api.qt_ngw_resources_model import QNGWResourceItem
from ngw_focl_proj import NGWFoclProject
from ngw_focl_struct import NGWFoclStruct
from ngw_situation_plan import NGWSituationPlan


class QNGWCompulinkResourceItem(QNGWResourceItem):

    def _load_children(self):
        '''
        Собирается дерево только для Групп, Проектов, ВОЛС и Ситуационных планов
        '''
        resource_children = self._ngw_resource.get_children()

        self._children = []
        for resource_child in resource_children:
            if resource_child.common.cls in [
                NGWGroupResource.type_id,
                NGWFoclStruct.type_id,
                NGWFoclProject.type_id,
                NGWSituationPlan.type_id,
            ]:
                self._children.append(QNGWCompulinkResourceItem(resource_child, self))

        self._children_loads = True

    def has_children(self):
        '''
        Ниже ВОЛС и СитПланов не уходим
        '''
        if self._ngw_resource.common.cls in [
                NGWFoclStruct.type_id,
                NGWSituationPlan.type_id,
        ]:
            return False
        return self.get_children_count() > 0

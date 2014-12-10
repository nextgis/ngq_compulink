# -*- coding: utf-8 -*-
"""
/***************************************************************************
    NextGIS WEB API
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
"""
from PyQt4.QtCore import QAbstractItemModel, QModelIndex, Qt, QVariant
from PyQt4.QtGui import QIcon


class QNGWResourcesModel(QAbstractItemModel):
    def __init__(self, tree_item):
        QAbstractItemModel.__init__(self)
        self.root = tree_item

    def index(self, row, column, parent_index=None, *args, **kwargs):
        if self.hasIndex(row, column, parent_index):
            parent_item = self._item_by_index(parent_index)
            child_item = parent_item.get_child(row)
            return self.createIndex(row, column, child_item)
        return QModelIndex()

    def parent(self, index=None):
        child_item = self._item_by_index(index)
        parent_item = child_item.parent()
        if parent_item == self.root or not parent_item:
            return QModelIndex()
        return self.createIndex(parent_item.row(), 0, parent_item) #??? WHY parent

    def rowCount(self, parent_index=None, *args, **kwargs):
        parent_item = self._item_by_index(parent_index)
        return parent_item.get_children_count()

    def columnCount(self, parent_index=None, *args, **kwargs):
        return 1

    def data(self, index, role=None):
        if index.isValid():
            return self._item_by_index(index).data(role)
        return QVariant()

    def hasChildren(self, parent_index=None, *args, **kwargs):
        return self._item_by_index(parent_index).has_children()

    def _item_by_index(self, index):
        if index and index.isValid():
            return index.internalPointer()
        else:
            return self.root


class QNGWResourceItem():
    def __init__(self, ngw_resource, parent):
        self._ngw_resource = ngw_resource
        self._parent = parent
        self._children = []  # lazy load
        self._children_loads = False
        print unicode(self.data(Qt.DisplayRole)), ' created!'  # debug

    def parent(self):
        return self._parent

    def row(self):
        if self._parent:
            return self._parent.get_children().index(self)
        else:
            return 0

    def get_children(self):
        if not self._children_loads:
            self._load_children()
        return self._children

    def get_child(self, row):
        if not self._children_loads:
            self._load_children()
        return self._children[row]

    def get_children_count(self):
        if not self._children_loads:
            self._load_children()
        return len(self._children)

    def _load_children(self):
        resource_children = self._ngw_resource.get_children()

        self._children = []
        for resource_child in resource_children:
            self._children.append(QNGWResourceItem(resource_child, self))

        self._children_loads = True

    def has_children(self):
        return self._ngw_resource.common.children

    def data(self, role):
        if role == Qt.DisplayRole:
            return self._ngw_resource.common.display_name
        if role == Qt.DecorationRole:
            return QIcon(self._ngw_resource.icon_path)
        if role == Qt.ToolTipRole:
            return self._ngw_resource.type_title
        if role == Qt.UserRole:
            return self._ngw_resource

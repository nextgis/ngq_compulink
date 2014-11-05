# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Plugins settings
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
from PyQt4.QtCore import QSettings
from ngw_api import NGWConnectionSettings


class PluginSettings():

    @classmethod
    def get_settings(cls):
        return QSettings('NextGIS', 'CompulinkTools')

    @classmethod
    def remove_connection(cls, connection_name):
        settings = cls.get_settings()
        key = '/connections/' + connection_name
        settings.remove(key)

    @classmethod
    def get_connection(cls, connection_name):
        settings = cls.get_settings()
        key = '/connections/' + connection_name

        return NGWConnectionSettings(
            connection_name,
            settings.value(key + '/url', ''),
            settings.value(key + '/user', ''),
            settings.value(key + '/password', '')
        )

    @classmethod
    def save_connection(cls, connection_settings):
        settings = cls.get_settings()
        key = '/connections/' + connection_settings.connection_name
        settings.setValue(key + '/url', connection_settings.url)
        settings.setValue(key + '/user', connection_settings.user)
        settings.setValue(key + '/password', connection_settings.password)

    @classmethod
    def get_last_connection(cls):
        settings = cls.get_settings()
        return settings.value('/ui/lastConnection', '')

    @classmethod
    def set_last_connection(cls, connection_name):
        settings = cls.get_settings()
        settings.setValue('/ui/lastConnection', connection_name)

    @classmethod
    def get_connection_names(cls):
        settings = cls.get_settings()
        settings.beginGroup('/connections')
        connections = settings.childGroups()
        settings.endGroup()
        return connections
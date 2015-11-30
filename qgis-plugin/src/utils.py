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
import json

from .plugin_settings import PluginSettings
from .ngw_api.core.ngw_connection import NGWConnection


class Utils:

    _compulink_dicts = None

    @classmethod
    def get_dicts(cls):
        if cls._compulink_dicts:
            return cls._compulink_dicts
        else:
            conn_name = PluginSettings.get_selected_ngw_connection_name()
            conn_sett = PluginSettings.get_ngw_connection(conn_name)
            conn = NGWConnection(conn_sett)
            cls._compulink_dicts = {}

            try:
                normal_dicts = conn.get('/compulink/get_dicts')
            except:
                return cls._compulink_dicts

            # revert dicts
            for d_name, d in normal_dicts.items():
                rev_d = {}
                for k,v in d.items():
                    rev_d[v] = k
                cls._compulink_dicts[d_name] = rev_d
            return cls._compulink_dicts

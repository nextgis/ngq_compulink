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
from urllib2 import URLError
#import sys

from PyQt4.QtGui import QDockWidget, QListWidgetItem  # , QMessageBox
from PyQt4.QtCore import QThread, pyqtSignal, Qt
from qgis.core import QgsPoint

from geocoder_factory import GeocoderFactory
from rb_result_renderer import RubberBandResultRenderer

from ui_quick_geocoding_toolbox import Ui_QuickGeocodingToolbox


class QuickGeocodingToolbox(QDockWidget, Ui_QuickGeocodingToolbox):
    def __init__(self, iface):
        QDockWidget.__init__(self, iface.mainWindow())
        self.setupUi(self)
        
        self.iface = iface
        self.search_threads = None  # []
        self.result_renderer = RubberBandResultRenderer(iface)

        if hasattr(self.txtSearch, 'setPlaceholderText'):
            self.txtSearch.setPlaceholderText(self.tr("Address..."))

        self.txtSearch.textChanged.connect(self.start_geocode)
        self.cmbGeocoder.currentIndexChanged.connect(self.start_geocode)
        self.cmbGeocoder.addItems(GeocoderFactory.get_geocoders_names())

        self.lstSearchResult.currentItemChanged.connect(self.result_selected)
        self.lstSearchResult.itemDoubleClicked.connect(self.result_selected)

        self.visibilityChanged.connect(self.result_renderer.clear)

    def __del__(self):
        self.result_renderer.clear()

    def start_geocode(self):
        search_text = unicode(self.txtSearch.text())
        if not search_text:
            self.lstSearchResult.clear()
            return
        
        geocoder_name = self.cmbGeocoder.currentText()
        
        if 1 == 1 and self.search_threads:
            print 'Kill ', self.search_threads
            self.search_threads.terminate()
            self.search_threads.wait()
            
        self.show_progress()
        searcher = SearchThread(search_text, geocoder_name, self.iface.mainWindow())
        searcher.data_downloaded.connect(self.show_result)
        searcher.error_occurred.connect(self.show_error)
        self.search_threads = searcher  # .append(searcher)
        searcher.start()

    def show_progress(self):
        self.lstSearchResult.clear()
        self.lstSearchResult.addItem(self.tr('Searching...'))
        
    def show_result(self, results):
        self.lstSearchResult.clear()
        if results:
            for (pt, desc) in results:
                new_item = QListWidgetItem()
                new_item.setText(unicode(desc))
                new_item.setData(Qt.UserRole, pt)
                self.lstSearchResult.addItem(new_item)
        else:
            new_item = QListWidgetItem()
            new_item.setText(self.tr('No results!'))
            new_item.setData(Qt.UserRole, None)
            self.lstSearchResult.addItem(new_item)

        self.lstSearchResult.update()
            
    def show_error(self, error_text):
        #print error_text
        self.lstSearchResult.clear()
        self.lstSearchResult.addItem(error_text)

    def result_selected(self, current=None, previous=None):
        self.result_renderer.clear()
        if current:
            point = current.data(Qt.UserRole)
            if isinstance(point, QgsPoint) and (point.x() != 0 and point.y() != 0):
                self.result_renderer.show_point(point, True)

    # for Settings
    def get_active_geocoder_name(self):
        return self.cmbGeocoder.currentText()

    def set_active_geocoder(self, geocoder_name):
        item_index = self.cmbGeocoder.findText(geocoder_name)
        if item_index >= 0:
            self.cmbGeocoder.setCurrentIndex(item_index)


class SearchThread(QThread):

    data_downloaded = pyqtSignal(object)
    error_occurred = pyqtSignal(object)    
    
    def __init__(self, search_text, geocoder_name, parent=None):
        QThread.__init__(self, parent)
        self.search_text = search_text
        self.geocoder_name = geocoder_name
        #define geocoder
        self.coder = GeocoderFactory.get_geocoder(geocoder_name)

    def __del__(self):
        pass
        #self.wait()

    def run(self):        
        results = []
        #results.append([None, self.search_text])  # debug

        #geocode
        try:
            results = self.coder.geocode_multiple_results(self.search_text)
        except URLError:
                        import sys
                        error_text = (self.tr("Network error!\n{0}")).format(unicode(sys.exc_info()[1]))
                        #error_text = 'net'
                        self.error_occurred.emit(error_text)
        except Exception:
                        import sys
                        error_text = (self.tr("Error of processing!\n{0}: {1}")).format(unicode(sys.exc_info()[0].__name__), unicode(sys.exc_info()[1]))
                        #error_text = 'common'
                        self.error_occurred.emit(error_text)

        self.data_downloaded.emit(results)
        #self.terminate()

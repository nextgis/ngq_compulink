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

import sys
from urllib2 import URLError
from datetime import datetime

from geocoder_factory import GeocoderFactory

from PyQt4.QtGui import QDialog, QMessageBox
from PyQt4.QtCore import QObject, SIGNAL

from qgis.core import QGis, QgsGeometry

from ui_batch_geocoding_dialog import Ui_BatchGeocodingDialog
from utils import get_vector_layer_by_name, get_layer_names, get_layer_str_fields,  get_layer_all_fields
import regions_helper


class BatchGeocodingDialog(QDialog, Ui_BatchGeocodingDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())

        #SIGNALS
        QObject.connect(self.btnRun, SIGNAL('clicked()'), self.processing)
        QObject.connect(self.cmbLayer, SIGNAL('currentIndexChanged(QString)'), self.fill_form)

        #INIT CONTROLS VALUES
        self.cmbGeocoder.addItems(GeocoderFactory.get_geocoders_names())
        self.cmbLayer.addItems(get_layer_names([QGis.Point]))
        for region in regions_helper.get_regions_names():
            self.cmbRegion.addItem(region['name'],  region)

    def __select_relevant_index(self, fields, values):
        for value in values:
            for field in fields:
                if value.lower() in field.lower():
                    return fields.index(field)
        return 0

    def fill_form(self, layer_name):
        layer = get_vector_layer_by_name(layer_name)
        str_fields = get_layer_str_fields(layer)
        all_fields = get_layer_all_fields(layer)

        #set cmb's
        self.cmbAddress.clear()
        self.cmbDistrictField.clear()
        self.cmbSettlField.clear()
        self.cmbStreet.clear()
        self.cmbBuildingNum.clear()

        self.cmbAddress.addItems(str_fields)
        self.cmbDistrictField.addItems(str_fields)
        self.cmbSettlField.addItems(str_fields)
        self.cmbStreet.addItems(str_fields)
        self.cmbBuildingNum.addItems(all_fields)

        #magic
        self.cmbAddress.setCurrentIndex(self.__select_relevant_index(str_fields,  ['address', 'addr']))
        self.cmbDistrictField.setCurrentIndex(self.__select_relevant_index(str_fields,  ['district', 'dist', 'rayon']))
        self.cmbSettlField.setCurrentIndex(self.__select_relevant_index(str_fields,  ['settlement', 'city', 'town',
                                                                                      'settl']))
        self.cmbStreet.setCurrentIndex(self.__select_relevant_index(str_fields,  ['street', 'st']))
        self.cmbBuildingNum.setCurrentIndex(self.__select_relevant_index(all_fields,  ['building', 'build', 'bld',
                                                                                       'bldg', 'house', 'number']))

    def processing(self):
        #checks
        if not self.cmbLayer.currentText():
            QMessageBox.warning(self, self.tr('RuGeocoder'), self.tr('You need to choose a point layer!'))
            return

        if self.cmbAddress.isEnabled() and not self.cmbAddress.currentText():
            QMessageBox.warning(self, self.tr('RuGeocoder'), self.tr(
                'You need to select the field containing the addresses!'))
            return

        if self.chkDistrict.isChecked() and self.rbDisctrictName.isChecked() and not self.txtDistrictName.text():
            QMessageBox.warning(self, self.tr('RuGeocoder'), self.tr('You need to enter the district name!'))
            return

        if self.chkDistrict.isChecked() and self.rbDistrictField.isChecked() and not self.cmbDistrictField.currentText():
            QMessageBox.warning(self, self.tr('RuGeocoder'), self.tr(
                'You need to select the field containing the names of districts!'))
            return

        if self.chkSettlement.isChecked() and self.rbSettlName.isChecked() and not self.txtSettlName.text():
            QMessageBox.warning(self, self.tr('RuGeocoder'), self.tr('You need to enter the city name!'))
            return

        if self.chkSettlement.isChecked() and self.rbSettlField.isChecked() and not self.cmbSettlField.currentText():
            QMessageBox.warning(self, self.tr('RuGeocoder'), self.tr(
                'You need to select the field containing the names of cities!'))
            return

        if self.chkStreet.isChecked() and not self.cmbStreet.currentText():
            QMessageBox.warning(self, self.tr('RuGeocoder'), self.tr(
                'You need to select the field containing the names of streets!'))
            return

        if self.chkStreet.isChecked() and not self.cmbBuildingNum.currentText():
            QMessageBox.warning(self, self.tr('RuGeocoder'), self.tr(
                'You need to select the field containing the numbers of buildings!'))
            return

        layer = get_vector_layer_by_name(self.cmbLayer.currentText())
        if not layer:
            QMessageBox.critical(self, self.tr('RuGeocoder'), self.tr(
                'Selected layer was not found! Maybe it was removed from the project. Please select another layer.'))
            return
        if not layer.isEditable():
            QMessageBox.warning(self, self.tr('RuGeocoder'),
                                 self.tr('Layer is not in edit mode! Please start editing the layer!'))
            return

        #setup ui
        data_provider = layer.dataProvider()
        features_for_update = data_provider.featureCount()
        if features_for_update > 0:
            self.prgProcess.setMaximum(features_for_update)
            self.prgProcess.setValue(0)
        start = datetime.now()

        #get num of fields
        addr_index = data_provider.fieldNameIndex(self.cmbAddress.currentText())
        district_index = data_provider.fieldNameIndex(self.cmbDistrictField.currentText())
        settl_index = data_provider.fieldNameIndex(self.cmbSettlField.currentText())
        street_index = data_provider.fieldNameIndex(self.cmbStreet.currentText())
        build_index = data_provider.fieldNameIndex(self.cmbBuildingNum.currentText())
        geocoded_index = data_provider.fieldNameIndex('geocoded')

        #define geocoder
        coder = GeocoderFactory.get_geocoder(self.cmbGeocoder.currentText())

        #define region
        region = None
        if self.chkRegion.isChecked():
            geocoder_name = unicode(self.cmbGeocoder.currentText())
            region_id = self.cmbRegion.itemData(self.cmbRegion.currentIndex())['id']
            region = regions_helper.get_specific_region_name(geocoder_name,  region_id)

        for feat in data_provider.getFeatures():
            #get values for geocoding
            addr = unicode(feat[addr_index])

            district = None
            if self.chkDistrict.isChecked():
                if self.rbDisctrictName.isChecked():
                    district = unicode(self.txtDistrictName.text())
                else:
                    district = unicode(feat[district_index])

            settl = None
            if self.chkSettlement.isChecked():
                if self.rbSettlName.isChecked():
                    settl = unicode(self.txtSettlName.text())
                else:
                    settl = unicode(feat[settl_index])

            if self.chkStreet.isChecked():
                street = unicode(feat[street_index])
                build_num = unicode(feat[build_index])
            else:
                street = addr  # ugly! maybe need one more method for geocoders???
                build_num = None

            #geocode
            try:
                pt, desc = coder.geocode_components(region, district, settl, street, build_num)
            except URLError:
                if QMessageBox.critical(self, self.tr('RuGeocoder'),
                            (self.tr('Network error!\n{0}\nIgnore the error and continue?'))
                            .format(unicode(sys.exc_info()[1])),
                            QMessageBox.Ignore | QMessageBox.Cancel) == QMessageBox.Ignore:
                    self.prgProcess.setValue(self.prgProcess.value() + 1)
                    continue
                else:
                    self.prgProcess.setValue(0)
                    return
            except Exception:
                if QMessageBox.critical(self, self.tr('RuGeocoder'),
                            (self.tr('Error of processing!\n{0}: {1}\nIgnore the error and continue?'))
                            .format(unicode(sys.exc_info()[0].__name__)), unicode(sys.exc_info()[1]),
                            QMessageBox.Ignore | QMessageBox.Cancel) == QMessageBox.Ignore:
                    self.prgProcess.setValue(self.prgProcess.value() + 1)
                    continue
                else:
                    self.prgProcess.setValue(0)
                    return

            #set geom
            layer.changeGeometry(feat.id(), QgsGeometry.fromPoint(pt))

            #set additional fields
            if geocoded_index >= 0:
                layer.changeAttributeValue(feat.id(), geocoded_index, desc)

            self.prgProcess.setValue(self.prgProcess.value() + 1)

        stop = datetime.now()

        #workaround for python < 2.7
        td = stop - start
        if sys.version_info[:2] < (2, 7):
            total_sec = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
        else:
            total_sec = td.total_seconds()

        QMessageBox.information(self, self.tr('Geocoding successfully completed'),
                         self.tr('Geoceded {0} features for {1} seconds')
                         .format(unicode(features_for_update), unicode(total_sec)))

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

from GdalTools.tools import GdalTools_utils

from identifyplusutils import  gdallocationinfoXMLOutputProcessing
from representations import provider_definition

class IdentificationObject(object):
    def __init__(self, attributes, qgsMapLayer, identificationTool = None, fid = None):
        self.__attributes = attributes
        self.__qgsMapLayer = qgsMapLayer
        self.__identificationTool = identificationTool
        self.__fid = fid
        self.providers = []
    @property
    def qgsMapLayer(self):
        return self.__qgsMapLayer
    
    @property
    def attributes(self):
        return self.__attributes
    
    @property
    def identificationTool(self):
        return self.__identificationTool
    
    @property
    def fid(self):
        return self.__fid
        
class IdentificationWorker(QObject):
    identificationProgress = pyqtSignal(int, int)
    identificationLayer = pyqtSignal(unicode)
    identificationResultsInLayer = pyqtSignal(list)
    finished = pyqtSignal()
    def __init__(self, qgsMapCanvas, qgsPoint, qgsLayers):
        QObject.__init__(self)
        
        self.__qgsMapCanvas = qgsMapCanvas
        self.__qgsPoint = qgsPoint
        self.__qgsLayers = qgsLayers
        
        self.__qgsLayersCounter = 0
        self.__qgsLayersNum = len(self.__qgsLayers)
    
    @pyqtSlot()
    def identification(self):
        for qgsLayer in self.__qgsLayers:
             
            self.thread().wait(100)         
            self.identificationProgress.emit(self.__qgsLayersCounter, self.__qgsLayersNum)
            self.identificationLayer.emit(qgsLayer.name())
            self.__qgsLayersCounter = self.__qgsLayersCounter + 1
            
            results = []
            if qgsLayer.type() == QgsMapLayer.RasterLayer:
                results = self.identificationInRaster(qgsLayer)
            elif qgsLayer.type() == QgsMapLayer.VectorLayer:
                results = self.identificationInVector(qgsLayer)
            
            if len(results) > 0:
                
                providers = provider_definition(qgsLayer)
                
                for i in range(0, len(results)):
                    results[i].providers = providers
                
                self.identificationResultsInLayer.emit(results)
        
        self.identificationProgress.emit(self.__qgsLayersNum, self.__qgsLayersNum)
        self.finished.emit()

    def identificationInRaster(self, qgsLayer):
        #QgsMessageLog.logMessage(
        #    "Identification raster point %f %f"%(self.__qgsPoint.x(), self.__qgsPoint.y()),
        #    u'IdentifyPlus',
        #    QgsMessageLog.INFO)
        
        point = self.__qgsMapCanvas.getCoordinateTransform().toMapCoordinates(self.__qgsPoint.x(), self.__qgsPoint.y())
        
        #QgsMessageLog.logMessage(
        #    "Identification raster point %f %f"%(point.x(), point.y()),
        #    u'IdentifyPlus',
        #    QgsMessageLog.INFO)
        
        #Use gdalocationinfo utility
        process = QProcess()
        GdalTools_utils.setProcessEnvironment(process)
        
        gdallocationinfo_params = []
        
        settings = QSettings()
        proxyEnabled = settings.value("proxy/proxyEnabled", False, type=bool)
        
        if proxyEnabled == True:
            proxyType = settings.value("proxy/proxyType", "", type=unicode)
            if  proxyType == "HttpProxy":
                
                GDAL_HTTP_PROXY = ""
                proxyHost = settings.value("proxy/proxyHost", None, type=unicode)
                if proxyHost is None:
                    QgsMessageLog.logMessage(
                        self.tr("QGIS proxysettings error") + ": " + self.tr("Parameter 'proxyHost' is missing"), 
                        u'IdentifyPlus', 
                        QgsMessageLog.CRITICAL)
                    return []                
                GDAL_HTTP_PROXY = GDAL_HTTP_PROXY + proxyHost             
                proxyPort = settings.value("proxy/proxyPort", None, type=unicode)
                if proxyPort is not None:
                    GDAL_HTTP_PROXY = GDAL_HTTP_PROXY  + ":%s"%proxyPort
                gdallocationinfo_params.extend(["--config", "GDAL_HTTP_PROXY", GDAL_HTTP_PROXY])
                
                GDAL_HTTP_PROXYUSERPWD = ""
                proxyUser = settings.value("proxy/proxyUser", None, type=unicode)
                if proxyUser is not None:
                    GDAL_HTTP_PROXYUSERPWD = GDAL_HTTP_PROXYUSERPWD + proxyUser
                    proxyPassword = settings.value("proxy/proxyPassword", None, type=unicode)
                    if proxyPassword is not None:
                        GDAL_HTTP_PROXYUSERPWD = GDAL_HTTP_PROXYUSERPWD + ":%s"%proxyPassword
                    gdallocationinfo_params.extend(["--config", "GDAL_HTTP_PROXYUSERPWD", GDAL_HTTP_PROXYUSERPWD])
        
        gdallocationinfo_params.extend(["-xml","-b", "1" ,"-geoloc", qgsLayer.source(), str(point.x()), str(point.y())])
        
        #QgsMessageLog.logMessage(
        #    "gdallocationinfo "+ " ".join(gdallocationinfo_params),
        #    u'IdentifyPlus',
        #    QgsMessageLog.INFO)
            
        process.start("gdallocationinfo", gdallocationinfo_params, QIODevice.ReadOnly)
        finishWaitSuccess = process.waitForFinished()
        
        #if not finishWaitSuccess:
        #    QgsMessageLog.logMessage(self.tr("Wait for gdallocationinfo more then 5 sec <br/>"), u'IdentifyPlus', QgsMessageLog.CRITICAL)
        #    return []
        
        if(process.exitCode() != 0):
            err_msg = str(process.readAllStandardError())
            if err_msg == '':
                err_msg = str(process.readAllStandardOutput())
            
            QgsMessageLog.logMessage(self.tr("gdallocationinfo return error status<br/>") + ":\n" + err_msg, u'IdentifyPlus', QgsMessageLog.CRITICAL)
        else:
            data = str(process.readAllStandardOutput());
            res = gdallocationinfoXMLOutputProcessing(data)
            
            if res[0] != None:
               QgsMessageLog.logMessage(self.tr("Parsing gdallocationinfo request error<br/>") + ":\n" + res[1] + "\n" + data, u'IdentifyPlus', QgsMessageLog.CRITICAL)
            else:
                identificationObjects = []
                for obj in res[1]:
                    identificationObjects.append(IdentificationObject(obj, qgsLayer, "gdallocationinfo utility")) 
                
                return identificationObjects
        return []
    
    def identificationInVector(self, qgsLayer):
        #QgsMessageLog.logMessage(
        #    "Identification vector in point %f %f"%(self.__qgsPoint.x(), self.__qgsPoint.y()),
        #    u'IdentifyPlus',
        #    QgsMessageLog.INFO)
        
        settings = QSettings()
        identifyValue = float(settings.value("/Map/searchRadiusMM", QGis.DEFAULT_IDENTIFY_RADIUS))
    
        if identifyValue <= 0.0:
          identifyValue = QGis.DEFAULT_IDENTIFY_RADIUS

        pointFrom = self.__qgsMapCanvas.getCoordinateTransform().toMapCoordinates(
            self.__qgsPoint.x() - identifyValue * self.__qgsMapCanvas.PdmWidthMM, 
            self.__qgsPoint.y() + identifyValue * self.__qgsMapCanvas.PdmHeightMM)
            
        pointTo = self.__qgsMapCanvas.getCoordinateTransform().toMapCoordinates(
            self.__qgsPoint.x() + identifyValue * self.__qgsMapCanvas.PdmWidthMM, 
            self.__qgsPoint.y() - identifyValue * self.__qgsMapCanvas.PdmHeightMM)
        
        featureCount = 0
        featureList = []
        try:
          #searchRadius = self.__qgsMapCanvas.extent().width() * (identifyValue / 100.0)
          r = QgsRectangle()
          r.setXMinimum(pointFrom.x())
          r.setXMaximum(pointTo.x())
          r.setYMinimum(pointFrom.y())
          r.setYMaximum(pointTo.y())
    
          r = self.__qgsMapCanvas.mapTool().toLayerCoordinates(qgsLayer, r)
    
          rq = QgsFeatureRequest()
          rq.setFilterRect(r)
          rq.setFlags(QgsFeatureRequest.ExactIntersect)
          for f in qgsLayer.getFeatures(rq):
            featureList.append(QgsFeature(f))
        except QgsCsException as cse:
          QgsMessageLog.logMessage(self.tr("Caught CRS exception") + ":\n" + cse.what(), u'IdentifyPlus', QgsMessageLog.CRITICAL)
        
        myFilter = False
    
        #renderer = qgsLayer.rendererV2() # РЅРµРёР·РІРµСЃС‚РЅРѕСЃС‚СЊ
    
        qgsVersion = int(unicode(QGis.QGIS_VERSION_INT))
        
        
        #if renderer is not None and (renderer.capabilities() | QgsFeatureRendererV2.ScaleDependent):
        #  if qgsVersion < 20200 and qgsVersion > 10900:
        #    renderer.startRender( self.__qgsMapCanvas.mapRenderer().rendererContext(), qgsLayer)
        #  elif qgsVersion >= 20300:
        #    renderer.startRender( self.__qgsMapCanvas.mapRenderer().rendererContext(), qgsLayer.pendingFields())
        #  else:
        #    renderer.startRender( self.__qgsMapCanvas.mapRenderer().rendererContext(), qgsLayer)
            
        #  myFilter = renderer.capabilities() and QgsFeatureRendererV2.Filter
    
        #for f in featureList:
        #    if myFilter and not renderer.willRenderFeature(f): # РєР°РєРёРµ-С‚Рѕ С„РёС‡Рё РѕС‚СЃРµРёРІР°СЋС‚
        #        continue
        #    featureCount += 1
        #    self.objects.append(ExtendedFeature(self.__qgsMapCanvas, qgsLayer, f))
        
        #if renderer is not None and (renderer.capabilities() | QgsFeatureRendererV2.ScaleDependent):
        #  renderer.stopRender(self.__qgsMapCanvas.mapRenderer().rendererContext())
        
        identificationObjects = []
        for qgsFeature in featureList:
            attrs = {}
            qgsAttrs = qgsFeature.attributes()
            fields = qgsFeature.fields().toList()
            for i in xrange(len(qgsAttrs)):
                attrs.update( {fields[i].name(): qgsAttrs[i]} )
                
            identificationObjects.append(IdentificationObject(attrs, qgsLayer, "qgis", qgsFeature.id())) 
        
        return identificationObjects
    
class IdentifyPlusModel(QObject):
    identificationProgress = pyqtSignal(int, int)
    identificationLayer = pyqtSignal(unicode)
    finished = pyqtSignal()
    
    reseted = pyqtSignal()
    objectsAppended = pyqtSignal(int)
    
    busy = pyqtSignal()
    def __init__(self, qgsMapCanvas):
        QObject.__init__(self)

        if not isinstance(qgsMapCanvas, QgsMapCanvas):
            raise TypeError("IdentifyPlusModel expected a qgis._gui.QgsMapCanvas, got a {} instead".format(type(qgsMapCanvas)))

        self._qgsMapCanvas = qgsMapCanvas
        self._qgsMapLayers = list()
        #self._killed = False
        self._identificationObjects = []
        
        self.__is_busy = False
    def data(self, index):
        return self._identificationObjects[index]
    
    def objectsCount(self):
        return len(self._identificationObjects)
    
    def _defineLayers(self, **args):
        del self._qgsMapLayers[:]

        if (args.has_key(u"all_qgis_layers")):
            if args[u"all_qgis_layers"] == True:
                self._qgsMapLayers.extend(self._qgsMapCanvas.layers())

    def identify(self, qgsPoint):
        if self.__is_busy == True:
            self.busy.emit()
            return
        
        self.__is_busy = True     
        self.thread = QThread(self)
        self.thread.setTerminationEnabled(True)
              
        self.reseted.emit()
        
        self._defineLayers(all_qgis_layers=True)
        self._identificationObjects = []
        
        self.worker = IdentificationWorker(self._qgsMapCanvas, qgsPoint, self._qgsMapLayers)
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.identification)
        self.thread.started.connect(self.threadStarted)
        self.thread.finished.connect(self.threadFinished)
        self.thread.terminated.connect(self.threadTerminated)
        
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.identificationFinishedHandle)
        self.worker.identificationProgress.connect(self.identificationProgressHandle)
        self.worker.identificationLayer.connect(self.identificationLayerHandle)
        self.worker.identificationResultsInLayer.connect(self.identificationResultsInLayerHandle)
        self.thread.start(QThread.HighestPriority)
        
    def threadTerminated(self):
        #QgsMessageLog.logMessage(
        #    "Identification thread terminated",
        #    u'IdentifyPlus',
        #    QgsMessageLog.INFO)
        pass
        
    def threadStarted(self):
        #QgsMessageLog.logMessage(
        #    "Identification thread start",
        #    u'IdentifyPlus',
        #    QgsMessageLog.INFO)
        pass
    def threadFinished(self):
        #QgsMessageLog.logMessage(
        #    "Identification thread finish",
        #    u'IdentifyPlus',
        #    QgsMessageLog.INFO)
        pass
    def identificationProgressHandle(self, i, c):
        self.identificationProgress.emit(i,c)
        
    def identificationLayerHandle(self, layerName):
        self.identificationLayer.emit(layerName)
    
    def identificationResultsInLayerHandle(self, res):
        self._identificationObjects.extend(res)
        self.objectsAppended.emit(len(res))
    
    def identificationFinishedHandle(self):
        self.__is_busy = False
        self.finished.emit()
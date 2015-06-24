# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from ui_nd_addfeature import Ui_Nd_AddFeature
import webbrowser, os

currentPath = os.path.dirname(__file__)
        
class NdAddFeatureGui(QDialog, QObject, Ui_Nd_AddFeature):
    def __init__(self, iface, layertype, coords):
        self.layertype = layertype
        QDialog.__init__(self, iface)
        self.iface = iface
        self.setupUi(self)
        
        self.twPoints.setColumnWidth(0,self.twPoints.width()/2)
        self.twPoints.setColumnWidth(1,self.twPoints.width()/2)
        self.twPoints.horizontalHeader().setResizeMode(0,QHeaderView.Stretch)
        self.twPoints.horizontalHeader().setResizeMode(1,QHeaderView.Stretch)
        
        QObject.connect( self.twPoints, SIGNAL("cellChanged(int,int)"), self.cellChanged )
        QObject.connect( self.buttonBox, SIGNAL("accepted ()"), self.onOK )   
        
        self.buttonBox.button(QDialogButtonBox.Ok ).setEnabled(False)
        
        self.pb_ChooseCrs.setEnabled(False)
        self.l_OtherCrsName.setEnabled(False)
        
        self.rb_OtherCrs.toggled.connect(self.selectOtherCrs)
        self.pb_ChooseCrs.clicked.connect(self.chooseOtherCrs)
        
        settings = QSettings()
        self.featureCrsId = settings.value("numericDigitize/featureCrsId", -1, type=long)
        rb_checked = settings.value("numericDigitize/checked", "rb_ProjectCrs", type=unicode)
        if rb_checked == "rb_ProjectCrs":
            self.rb_ProjectCrs.setChecked(True)
        elif rb_checked == "rb_LayerCrs":
            self.rb_LayerCrs.setChecked(True)
        else:
            self.rb_OtherCrs.setChecked(True)
        self.__displayAuthid()
        
        row_index = 0
        for coord in coords:
            item = QTableWidgetItem(str(coord.x()))
            item.setText(str(coord.x()))
            self.twPoints.setItem(row_index,0,item)
            item = QTableWidgetItem(str(coord.y()))
            item.setText(str(coord.y()))
            self.twPoints.setItem(row_index,1,item)
            row_index = row_index + 1
            
        if self.__checkMinFeaturePoints():
            self.buttonBox.button(QDialogButtonBox.Ok ).setEnabled(True)
            
    def selectOtherCrs(self, checked):
        if checked == True:
            self.pb_ChooseCrs.setEnabled(True)
            self.l_OtherCrsName.setEnabled(True)
        else:
            self.pb_ChooseCrs.setEnabled(False)
            self.l_OtherCrsName.setEnabled(False)

    def chooseOtherCrs(self):
        crsSelector = QgsGenericProjectionSelector()
        if crsSelector.exec_():
            self.featureCrsId = crsSelector.selectedCrsId()
            self.__displayAuthid()
    
    def __displayAuthid(self):
        if self.featureCrsId == -1:
            self.l_OtherCrsName.setText("[%s]"%self.tr("crs not selected"))
        else:
            self.l_OtherCrsName.setText(
                "[%s]"%QgsCoordinateReferenceSystem(self.featureCrsId, QgsCoordinateReferenceSystem.InternalCrsId).authid()
                )
    
    def __getPointCoordinate(self, currentRow, currentColumn):
        theValue = self.twPoints.item(currentRow, currentColumn)
        return theValue.text().replace(',', '.')
    
    def cellChanged (self, currentRow, currentColumn):      
        theValueAsString = self.__getPointCoordinate(currentRow, currentColumn)
        
        #only add a new row, if all cells are used, also be sure, 
        #that only numerics find their way in the table
        if( self.is_number(theValueAsString) ):
           if((self.twPoints.rowCount() == currentRow+1)) :
             try:
               self.twPoints.item(currentRow, 0).text() != ""
               xok = True
             except AttributeError:
               xok = False
             try:
               self.twPoints.item(currentRow, 1).text() != ""
               yok = True
             except AttributeError:
               yok = False

             if(xok and yok):
               self.twPoints.setRowCount(self.twPoints.rowCount())
               self.twPoints.insertRow(self.twPoints.rowCount())
               if self.__checkMinFeaturePoints():
                 self.buttonBox.button(QDialogButtonBox.Ok ).setEnabled(True)

        else:
          self.twPoints.item(currentRow, currentColumn).setText("")
        
    def __checkMinFeaturePoints(self):
        if(self.layertype in (QGis.WKBPoint, QGis.WKBMultiPoint) ):
            if(self.twPoints.rowCount()-1)>=1:
                return True
        elif(self.layertype in (QGis.WKBLineString, QGis.WKBMultiLineString  ) ):
            if(self.twPoints.rowCount()-1)>=2:
                return True
        elif(self.layertype in (QGis.WKBPolygon, QGis.WKBMultiPolygon) ):
            if(self.twPoints.rowCount()-1)>=3:
                return True
        return False
    
    def is_number(self, s):
      try:
          float(s)
          return True
      except ValueError:
          return False
    
    def onOK(self):
      settings = QSettings()
      #tell the world if the coord sould be transformed into the layer crs
      if self.rb_ProjectCrs.isChecked():
        self.emit(SIGNAL("transformOTF_CRS(PyQt_PyObject)"), self.rb_ProjectCrs.isChecked())
        settings.setValue("numericDigitize/checked", "rb_ProjectCrs")
      elif self.rb_OtherCrs.isChecked():
        self.emit(SIGNAL("transformFromCrs(long)"), self.featureCrsId)
        settings.setValue("numericDigitize/checked", "rb_OtherCrs")
        settings.setValue("numericDigitize/featureCrsId", self.featureCrsId)
      else:
        settings.setValue("numericDigitize/checked", "rb_LayerCrs")
        
      #tell the coords
      coords = []
      for i in range(self.twPoints.rowCount()-1):
        pt = QgsPoint(float( self.__getPointCoordinate(i, 0) ), float( self.__getPointCoordinate(i, 1) ))
        coords.append(pt)
      self.emit(SIGNAL("numericalFeature(PyQt_PyObject)"), coords)
      
        



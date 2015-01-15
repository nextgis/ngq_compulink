!define PROGRAM_NAME "NextGIS QGIS Compulink" ; для идентификации установленного ПО 

; define by auto build system ======
;!define PROGRAM_VERSION "0.0.5" ; для идентификации установленного ПО
; ==================================

!define PROGRAM_INSTALLER_HEADER "ГИС контроля строительства ВОЛС"

; define by auto build system ======
;!define INSTALLER_DST_DIR "./" ; good
; ==================================

!define PROGRAM_INSTALLER_OUTPUT_FILENAME "${INSTALLER_DST_DIR}\NextGIS_QGIS_Compulink_${PROGRAM_VERSION}"

!define PROGRAM_INSTALL_DEFAULT_INSTALL_DIR "c:\NextGIS_QGIS_Compulink"

!define PROGRAM_RUN_LNK_NAME "ГИС контроля строительства ВОЛC"
!define PROGRAM_UNINSTALL_FILE_NAME "Uninstall-NextGIS_QGIS_Compulink-${PROGRAM_VERSION}"
!define PROGRAM_UNINSTALL_LNK_NAME "Удалить ${PROGRAM_RUN_LNK_NAME} (${PROGRAM_VERSION})"

#!define DEFAULT_PROJECT ""

!define PROGRAM_RUN_LNK_ICO_PATH "..\src\files-diff\src\app\qgis.ico"
!define PROGRAM_RUN_LNK_ICO_FILENAME "qgis.ico"

!define QGIS_RUN_BAT "..\Installer-Files\qgis.bat"
!define QGIS_PRE_RUN_BAT "..\Installer-Files\qgis_preruner.bat"

!define QGIS_DEFAULT_OPTIONS_PATH "..\interface_settings"

!define FONTS_DIR "..\fonts"

; define by auto build system ======
;!define OSGEO4W_SRC_DIR "D:\builds\osgeo4w" ;good
;!define QGIS_SRC_DIR "D:\builds\nextgis-qgis-release" ;good
;!define GRASS_SRC_DIR "D:\builds\grass-fromOSGEO4W" ;good
;!define SAGA_SRC_DIR "D:\builds\saga-fromOSGEO4W" ;good
;!define GDAL_SRC_DIR "D:\builds\gdal-1.11.0-fromOSGEO4W" ;good
; ==================================

; define by auto build system ======
;!define QGIS_MANUAL_FILE_NAME_RU "QGIS-2.6-UserGuide-ru.pdf"; good
;!define QGIS_MANUAL_FILE_NAME_EN "QGIS-2.6-UserGuide-en.pdf"; good
;!define PLUGINS "d:\builds\plugins\map_services d:\builds\plugins\openlayers_plugin d:\builds\plugins\identifyplus d:\builds\plugins\compulink_tools"
; ==================================

!include "nextgis-qgis-ru-base.nsi"
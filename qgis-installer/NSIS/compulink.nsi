!define PROGRAM_NAME "NextGIS QGIS Compulink" ; для идентификации установленного ПО 

!define PROGRAM_VERSION "0.0.5" ; для идентификации установленного ПО

!define PROGRAM_INSTALLER_HEADER "ГИС контроля строительства ВОЛС"

!define PROGRAM_INSTALLER_OUTPUT_FILENAME "d:\builds\NextGIS_QGIS_Compulink_0.0.5"

!define PROGRAM_INSTALL_DEFAULT_INSTALL_DIR "c:\NextGIS_QGIS_Compulink"

!define PROGRAM_RUN_LNK_NAME "ГИС контроля строительства ВОЛC"
!define PROGRAM_UNINSTALL_FILE_NAME "Uninstall-NextGIS_QGIS_Compulink-${PROGRAM_VERSION}"
!define PROGRAM_UNINSTALL_LNK_NAME "Удалить ${PROGRAM_RUN_LNK_NAME} (${PROGRAM_VERSION})"

#!define DEFAULT_PROJECT ""

!define PROGRAM_RUN_LNK_ICO_PATH "..\src\qgis.ico"
!define PROGRAM_RUN_LNK_ICO_FILENAME "qgis.ico"

!define QGIS_RUN_BAT "..\Installer-Files\qgis.bat"
!define QGIS_PRE_RUN_BAT "..\Installer-Files\qgis_preruner.bat"

!define QGIS_DEFAULT_OPTIONS_PATH "..\interface_settings"

!define PLUGINS "d:\builds\plugins\map_services d:\builds\plugins\openlayers_plugin d:\builds\plugins\identifyplus d:\builds\plugins\compulink_tools"

!define FONTS_DIR "d:\builds\fonts"

!define OSGEO4W_SRC_DIR "d:\\builds\\osgeo4w-env____\\"
!define QGIS_SRC_DIR "d:\\builds\\nextgis-qgis-compulink\\"
!define GRASS_SRC_DIR "d:\\builds\\grass-fromOSGEO4W\\"
!define SAGA_SRC_DIR "d:\\builds\\saga-fromOSGEO4W\\"
!define GDAL_SRC_DIR "d:\\builds\\gdal-2.0.0-dev-with-ags\\"

;!define OSGEO4W_SRC_DIR "d:\\builds\\for_test\\"
;!define QGIS_SRC_DIR "d:\\builds\\for_test\\"
;!define GRASS_SRC_DIR "d:\\builds\\for_test\\"
;!define SAGA_SRC_DIR "d:\\builds\\for_test\\"
;!define GDAL_SRC_DIR "d:\\builds\\for_test\\"

!include "nextgis-qgis-ru-base.nsi"
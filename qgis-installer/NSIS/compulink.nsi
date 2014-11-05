!define PROGRAM_NAME "NextGIS QGIS Compulink" ; для идентификации установленного ПО 

!define PROGRAM_VERSION "0.0.1" ; для идентификации установленного ПО

!define PROGRAM_INSTALLER_HEADER "ГИС контроля строительства ВОЛС"

!define PROGRAM_INSTALLER_OUTPUT_FILENAME "d:\builds\NextGIS_QGIS_Compulink_0.0.1"

!define PROGRAM_INSTALL_DEFAULT_INSTALL_DIR "c:\NextGIS_QGIS_Compulink"

!define PROGRAM_RUN_LNK_NAME "ГИС контроля строительства ВОЛC"
!define PROGRAM_UNINSTALL_FILE_NAME "Uninstall-NextGIS_QGIS_Compulink-${PROGRAM_VERSION}"
!define PROGRAM_UNINSTALL_LNK_NAME "Удалить ${PROGRAM_RUN_LNK_NAME} (${PROGRAM_VERSION})"

#!define DEFAULT_PROJECT ""

!define PROGRAM_RUN_LNK_ICO_PATH "..\src\src\app\qgis.ico"
!define PROGRAM_RUN_LNK_ICO_FILENAME "qgis.ico"

!define QGIS_RUN_BAT "..\Installer-Files\qgis.bat"

!define QGIS_DEFAULT_OPTIONS_PATH "..\src\default_options"

!define PLUGINS "d:\builds\plugins\gdallocationinfo_plugin d:\builds\plugins\openlayers_plugin"

!define OSGEO4W_SRC_DIR "d:\\builds\\osgeo4w-env\\"
!define QGIS_SRC_DIR "c:\\builds\\nextgis-qgis-compulink\\"
!define GRASS_SRC_DIR "d:\\builds\\grass-fromOSGEO4W\\"
!define SAGA_SRC_DIR "d:\\builds\\saga-fromOSGEO4W\\"
!define GDAL_SRC_DIR "d:\\builds\\gdal-2.0.0-dev\\"

;!define OSGEO4W_SRC_DIR "d:\\builds\\for_test\\"
;!define QGIS_SRC_DIR "d:\\builds\\for_test\\"
;!define GRASS_SRC_DIR "d:\\builds\\for_test\\"
;!define SAGA_SRC_DIR "d:\\builds\\for_test\\"
;!define GDAL_SRC_DIR "d:\\builds\\for_test\\"

!include "nextgis-qgis-ru-base.nsi"
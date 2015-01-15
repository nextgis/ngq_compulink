@echo off
echo "======== Configurate qgis  Start==========="

cmake -G "Visual Studio 9 2008" ^
-D PEDANTIC=TRUE ^
-D WITH_QSPATIALITE=TRUE ^
-D WITH_MAPSERVER=TRUE ^
-D MAPSERVER_SKIP_ECW=TRUE ^
-D WITH_GLOBE=TRUE ^
-D WITH_TOUCH=TRUE ^
-D WITH_ORACLE=TRUE ^
-D CMAKE_BUILD_TYPE=Release ^
-D CMAKE_INSTALL_PREFIX=%1 ^
-D BISON_EXECUTABLE=bison.exe ^
-D FLEX_EXECUTABLE=flex.exe ^
%2

echo "======== Configurate qgis  Finish==========="
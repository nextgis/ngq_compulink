@echo off
call "%~dp0\o4w_env.bat"
call "%OSGEO4W_ROOT%"\apps\grass\grass-6.4.3\etc\env.bat
@echo off
path %PATH%;%OSGEO4W_ROOT%\apps\qgis\bin;%OSGEO4W_ROOT%\apps\grass\grass-6.4.3\lib
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis
rem Set VSI cache to be used as buffer, see #6448
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000

start "Prerun NextGIS QGIS" /B /WAIT "python.exe" "%OSGEO4W_ROOT%"\bin\qgis_preruner.py "%OSGEO4W_ROOT%" "%UserProfile%\NextGIS QGIS Compulink"

start "NextGIS QGIS" /B "%OSGEO4W_ROOT%"\bin\qgis.exe --configpath "%UserProfile%\NextGIS QGIS Compulink"
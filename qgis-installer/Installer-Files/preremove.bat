@echo off
del preremove.log>>preremove.log
echo OSGEO4W_ROOT=%OSGEO4W_ROOT%>>preremove.log 2>&1
echo OSGEO4W_STARTMENU=%OSGEO4W_STARTMENU%>>preremove.log 2>&1
set OSGEO4W_ROOT_MSYS=%OSGEO4W_ROOT:\=/%
if "%OSGEO4W_ROOT_MSYS:~1,1%"==":" set OSGEO4W_ROOT_MSYS=/%OSGEO4W_ROOT_MSYS:~0,1%/%OSGEO4W_ROOT_MSYS:~3%
echo OSGEO4W_ROOT_MSYS=%OSGEO4W_ROOT_MSYS%>>preremove.log 2>&1
PATH %OSGEO4W_ROOT%\bin;%PATH%>>preremove.log 2>&1
cd %OSGEO4W_ROOT%>>preremove.log 2>&1
echo Running preremove grass64.bat...
%COMSPEC% /c etc\preremove\grass64.bat>>preremove.log 2>&1
ren etc\preremove\grass64.bat grass64.bat.done>>preremove.log 2>&1
echo Running preremove msys.bat...
%COMSPEC% /c etc\preremove\msys.bat>>preremove.log 2>&1
ren etc\preremove\msys.bat msys.bat.done>>preremove.log 2>&1
echo Running preremove pyqt4.bat...
%COMSPEC% /c etc\preremove\pyqt4.bat>>preremove.log 2>&1
ren etc\preremove\pyqt4.bat pyqt4.bat.done>>preremove.log 2>&1
echo Running preremove qgis.bat...
%COMSPEC% /c etc\preremove\qgis.bat>>preremove.log 2>&1
ren etc\preremove\qgis.bat qgis.bat.done>>preremove.log 2>&1
echo Running preremove qt4-libs.bat...
%COMSPEC% /c etc\preremove\qt4-libs.bat>>preremove.log 2>&1
ren etc\preremove\qt4-libs.bat qt4-libs.bat.done>>preremove.log 2>&1
echo Running preremove shell.bat...
%COMSPEC% /c etc\preremove\shell.bat>>preremove.log 2>&1
ren etc\preremove\shell.bat shell.bat.done>>preremove.log 2>&1
echo Running preremove sip.bat...
%COMSPEC% /c etc\preremove\sip.bat>>preremove.log 2>&1
ren etc\preremove\sip.bat sip.bat.done>>preremove.log 2>&1
ren preremove.bat preremove.bat.done

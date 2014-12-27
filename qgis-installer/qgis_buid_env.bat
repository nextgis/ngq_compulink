@echo off

path %SYSTEMROOT%\system32;%SYSTEMROOT%;%SYSTEMROOT%\System32\Wbem;
set PYTHONPATH=

set OSGEO4W_ROOT=c:\OSGeo4W
call "%OSGEO4W_ROOT%\bin\o4w_env.bat"

set VS90COMNTOOLS=%PROGRAMFILES%\Microsoft Visual Studio 9.0\Common7\Tools\
call "%PROGRAMFILES%\Microsoft Visual Studio 9.0\VC\vcvarsall.bat" x86

set INCLUDE=%INCLUDE%;%PROGRAMFILES%\Microsoft Platform SDK for Windows Server 2003 R2\Include
set LIB=%LIB%;%PROGRAMFILES%\Microsoft Platform SDK for Windows Server 2003 R2\Lib

path %PATH%;%PROGRAMFILES%\CMake 2.8\bin;%PROGRAMFILES%\Git\bin;%PROGRAMFILES%\subversion\bin;%PROGRAMFILES%\GnuWin32\bin;%PROGRAMFILES%\Microsoft Visual Studio 9.0\Common7\IDE

set GRASS_PREFIX=c:\OSGeo4W\apps\grass\grass-6.4.4
set INCLUDE=%INCLUDE%;%OSGEO4W_ROOT%\include
set LIB=%LIB%;%OSGEO4W_ROOT%\lib

path %PATH%;%PROGRAMFILES%\NSIS\bin
path %PATH%;%1
@cmd


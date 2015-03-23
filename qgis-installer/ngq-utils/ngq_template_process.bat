@echo off

echo OSGEO4W_ROOT: %OSGEO4W_ROOT%

call %OSGEO4W_ROOT%\bin\o4w_env.bat

set TemplatesDir=%1
set InsertPath=%2
set InsertPath=%InsertPath:"=%
set InsertPath=%InsertPath:\=\/%

echo TemplatesDir: %TemplatesDir%
echo InsertPath: %InsertPath%

echo PATH: %PATH%
for %%f in (%TemplatesDir%\*.template) do (
    echo "Process %%~nxf"
    sed -e 's/{TEMPLATE-PATH}/%InsertPath%/g' "%%f" > "%%~pnf"
    del "%%f"
)
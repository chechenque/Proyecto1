@echo off
setlocal

echo === LogiTrack Desktop ===
echo Configurando entorno...

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_BIN=py -3
) else (
    set PYTHON_BIN=python
)

echo Python seleccionado: %PYTHON_BIN%

%PYTHON_BIN% -m venv .venv

call .venv\Scripts\activate.bat

python -m pip install --upgrade pip

pip install -r requirements.txt
pip install -r requirements-dev.txt

echo.
echo Entorno configurado correctamente.
echo.
echo Para activar el entorno:
echo .venv\Scripts\activate
echo.
echo Para ejecutar LogiTrack:
echo python -m logitrack
echo.
echo Para ejecutar las pruebas:
echo python -m pytest

endlocal

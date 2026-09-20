#!/bin/bash

set -e

echo "=== LogiTrack Desktop ==="

echo "Configurando entorno..."

PYTHON_BIN="python3"

if command -v python3.12 >/dev/null 2>&1; then

    PYTHON_BIN="python3.12"

fi

echo "Python seleccionado: $PYTHON_BIN"

$PYTHON_BIN -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

pip install -r requirements.txt

pip install -r requirements-dev.txt

echo ""

echo "Entorno configurado correctamente."

echo ""

echo "Para activar el entorno:"

echo "source .venv/bin/activate"

echo ""

echo "Para ejecutar LogiTrack:"

echo "python -m logitrack"

echo ""

echo "Para ejecutar las pruebas:"

echo "python -m pytest"
#!/bin/bash
# @rationale: Ejecuta pre-validaciones, evita subir código basura.
python3 pycodestyle src/
python3 pylint src/

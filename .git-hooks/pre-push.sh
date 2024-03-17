#!/bin/bash
# @rationale: Ejecuta pre-validaciones, evita subir código en mal estado.

CURRENT_BRANCH=$(git symbolic-ref --short head)
pycodestyle src/
STYLE_STATUS=$?
pylint src/
PYLINT_STATUS=$?

if ([ $STYLE_STATUS -eq 0 ] && [ $PYLINT_STATUS -eq 0 ]) || [[ "${CURRENT_BRANCH}" == *"style"* ]];
then
    echo "Controles pasados, se puede hacer push to ${CURRENT_BRANCH}"
    exit 0
else
    echo "Hay errores de estilo de código, no se puede hacer push to ${CURRENT_BRANCH} -- pep8 -> ${STYLE_STATUS} -- pylint -> ${PYLINT_STATUS}"
    exit 1
fi
#!/bin/bash

# Detener en caso de error
set -e

# Variables de entorno
DB_USER="postgres"
DB_PASSWORD="375CheyTac"
DB_NAME="tournament"

echo "Eliminando base de datos existente si existe..."
dropdb --if-exists $DB_NAME -U $DB_USER

echo "Creando nueva base de datos..."
createdb $DB_NAME -U $DB_USER

echo "Eliminando migraciones existentes..."
rm -rf alembic/versions/*

echo "Creando nueva migración inicial..."
alembic revision --autogenerate -m "initial migration"

echo "Aplicando migración..."
alembic upgrade head

echo "Base de datos inicializada correctamente!" 
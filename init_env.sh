#!/usr/bin/env bash

set -euo pipefail

# ENV VARs SET
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env

export AIRFLOW_UID=50000
export AIRFLOW_VERSION="2.8.0"
export AIRFLOW_PROJ_DIR="${PWD}"

# INIT DOCKER AIRFLOW
docker compose up airflow-init --build

exit 0
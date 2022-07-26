#!/usr/bin/env bash
# install.sh
# installs HealthOS components onto a target system.
#
# Arguments:
# BASE_INSTALL_DIRECTORY: the base directory for the installation. Defaults to /opt/healthos
# HEALTHOS_USER: The user account used to run services. Defaults to healthos.
# HEALTHOS_GROUP: The group account used to manage HealthOS software. Defaults to lfh.
set -Eeuo pipefail

BASE_INSTALL_DIRECTORY=${1:-/opt/healthos}
HEALTHOS_USER=${2:-healthos}
HEALTHOS_GROUP=${3:-lfh}

echo "installing OS dependencies"
apt update -y
apt install -y python3 \
               python3.10-venv \
               systemd

echo "Creating user and groups for LinuxForHealth HealthOS . . ."
echo "HealthOS User $HEALTHOS_USER"
echo "HealthOS Group $HEALTHOS_GROUP"

if ! getent passwd "$HEALTHOS_GROUP" > /dev/null 2>&1; then
  addgroup "$HEALTHOS_GROUP"
fi

if ! getent passwd "$HEALTHOS_USER" > /dev/null 2>&1; then
  adduser --disabled-password --ingroup "$HEALTHOS_GROUP" --gecos "" "$HEALTHOS_USER"
fi

HEALTHOS_MODULES=( core )
for module in "${HEALTHOS_MODULES[@]}"
do
  echo "configuring $module module"
  venv_path="$BASE_INSTALL_DIRECTORY"/"$module"/venv
  requirements_path="$BASE_INSTALL_DIRECTORY"/"$module"

  echo "virtual environment path $venv_path"
  python3 -m venv "$venv_path"

  source "$venv_path"/bin/activate && \
    python -m pip install --upgrade pip setuptools && \
    python -m pip install -r "$requirements_path"/requirements.txt
done

echo "Updating owner and groups on HealthOS directories"
chown -R healthos:lfh /opt/healthos

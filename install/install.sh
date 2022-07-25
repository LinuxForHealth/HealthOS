#!/usr/bin/env bash
set -Eeuo pipefail

BASE_INSTALL_DIRECTORY=${1:-/opt/lfh/healthos}
HEALTHOS_GROUP=${2:-healthos}
HEALTHOS_USER=${3-lfh}

echo "Creating LinuxForHealth HealthOS directories in $BASE_INSTALL_DIRECTORY"
mkdir -p "$BASE_INSTALL_DIRECTORY"

HEALTHOS_MODULES=( core )
for module in "${HEALTHOS_MODULES[@]}"
do
  mkdir -p "$BASE_INSTALL_DIRECTORY"/"$module"
done

apt update -y
apt install -y python3 \
               systemd

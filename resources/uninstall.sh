#!/usr/bin/env bash
# uninstall.sh
# removes HealthOS components onto a target system.
#
# Usage:
# install.sh [-d --directory]
# Defaults:
# -d: /opt/healthos

set -Eeuo pipefail

# set defaults for script arguments
directory=/opt/healthos

# handle script arguments
INSTALL_ARGS=$(getopt -o d: --long directory: -- "$@")
eval set -- "$INSTALL_ARGS"

while true; do
  case "$1" in
    -d|--directory)
      directory="$2"
      shift 2
      ;;
    --)
      shift;
      break
      ;;
  esac
done

echo "******************************"
echo "Preparing to uninstall HealthOS"
echo "Uninstall arguments:"
echo "directory = $directory"
echo "******************************"

echo "*******************************"
echo "remove systemd services"
systemctl stop healthos-core.service
rm -f /lib/systemd/system/healthos-core.service
rm -f /lib/systemd/system/nats.service
echo "*******************************"

echo "*******************************"
echo "remove healthos installation directory"
echo "*******************************"

if [[ "$directory" == "/" ]]; then
  "directory is set to /, skipping deletion . . . "
else
  cd /opt && rm -rf "$directory"
fi

echo "*******************************"
echo "remove python 3.10"
echo "*******************************"
apt remove -y python3 python3.10-venv

echo "*******************************"
echo "remove nats-server"
echo "*******************************"
apt remove -y nats-server

echo "*******************************"
echo "tidy up"
echo "*******************************"

apt autoremove -y
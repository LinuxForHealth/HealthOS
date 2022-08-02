#!/usr/bin/env bash
# install.sh
# installs HealthOS components onto a target system.
#
# Usage:
# install.sh [-d --directory] [-u --username] [-g --group] [-n --nats]
# Defaults:
# -d: /opt/healthos
# -u: healthos
# -g: lfh
# -n: https://github.com/nats-io/nats-server/releases/download/v2.8.4/nats-server-v2.8.4-arm64.deb

set -Eeuo pipefail

# set defaults for script arguments
directory=/opt/healthos
username=healthos
group=lfh
nats=https://github.com/nats-io/nats-server/releases/download/v2.8.4/nats-server-v2.8.4-arm64.deb

# handle script arguments
INSTALL_ARGS=$(getopt -o d: --long directory: -- "$@")
eval set -- "$INSTALL_ARGS"

while true; do
  case "$1" in
    -d|--directory)
      directory="$2"
      shift 2
      ;;
    -u|--username)
      username="$2"
      shift 2
      ;;
    -g|--group)
      group="$2"
      shift 2
      ;;
    -n|--nats)
      nats="$2"
      shift 2
      ;;
    --)
      shift;
      break
      ;;
  esac
done

echo "******************************"
echo "Preparing to install HealthOS"
echo "Installation arguments:"
echo "directory = $directory"
echo "username = $username"
echo "group = $group"
echo "nats = $nats"
echo "******************************"

echo "installing OS dependencies"
apt update -y
apt install -y python3 \
               python3.10-venv \
               systemd \
               wget


echo "Creating user and groups for LinuxForHealth HealthOS . . ."
echo "HealthOS User $username"
echo "HealthOS Group $group"

if ! getent passwd "$group" > /dev/null 2>&1; then
  addgroup "$group"
fi

if ! getent passwd "$username" > /dev/null 2>&1; then
  adduser --disabled-password --ingroup "$group" --gecos "" "$username"
fi

healthos_modules=( core )
for module in "${healthos_modules[@]}"
do
  echo "configuring $module module"
  venv_path="$directory"/"$module"/venv
  requirements_path="$directory"/"$module"

  echo "virtual environment path $venv_path"
  python3 -m venv "$venv_path"

  source "$venv_path"/bin/activate && \
    python -m pip install --upgrade pip setuptools && \
    python -m pip install -r "$requirements_path"/requirements.txt
done

echo "Updating owner and groups on HealthOS directories"
chown -R healthos:lfh "$directory"


nats_version=$(nats-server --version || true )

if [[ "$nats_version" != "" ]]; then
  apt remove -y nats-server
fi

echo "installing NATS server"
cd /opt && \
   wget "$nats" && \
   apt install -y ./nats-server* && \
   rm nats-server*

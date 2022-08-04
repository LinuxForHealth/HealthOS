#!/usr/bin/env bash
# install.sh
# installs HealthOS components onto a target system.
#
# Usage:
# install.sh [-d --directory] [-u --username] [-g --group] [-n --nats] [-r --rust]
# Defaults:
# -d: /opt/healthos
# -u: healthos
# -g: lfh
# -n: https://github.com/nats-io/nats-server/releases/download/v2.8.4/nats-server-v2.8.4-arm64.deb
# -r: https://sh.rustup.rs

set -Eeuo pipefail

# set defaults for script arguments
# base install directory
directory=/opt/healthos
# user context associated with healthos services
username=healthos
# group account for LinuxForHealth
group=lfh
# NATS package URL
nats=https://github.com/nats-io/nats-server/releases/download/v2.8.4/nats-server-v2.8.4-arm64.deb
# Rust installation script (required for a uvicorn dependency, watchfiles)
rust=https://sh.rustup.rs

# handle script arguments
INSTALL_ARGS=$(getopt -o d:u:g:n:r: --long directory:username:group:nats:rust: -- "$@")
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
    -r|--rust)
      rust="$2"
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
DEBIAN_FRONTEND=noninteractive apt update -y

# Python and systemd
DEBIAN_FRONTEND=noninteractive apt install -y python3 \
                                              python3.10-venv \
                                              python3-all-dev\
                                              systemd

# compiler toolchain for Rust and Python packages with C/Native extensions
DEBIAN_FRONTEND=noninteractive apt install -y wget \
                                              apt-transport-https \
                                              gnupg2 \
                                              curl \
                                              build-essential \
                                              gcc \
                                              make

echo "Creating user and groups for LinuxForHealth HealthOS . . ."
echo "HealthOS User $username"
echo "HealthOS Group $group"

# add groups if it doesn't exist
cut -d: -f1 /etc/group | grep -i "$group" || addgroup "$group"

# add user account if it doesn't exist
cut -d: -f1 /etc/passwd | grep -i "$username" || adduser --disabled-password --ingroup "$group" --gecos "" "$username"

# install rust (required for uvicorn watchfiles support)
cargo --version || curl "$rust" -sSf | sh -s -- -y
source /root/.cargo/env

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
    python -m pip install "$directory"/"$module"/linuxforhealth_healthos*.whl
done

nats_version=$(nats-server --version || true )

if [[ "$nats_version" != "" ]]; then
  apt remove -y nats-server
fi

echo "installing NATS server"
cd /opt && \
   wget "$nats" && \
   apt install -y ./nats-server* && \
   rm nats-server*

mkdir -p "$directory"/conf
echo "preparing configuration files"

cd "$directory" && \
  mv *.service /lib/systemd/system && \
  mv *.conf healthos-*-config.yml logging.yaml "$directory"/conf

echo "Updating owner and groups on HealthOS directories"
chown -R "$username":"$group" "$directory"

echo "Restoring permissions for systemd"
chown -R root:root /lib/systemd

# install is complete return to our base directory
cd "$directory"

systemctl start healthos-core.service
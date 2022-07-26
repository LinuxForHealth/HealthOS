# HealthOS Build Documentation

The current HealthOS target platform is Ubuntu 22.02, aka the "Jammy" release. HealthOS components are delivered as
a tarball and installed using a shell script.

## Create Installation Package (Tarball)

The following command creates a new "package" in `install/lfh-healthos.tar.gz`

```shell
user HealthOS % make
```

## Install HealthOS Components

First, upload lfh-healthos.tar.gz to the target server's /opt directory.

Next, extract the tarball and run the installation script.
```shell
cd /opt
tar -xvzf lfh-healthos.tar.gz
./healthos/install.sh
```

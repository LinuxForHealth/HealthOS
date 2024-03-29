# HealthOS Build Documentation

The current HealthOS target platform is the Ubuntu 22.02 "Jammy" release. HealthOS components are delivered as
a tarball and installed using a shell script. 

The HealthOS is deployed to the following file structure. 

```shell
user@workstation /opt % tree /opt/healthos
/opt/healthos
├── core
│   ├── healthos-core-config.yml
│   ├── linuxforhealth_healthos_core-0.1.0a1-py3-none-any.whl
│   └── requirements.txt
└── install.sh
```

In the example above, `/opt/healthos` is the base installation directory. HealthOS modules, such as the `core` module
listed above are installed as subdirectories. 

HealthOS modules utilize the same configuration footprint. Common files within each HealthOS module includes:

- healthos-<module name>-config.yml: Configuration settings for the HealthOS module.
- linuxforhealth_healthos_<module name><version>.whl: The distribution file for the HealthOS module.
- requirements.txt: The HealthOS module 3rd party dependencies.

## Install HealthOS on Target Server

First, create a HealthOS package (tarball) using the default `make` target. 

```shell
user@workstation HealthOS % make
```

The target creates a file in `install/lfh-healthos.tar.gz`

Next, upload the tarball to the server.

Once the tarball has been uploaded, extract the contents to the `/opt` directory and run the installation script.
```shell
cd /opt
tar -xvzf lfh-healthos.tar.gz
./healthos/install.sh
```

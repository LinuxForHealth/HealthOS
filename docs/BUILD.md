# HealthOS Build Documentation

The current HealthOS target platform is Ubuntu 22.02, aka the "Jammy" release. HealthOS components are delivered as
a tarball and installed using a shell script. 

The HealthOS is deployed to the following file structure. 

```shell
user@MBP /opt % tree /opt/healthos
/opt/healthos
├── core
│   ├── healthos-core-config.yml
│   ├── linuxforhealth_healthos_core-0.1.0a1-py3-none-any.whl
│   └── requirements.txt
└── install.sh
```

In the example above, `/opt/healthos` is the base installation directory. HealthOS modules, such as the `core` module
listed above are installed as subdirectories. 

HealthOS modules utilize the same configuration footprint. Files within HealthOS modules include:

- healthos-<module name>-config.yml: Configuration settings for the HealthOS module.
- linuxforhealth_healthos_<module name><version>.whl: The distribution file for the HealthOS module.
- requirements.txt: The HealthOS module 3rd party dependencies.


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

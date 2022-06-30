# LinuxForHealth HealthOS

LinuxForHealth HealthOS provides an interoperable open-sourced health stack for developing highly available, standards compliant, and
secure applications and services.

The source code for the HealthOS is split into the following modules:

- core: Base level module used for data acquisition, data processing, and data distribution.
- plugins: Features used to augment core data support, such as de-identification, cohorting, etc.
- sdk: The HealthOS development SDK provides access to HealthOS data and services for application development.
- support: Contains common datatypes and services used across the HealthOS.

## Development Dependencies

The HealthOS development environment depends on the following 3rd party packages:

- [Python 3.10 or higher](https://www.python.org/downloads/) the HealthOS language runtime.
- [Poetry](https://python-poetry.org/) for packaging, dependency management, and publishing support.
- [GNU Make](https://www.gnu.org/software/make/) for component builds.
- [Pyclean](https://pypi.org/project/pyclean/) removes Python bytecode, used as a cross-platform tool in the build process. 

## Build Targets

The HealthOS supports the following build targets

- wheels (default): builds a Python wheel for each module.
- dev_env: creates local development virtual environments, using poetry.
- clean: removes python bytecode and untracked dependencies from each module.

```shell
# executes the wheels target (default) for all modules
make 

# executes the dev_env target for all modules
make dev_env
```

Build targets will operate on all modules, by default. To override this behavior, set and export the TARGET_MODULES variable.
```shell
# multiple modules are delimited by a space
export TARGET_MODULES="support core"
make dev_env
```
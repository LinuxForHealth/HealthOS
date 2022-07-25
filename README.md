# LinuxForHealth HealthOS

LinuxForHealth HealthOS provides an interoperable open-sourced health stack for developing highly available, 
standards compliant, and secure applications and services.

The source code for the HealthOS is split into the following modules:

- core: Base level module used for data acquisition, data processing, and data distribution.
- support: Contains common datatypes and services used across the HealthOS.
- Additional modules TBD

## Development Dependencies

The HealthOS development environment depends on the following 3rd party packages:

- [Python 3.10 or higher](https://www.python.org/downloads/) the HealthOS language runtime.
- [Poetry](https://python-poetry.org/) for packaging, dependency management, and publishing support.
- [GNU Make](https://www.gnu.org/software/make/) for module builds.
- [Pyclean](https://pypi.org/project/pyclean/) removes Python bytecode, used as a cross-platform tool in the build process. 

## Quick Start

The LinuxForHealth HealthOS project is composed of multiple modules, where each module is located within a separate
HealthOS subdirectory. Each module utilizes the same build and development tooling to improve ease of use and simplify
automation.

First use `make` to build the development environments

```shell
make dev-env
```

Once the build is complete, it's time to [get started with HealthOS modules](#Module-Documentation).

## HealthOS Build Targets

The HealthOS supports the following build targets, which execute against one or modules within the "monorepo":

- wheels (default): builds a Python wheel
- test: executes pytest unit tests
- format: runs the black formatter against source code, including unit tests
- dev-env: creates local development virtual environments
- clean: removes python bytecode and untracked dependencies from each module.

```shell
# executes the wheels target (default) for all modules
make 

# executes the dev_env target for all modules
make dev-env
```

Build targets will operate on all modules, by default. To override this behavior, set and export the TARGET_MODULES variable.
```shell
# multiple modules are delimited by a space
export TARGET_MODULES="core <other module> <some other module>"
make dev-env
```

## Common Development Environment
Each HealthOS module utilizes the same tooling and conventions. [Poetry](https://python-poetry.org/) provides
a standard development workflow. The following co

### Dependency Management
To add a dependency to a module, execute the following command:
```shell
poetry add <dependency name>
```

Dependencies are updated using poetry. The `--dry-run` switch may be used to view updates without making actual changes.
```shell
poetry update --dry-run
```

Executing updates:
```shell
# update all project dependencies
poetry update
# update specific dependency
poetry update <dependency>
```


### Code Formatting
The LinuxForHealth HealthOS code base uses the [black formatter](https://black.readthedocs.io/en/stable/).

```shell
poetry run black ./src ./tests
```

### Unit tests 
Use [pytest](https://docs.pytest.org/en/7.1.x/) to execute unit tests

```shell
poetry run pytest
```

### Tidying Up Imports
Use [isort](https://pycqa.github.io/isort/) to clean up the project's imports

```shell
poetry run isort .
```

## Module Documentation

Please consult the following guides for module specific documentation:

- [Core Module](./core/README.md)

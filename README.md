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

## Common Development Environment
Each HealthOS module utilizes the same tooling and conventions. [Poetry](https://python-poetry.org/) is the primary
tool used to provide the standard development workflow. The following sections highlight the common commands used
within a HealthOS module, or "sub-directory".

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

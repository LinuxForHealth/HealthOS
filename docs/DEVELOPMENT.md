# Development Tools

At the project level, the HealthOS provides `make` targets for common processes such as creating virtual environments,
executing unit tests, and formatting code.  

At the module level, [Poetry](https://python-poetry.org/) provides a standard development workflow.

## Make Targets

The HealthOS supports the following build targets, which execute against one or modules within the "monorepo":

- package (default): build the HealthOS installation tarball
- wheels: builds a Python wheel
- test: executes pytest unit tests
- format: runs the black formatter against source code, including unit tests
- dev-env: creates local development virtual environments
- clean: removes python bytecode and untracked dependencies from each module.

Build targets will operate on all modules, by default. To override this behavior, set and export the TARGET_MODULES variable.
The example below runs tests for the `core` module.
```shell
# multiple modules are delimited by a space
export TARGET_MODULES="core"
make test
```

## Poetry Tooling

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

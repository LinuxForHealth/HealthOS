# LinuxForHealth HealthOS

LinuxForHealth HealthOS provides an interoperable open-sourced health stack for developing highly available, 
standards compliant, and secure applications and services.

The HealthOS project is a mono-repo with source code split into separate modules:

- core: Base level module used for data acquisition, data processing, and data distribution.
- Additional modules are coming soon!

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

Once the build is complete, it's time to [review the HealthOS Documentation](#Documentation).

##  Documentation

* [Development Tools](./docs/DEVELOPMENT.md)
* Module Docs
  - [Core Module](./core/README.md)
* [Build Documentation](./docs/BUILD.md)

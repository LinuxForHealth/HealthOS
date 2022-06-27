# LinuxForHealth Core
LinuxForHealth Core provides the foundational services for the LinuxForHealth HealthOS. Services include:

- [Connect](./connect/README.md) provides push and pull interfaces for data acquisition
- [Store](./store/README.md) configurable data storage
- [Sync](./sync/README.md) synchronizes data throughout a LinuxForHealth network 

## Development Tools and Dependencies
LinuxForHealth Core has the following dependencies:

- [Python 3.10](https://www.python.org/downloads/) or higher
- [gnu make](https://www.gnu.org/software/make/)

### Building and Packaging Components

Core components are stored in separate "top level" directories within the project.
```shell
mbp core % tree -d -L 1
.
├── connect
├── store
└── sync
```

#### Create Local Development Environment and run tests

The Makefile provides separate targets for each component's virtual environment build and tests. Targets following the
naming convention clean-<component name>-venv, <component name>-dev-venv, and <component name>-test.

```shell
make clean-connect-venv
make connect-dev-venv
make connect-test
```

#### Local Development IDE Integration

For the best IDE experience:

- Use `make` to create a development virtual environment for each component
- Open the component sub-directory within the IDE and configure the environment accordingly

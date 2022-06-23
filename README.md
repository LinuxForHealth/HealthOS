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

To build a component specify `make build` followed by the component name
```shell
make build COMPONENT_NAME=connect
```

## Core Processing

TODO: Add Core Diagram Processing


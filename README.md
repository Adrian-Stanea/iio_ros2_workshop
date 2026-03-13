# IIO Sensors in ROS2 Workshop

[![ROS2 Humble](https://img.shields.io/badge/ROS2-Humble-blue?logo=ros)](https://docs.ros.org/en/humble/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://hub.docker.com/r/astanea/adi_ros2)

A hands-on workshop for integrating Analog Devices Industrial I/O (IIO) sensors with ROS2. Build a complete ADC data acquisition pipeline using ADI evaluation hardware and the `adi_iio` ROS2 package.

## Overview

This workshop teaches ROS2 concepts through practical exercises with real hardware. You'll work directly with ADI's IIO-based sensor packages to:

- Interact with ADI sensors through ROS2 topics and services
- Automate sensor bringup using launch files
- Create custom ROS2 packages for data processing

### Hardware Requirements

| Component           | Description                                        |
| ------------------- | -------------------------------------------------- |
| **EVAL-AD7124-8**   | 8-channel, 24-bit sigma-delta ADC evaluation board |
| **ADALM2000 (M2K)** | Signal generator for test input signals            |
| **Raspberry Pi 5**  | Running Kuiper Linux with IIO drivers              |
| **PMD-RPI-INTZ**    | Interface board connecting AD7124 to RPi5          |

### Software Requirements

- **Windows**: WSL2, Docker Desktop, VS Code with Dev Containers extension
- **Linux**: Docker, VS Code (optional)
- **Scopy**: For M2K signal generation (Windows/Linux native install)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Adrian-Stanea/iio_ros2_workshop
cd iio_ros2_workshop
```

### 2. Open in VS Code Dev Container

1. Open the folder in VS Code
2. When prompted, click "Reopen in Container"
3. Wait for the container to build and initialize

**Or use Docker Compose directly:**

```bash
# Linux
xhost +local:docker
docker compose up -d
docker compose exec ros2 /ros_entrypoint.sh bash

# Cleanup
docker compose down
```

### 3. Build the Workspace

Inside the container:

```bash
cd /adc_workshop_ws
colcon build
source install/setup.bash
```

### 4. Verify Setup

```bash
# Check ROS2 environment
ros2 topic list

# Start the adi_iio_node (requires hardware connection)
ros2 run adi_iio adi_iio_node --ros-args -p uri:="ip:analog.local"
```

## Workshop Modules

| Module | Title                                                            | Description                                           |
| ------ | ---------------------------------------------------------------- | ----------------------------------------------------- |
| **00** | [Workshop Setup](modules/00-setup/README.md)                     | Development environment and hardware verification     |
| **01** | [Interacting with ADI Sensors](modules/01-adi-sensors/README.md) | ROS2 CLI interaction with adi_iio services and topics |
| **02** | [Sensor Bringup](modules/02-sensor-bringup/README.md)            | Launch files and automated configuration              |
| **03** | [Processing Package](modules/03-processing-package/README.md)    | Custom ROS2 package for data processing               |

## Project Structure

```
iio_ros2_workshop/
├── .devcontainer/              # VS Code Dev Container config
├── modules/
│   ├── 00-setup/               # Environment setup guides
│   ├── 01-adi-sensors/         # CLI interaction exercises
│   ├── 02-sensor-bringup/      # Launch file package
│   │   └── ad7124_workshop/    # ROS2 package with launch files
│   └── 03-processing-package/  # Processing node exercises
├── compose.yaml                # Docker Compose configuration
└── README.md
```

## Resources

| Resource                  | Description                                                |
| ------------------------- | ---------------------------------------------------------- |
| `HANDBOOK.md`             | Main workshop guide for following the session step by step |
| `solutions/checkpoint.md` | Expected outputs and solutions                             |

> NOTE: The branch `solutions` holds tips and reference material for working through each module when you need extra guidance.
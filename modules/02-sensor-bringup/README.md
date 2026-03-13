# Module 2: Sensor Bringup with Launch Files

## Overview

Learn how to automate sensor configuration and data streaming using ROS2 launch files. This module builds on Module 1's manual CLI interaction by teaching you to orchestrate multiple operations through composable, event-driven launch files.

## Prerequisites

- Module 1 completed (understanding of adi_iio services)
- AD7124-8 ADC connected to Raspberry Pi 5
- Devcontainer environment running
- Basic Python familiarity

## Module Contents

| File                | Purpose                            |
| ------------------- | ---------------------------------- |
| `hands-on-guide.md` | Step-by-step practical guide       |
| `exercises/`        | Challenge-based exercises          |
| `ad7124_workshop/`  | ROS2 package with launch templates |

## Learning Objectives

By the end of this module, you will be able to:

1. Understand ROS2 launch file structure and Python launch API
2. Use `IncludeLaunchDescription` to compose launch files
3. Apply event-driven orchestration with `RegisterEventHandler`
4. Separate configuration from code using YAML parameter files
5. Debug launch sequences using standard ROS2 CLI tools

## Key Concepts

### Launch File Composition

Instead of running commands manually, launch files automate the entire bringup:

```
bringup.launch.py
    ├── Start adi_iio_node
    ├── Run config_attributes.launch.py (after node starts)
    └── Run buffer_setup.launch.py (after config completes)
```

### Event-Driven Orchestration

Launch files can react to process events:

- `OnProcessStart`: Trigger actions when a Node or process starts
- `OnProcessExit`: Trigger actions when an ExecuteProcess exits
- `OnExecutionComplete`: Trigger actions when an IncludeLaunchDescription completes

### YAML Configuration

Parameters are externalized to YAML files, separating configuration from code:

```yaml
adi_iio_node:
  ros__parameters:
    uri: "ip:analog.local"
```

## Hands-on Parts

1. **Introduction** (5 min) - Launch file concepts
2. **Explore the Package** (10 min) - Build and examine ad7124_workshop
3. **Run Baseline** (5 min) - Test bringup with just the node
4. **Exercise 1: Config Challenge** (15 min) - Complete attribute configuration
5. **Test Config** (5 min) - Verify attributes are set
6. **Exercise 2: Buffer Challenge** (10 min) - Complete buffer setup
7. **Test Buffer** (5 min) - Verify topic streaming
8. **Exercise 3: Verification** (10 min) - Diagnostic walkthrough

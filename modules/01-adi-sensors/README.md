# Module 1: Interacting with ADI Sensors via ROS2

## Overview

Learn how to interact with ADI sensors using the `adi_iio` ROS2 package. Unlike typical ROS2 drivers that auto-publish data, `adi_iio_node` uses a **services-first architecture** - topics are created on demand.

## Prerequisites

- Module 0 completed (Docker environment verified)
- AD7124-8 ADC connected to Raspberry Pi 5
- Basic terminal comfort

## Module Contents

| File                | Purpose                      |
| ------------------- | ---------------------------- |
| `hands-on-guide.md` | Step-by-step practical guide |
| `exercises/`        | Challenge-based exercises    |

## Key Concept: IIO Paths

All adi_iio services use a path-based addressing system:

```
device/channel/attribute

Examples:
  "ad7124-8"                              → Device
  "ad7124-8/input_voltage0-voltage1"      → Channel
  "ad7124-8/input_voltage0-voltage1/raw"  → Attribute
```

## Hands-on Parts

1. **Discovery & IIO Paths** (10 min) - Explore devices and channels
2. **Read Attributes** (5 min) - Query device configuration
3. **Write Attributes** (5 min) - Configure sampling frequency
4. **Enable Attribute Topics** (10 min) - Create topics on demand
5. **Buffer Topics** (10 min) - High-performance multi-sample streaming

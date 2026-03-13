# Module 2: Hands-on Guide

## Sensor Bringup with Launch Files

## Before You Begin

> **Note:** This guide assumes you are running inside the **devcontainer**. If you haven't opened the project in VS Code with the devcontainer, do so now (Command Palette → "Dev Containers: Reopen in Container"). In this environment, the repository root is also the ROS 2 workspace root. If a terminal does not pick up the workspace overlay after a build, run `source install/setup.bash` once and continue.

### Terminal Setup

You'll need **two terminals** for this hands-on session:

- **Terminal 1:** Runs the launch files
- **Terminal 2:** Runs verification commands

Open two terminals in VS Code (Ctrl+Shift+` or Terminal → New Terminal).


## Part 1: Introduction (5 min)

### Why Launch Files?

In Module 1, we manually ran multiple commands to:

1. Start the adi_iio_node

2. Configure channel attributes

3. Create buffers and enable topics

**Launch files automate this entire workflow** into a single command.

### What You'll Build

```
bringup.launch.py (orchestrator)
    │
    ├── Start adi_iio_node (with YAML config)
    │
    ├── OnProcessStart → config_attributes.launch.py
    │   └── Set scale and sampling_frequency for channels
    │
    └── OnExecutionComplete → buffer_setup.launch.py
        └── Create buffer and enable topic
```


## Part 2: Explore the Package (10 min)

### Step 2.1: Navigate to Package

From the workspace root, go to the `ad7124_workshop` package in `module 02-sensor-bringup`:

### Step 2.2: Examine Package Structure

**Relevant files:**
```
CMakeLists.txt
config/
launch/
package.xml
```

### Step 2.3: View the YAML Config

**Expected content:**
```yaml
adi_iio_node:
  ros__parameters:
    uri: "ip:analog.local"
```

> **Action:** Update the `uri` value to match your Raspberry Pi's address if needed.

### Step 2.4: Build the Package

Return to the workspace root, then build the package:

```bash
colcon build --symlink-install --packages-select ad7124_workshop
```

**Expected output:**
```
Starting >>> ad7124_workshop
Finished <<< ad7124_workshop [0.5s]

Summary: 1 package finished [0.7s]
```

### Step 2.5: Understand Workspace Overlay & Environment Setup

In ROS 2, an **overlay** means your workspace install is layered on top of the base ROS environment, so newly built packages become discoverable by ROS tools.

After building, run:

```bash
source install/setup.bash
```

This updates your current terminal environment to include packages from this workspace (for example, `ad7124_workshop`).

> **Note:** In this devcontainer, new terminals are configured to automatically look for workshop package installs and source them when available. So you usually do **not** need to run `source install/setup.bash` every time. A common case where manual sourcing is needed: you opened a terminal **before** `install/` existed, then built afterward.

### Step 2.6: Verify Installation

```bash
ros2 pkg list | grep ad7124
```

**Expected output:**
```
ad7124_workshop
```


## Part 3: Run Baseline (5 min)

### Step 3.1: Examine the Bringup Launch File

Open `module 02-sensor-bringup/ad7124_workshop/launch/bringup.launch.py`.

Notice the structure:

1. Loads YAML config

2. Creates adi_iio_node with parameters

3. Registers event handlers for sequencing

### Step 3.2: Run the Bringup (Terminal 1)

```bash
ros2 launch ad7124_workshop bringup.launch.py
```

**Expected output:**
```
[INFO] [launch]: All log files can be found below ...
[INFO] [launch]: Default logging verbosity is set to INFO
[INFO] [adi_iio_node-1]: process started with pid [12345]
[adi_iio_node-1] [INFO] [...] [adi_iio_node]: creating context...
```

### Step 3.3: Verify Node is Running (Terminal 2)

```bash
ros2 node list
```

**Expected output:**
```
/adi_iio_node
```

### Step 3.4: Check Service Calls Executed

You should see log messages indicating the service calls were made:

```
[ros2-2] response: ...AttrWriteString_Response(success=True...
```

> **Note:** Currently only the scale for channel 0 is configured. The other attributes need YOUR implementation!

Press `Ctrl+C` in Terminal 1 to stop.


## Part 4: Exercise 1 - Config Challenge (15 min)

**Goal:** Complete `config_attributes.launch.py` to configure all attributes.

### Step 4.1: Open the Launch File

Open `config_attributes.launch.py` from the `ad7124_workshop/launch` directory in the `module 02-sensor-bringup` package.

### Step 4.2: Review What's Complete

The file already configures **scale for channel 0**:

```python
ch0_scale = ExecuteProcess(
    cmd=[[
        FindExecutable(name='ros2'),
        ' service call ',
        '/adi_iio_node/AttrWriteString ',
        'adi_iio/srv/AttrWriteString ',
        '"{attr_path: \'ad7124-8/input_voltage0-voltage1/scale\', ',
        f"value: '{scale}'}}\"",
    ]],
    shell=True,
)
```

### Step 4.3: Discover Available Attributes

Use the running workshop package to inspect the available attributes.

In Terminal 1, start the baseline bringup again:

```bash
ros2 launch ad7124_workshop bringup.launch.py
```

Then, in Terminal 2, list the attributes for channel 0:

```bash
ros2 service call /adi_iio_node/ListAttributes adi_iio/srv/ListAttributes \
  "{iio_path: 'ad7124-8/input_voltage0-voltage1'}"
```

**Look for:** `sampling_frequency` in the list

When you're done inspecting the attributes, stop the bringup in Terminal 1 with `Ctrl+C`.

### Step 4.4: Complete the TODOs

You need to add:

1. **ch0_sampling_freq** - Set sampling_frequency for channel 0

2. **ch1_scale** - Set scale for channel 1 (input_voltage2-voltage3)

3. **ch1_sampling_freq** - Set sampling_frequency for channel 1

**Pattern to follow:**
```python
ch0_sampling_freq = ExecuteProcess(
    cmd=[[
        FindExecutable(name='ros2'),
        ' service call ',
        '/adi_iio_node/AttrWriteString ',
        'adi_iio/srv/AttrWriteString ',
        '"{attr_path: \'ad7124-8/input_voltage0-voltage1/sampling_frequency\', ',
        f"value: '{sampling_frequency}'}}\"",
    ]],
    shell=True,
)
```

### Step 4.5: Update the Return Statement

Don't forget to add your new variables to the LaunchDescription:

```python
return LaunchDescription([
    ch0_scale,
    ch0_sampling_freq,  # Add this
    ch1_scale,          # Add this
    ch1_sampling_freq,  # Add this
])
```

### Step 4.6: Rebuild and Test

From the workspace root:

```bash
colcon build --symlink-install --packages-select ad7124_workshop
```


## Part 5: Test Config (5 min)

### Step 5.1: Run the Bringup (Terminal 1)

```bash
ros2 launch ad7124_workshop bringup.launch.py
```

### Step 5.2: Verify Attributes (Terminal 2)

Check that both channels are configured:

```bash
# Channel 0 scale
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString \
  "{attr_path: 'ad7124-8/input_voltage0-voltage1/scale'}"

# Channel 0 sampling_frequency
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString \
  "{attr_path: 'ad7124-8/input_voltage0-voltage1/sampling_frequency'}"

# Channel 1 scale
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString \
  "{attr_path: 'ad7124-8/input_voltage2-voltage3/scale'}"

# Channel 1 sampling_frequency
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString \
  "{attr_path: 'ad7124-8/input_voltage2-voltage3/sampling_frequency'}"
```

**Expected:** All return `success=True` with configured values.

Press `Ctrl+C` to stop before continuing.


## Part 6: Exercise 2 - Buffer Challenge (10 min)

**Goal:** Complete `buffer_setup.launch.py` to enable buffer topic streaming.

### Step 6.1: Open the Launch File

Open `buffer_setup.launch.py` from the `ad7124_workshop/launch` directory in the `module 02-sensor-bringup` package.

### Step 6.2: Review What's Complete

The file already creates the buffer:

```python
buffer_create = ExecuteProcess(
    cmd=[[
        FindExecutable(name='ros2'),
        ' service call ',
        '/adi_iio_node/BufferCreate ',
        'adi_iio/srv/BufferCreate ',
        f"\"{{device_path: '{device_path}', ",
        f"channels: ['{channel}'], ",
        f"samples_count: {samples_count}}}\"",
    ]],
    shell=True,
)
```

### Step 6.3: Check the BufferEnableTopic Interface

```bash
ros2 interface show adi_iio/srv/BufferEnableTopic
```

**Expected output:**
```
string device_path
string topic_name
float64 loop_rate 1.0
---
bool success
string message
```

### Step 6.4: Complete the TODO

Add the `buffer_enable_topic` ExecuteProcess:

```python
buffer_enable_topic = ExecuteProcess(
    name='buffer_enable_topic',
    cmd=[[
        FindExecutable(name='ros2'),
        ' service call ',
        '/adi_iio_node/BufferEnableTopic ',
        'adi_iio/srv/BufferEnableTopic ',
        f"\"{{device_path: '{device_path}', ",
        f"topic_name: '{topic_name}', ",
        f"loop_rate: {loop_rate}}}\"",
    ]],
    shell=True,
    output='screen',
)
```

### Step 6.5: Add Sequencing

**Important:** BufferEnableTopic must run AFTER BufferCreate completes.

> **Note:** For `ExecuteProcess` actions, use `OnProcessExit` (not `OnExecutionComplete` which is for `IncludeLaunchDescription`).

```python
on_buffer_created = RegisterEventHandler(
    OnProcessExit(
        target_action=buffer_create,
        on_exit=[buffer_enable_topic],
    )
)
```

### Step 6.6: Update the Return Statement

```python
return LaunchDescription([
    buffer_create,
    on_buffer_created,
])
```

### Step 6.7: Rebuild

```bash
colcon build --symlink-install --packages-select ad7124_workshop
```


## Part 7: Test Buffer (5 min)

### Step 7.1: Run Full Bringup (Terminal 1)

```bash
ros2 launch ad7124_workshop bringup.launch.py
```

### Step 7.2: Verify Topic Exists (Terminal 2)

```bash
ros2 topic list | grep ad7124
```

**Expected output:**
```
/ad7124_buffer
```

### Step 7.3: Echo Buffer Data

```bash
ros2 topic echo /ad7124_buffer --once
```

**Expected output:**
```yaml
layout:
  dim:
  - label: samples
    size: 1024
    stride: 1024
  - label: channels
    size: 1
    stride: 1
  data_offset: 0
data:
- 1682586
- 1683546
...
```

### Step 7.4: Check Topic Rate

```bash
ros2 topic hz /ad7124_buffer
```

**Expected output:**
```
average rate: 10.012
        min: 0.095s max: 0.105s std dev: 0.00257s
```


## Part 8: Exercise 3 - Verification & Diagnostics (10 min)

**Goal:** Learn the systematic verification process for launch file bringup.

### Verification Checklist

Use this checklist to verify your system is working correctly:

| Check                 | Command                                 | Expected Result            |
| --------------------- | --------------------------------------- | -------------------------- |
| Node running          | `ros2 node list`                        | `/adi_iio_node` present    |
| Services available    | `ros2 service list \| grep adi_iio`     | All services listed        |
| Attributes configured | `ros2 service call .../AttrReadString`  | Returns configured values  |
| Buffer topic exists   | `ros2 topic list`                       | `/ad7124_buffer` present   |
| Data streaming        | `ros2 topic echo /ad7124_buffer --once` | MultiArray with samples    |
| Topic rate            | `ros2 topic hz /ad7124_buffer`          | ~10 Hz (matches loop_rate) |


## Summary

### What You Learned

1. **Launch file structure** - Python-based declarative orchestration
2. **Event handlers** - OnProcessStart, OnExecutionComplete for sequencing
3. **YAML configuration** - Separating parameters from code
4. **Service calls in launch** - ExecuteProcess for automation
5. **Debugging tools** - ros2 node/service/topic commands

### Complete Workflow

```bash
# After building ad7124_workshop
ros2 launch ad7124_workshop bringup.launch.py
```

**You've automated what took multiple manual steps in Module 1!**

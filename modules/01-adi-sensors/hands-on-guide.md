# Module 1: Hands-on Guide

## Interacting with ADI Sensors via ROS2

## Before You Begin

> **Note:** This guide assumes you are running inside the **devcontainer**. If you haven't opened the project in VS Code with the devcontainer, do so now (Command Palette → "Dev Containers: Reopen in Container").

### Terminal Setup

You'll need **two terminals** for this hands-on session:

- **Terminal 1:** Runs the adi_iio_node
- **Terminal 2:** Runs commands to interact with the node

Open two terminals in VS Code (`Ctrl+Shift+`` or Terminal → New Terminal).

### Terminal 1: Start the IIO Node

```bash
ros2 run adi_iio adi_iio_node --ros-args -p uri:=ip:<RPI_URI>
```

**Expected output:**
```bash
[INFO] [1773217697.732463206] [adi_iio_node]: creating context 0x555649362530 from uri local:
[INFO] [1773217697.732843077] [adi_iio_node]: setting timeout to 0
[INFO] [1773217697.733033374] [rclcpp]: Initializing buffers...
[INFO] [1773217697.736300098] [adi_iio_node]: IIO Node
```

Keep this terminal running throughout the hands-on session.

### Terminal 2: Command Terminal

Open a second terminal. All commands in the following sections are run from **Terminal 2**.

---

<details>
<summary><strong>Alternative: Running with Docker Compose (without devcontainer)</strong></summary>

If you're not using the devcontainer (e.g., running directly on a target device), you can use Docker Compose:

```bash
# Set architecture variable
export ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')

# Start the container in background
docker compose up -d

# Terminal 1: Start the node
docker compose exec ros2 /ros_entrypoint.sh bash
ros2 run adi_iio adi_iio_node --ros-args --log-level info

# Terminal 2: Open a second shell
docker compose exec ros2 /ros_entrypoint.sh bash
```

This approach is useful for:
- Running on embedded targets (Raspberry Pi, Jetson)
- Deploying specific node configurations
- Testing without VS Code

</details>

---

### Verify Initial State

Check the initial topic list:

```bash
ros2 topic list
```

**Expected output:**
```bash
/parameter_events
/rosout
```

Note: No sensor data topics yet! This is the services-first architecture in action.

---

## Part 1: Discovery & IIO Paths (15 min)

**Goal:** Understand the IIO path hierarchy and discover available devices/channels/attributes

**ROS2 Concept:** Services = request/response pattern

### Step 1.1: List Available Services

```bash
ros2 service list
```

**Expected output:**
```bash
/adi_iio_node/AttrDisableTopic
/adi_iio_node/AttrEnableTopic
/adi_iio_node/AttrReadString
/adi_iio_node/AttrWriteString
/adi_iio_node/BufferCreate
...
```

### Step 1.2: Scan the IIO Context

The IIO context represents all connected IIO devices. This gives you a complete overview:

```bash
ros2 service call /adi_iio_node/ScanContext adi_iio/srv/ScanContext
```

**Expected output:**
```bash
response:
adi_iio.srv.ScanContext_Response(success=True, message='Found: Context attributes:
2; Devices: 6; Channels: 17; Device attributes: 1; Channel attributes: 63; ',
devices=['cpu_thermal', 'rp1_adc', 'pwmfan', 'rpi_volt', 'ad7124-8', 'ad7124-8-dev0'],
channels=['cpu_thermal/input_temp1', 'rp1_adc/input_in4', ...
'ad7124-8/input_voltage0-voltage1', 'ad7124-8/input_voltage2-voltage3', ...], ...)
```

Notice that the Raspberry Pi 5 exposes several IIO devices:

- `cpu_thermal` - CPU temperature sensor

- `rp1_adc` - Built-in ADC

- `pwmfan` - PWM fan control

- `rpi_volt` - Voltage monitor

- `ad7124-8` - Our external ADC (the one we're working with)

### Step 1.3: List IIO Devices

For a cleaner view of just the device names:

```bash
ros2 service call /adi_iio_node/ListDevices adi_iio/srv/ListDevices
```

**Expected output:**
```bash
response:
adi_iio.srv.ListDevices_Response(success=True, message='Found 6 devices', data=['cpu_thermal', 'rp1_adc', 'pwmfan', 'rpi_volt', 'ad7124-8', 'ad7124-8-dev0'])
```

You should see `ad7124-8` in the list - this is our ADC.

### Step 1.4: List Channels for AD7124

Now let's see what channels the AD7124-8 has:

```bash
ros2 service call /adi_iio_node/ListChannels adi_iio/srv/ListChannels "{iio_path: 'ad7124-8'}"
```

**Expected output:**
```bash
response:
adi_iio.srv.ListChannels_Response(success=True, message='Found 9 channels in device: ad7124-8', data=['ad7124-8/input_voltage0-voltage1', 'ad7124-8/input_voltage2-voltage3', 'ad7124-8/input_voltage4-voltage5', 'ad7124-8/input_voltage6-voltage7', 'ad7124-8/input_voltage8-voltage9', 'ad7124-8/input_voltage10-voltage11', 'ad7124-8/input_voltage12-voltage13', 'ad7124-8/input_voltage14-voltage15', 'ad7124-8/input_temp'])
```

The AD7124-8 has **8 differential channels**:
- `input_voltage0-voltage1` = AIN0 - AIN1
- `input_voltage2-voltage3` = AIN2 - AIN3
- ... and so on

### Step 1.5: List Attributes for a Channel

Let's explore what we can read/write on a channel:

```bash
ros2 service call /adi_iio_node/ListAttributes adi_iio/srv/ListAttributes "{iio_path: 'ad7124-8/input_voltage0-voltage1'}"
```

**Expected output:**
```bash
response:
adi_iio.srv.ListAttributes_Response(success=True, message='Found 11 attributes in channel: input_voltage0-voltage1', data=['ad7124-8/input_voltage0-voltage1/filter_low_pass_3db_frequency', 'ad7124-8/input_voltage0-voltage1/filter_type', 'ad7124-8/input_voltage0-voltage1/filter_type_available', 'ad7124-8/input_voltage0-voltage1/offset', 'ad7124-8/input_voltage0-voltage1/raw', 'ad7124-8/input_voltage0-voltage1/sampling_frequency', 'ad7124-8/input_voltage0-voltage1/scale', 'ad7124-8/input_voltage0-voltage1/scale_available', 'ad7124-8/input_voltage0-voltage1/sys_calibration', 'ad7124-8/input_voltage0-voltage1/sys_calibration_mode', 'ad7124-8/input_voltage0-voltage1/sys_calibration_mode_available'])
```

**Key attributes:**

| Attribute                       | Description                    |
| ------------------------------- | ------------------------------ |
| `raw`                           | Raw ADC reading (24-bit value) |
| `scale`                         | Conversion factor to voltage   |
| `sampling_frequency`            | Current sample rate in Hz      |
| `offset`                        | Offset calibration value       |
| `filter_low_pass_3db_frequency` | Anti-aliasing filter cutoff    |

### Checkpoint: IIO Path Understanding

You've now learned the IIO path hierarchy:

| Path                                   | Type      | Example                |
| -------------------------------------- | --------- | ---------------------- |
| `ad7124-8`                             | Device    | The ADC itself         |
| `ad7124-8/input_voltage0-voltage1`     | Channel   | Differential input 0-1 |
| `ad7124-8/input_voltage0-voltage1/raw` | Attribute | Raw ADC reading        |

---

## Part 2: Read Attributes (10 min)

**Goal:** Query current device configuration

**ROS2 Concept:** Service request with parameters

### Step 2.1: Read the Raw ADC Value

```bash
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString "{attr_path: 'ad7124-8/input_voltage0-voltage1/raw'}"
```

**Expected output:**
```bash
response:
adi_iio.srv.AttrReadString_Response(success=True, message='8388552')
```

### Step 2.2: Read the Scale Factor

```bash
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString "{attr_path: 'ad7124-8/input_voltage0-voltage1/scale'}"
```

**Expected output:**
```bash
response:
adi_iio.srv.AttrReadString_Response(success=True, message='0.000149011')
```

Hint: To convert raw to voltage: `voltage = raw * scale`

### Step 2.3: Read Current Sampling Frequency

```bash
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString "{attr_path: 'ad7124-8/input_voltage0-voltage1/sampling_frequency'}"
```

**Expected output:**
```bash
response:
adi_iio.srv.AttrReadString_Response(success=True, message='10.000000000')
```

The default sampling frequency is 10 Hz.

### Checkpoint: Reading Attributes

You can now read any attribute using the pattern:
```bash
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString "{attr_path: '<device>/<channel>/<attribute>'}"
```

---

## Part 3: Write Attributes (10 min)

**Goal:** Configure the ADC (change sampling frequency)

**ROS2 Concept:** Service request to modify hardware state

### Step 3.1: Read Current Sampling Frequency

First, check the current value:

```bash
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString "{attr_path: 'ad7124-8/input_voltage0-voltage1/sampling_frequency'}"
```

Note the current value (default is 10 Hz).

### Step 3.2: Write New Sampling Frequency

Let's change it to 19200 Hz:

```bash
ros2 service call /adi_iio_node/AttrWriteString adi_iio/srv/AttrWriteString "{attr_path: 'ad7124-8/input_voltage0-voltage1/sampling_frequency', value: '19200'}"
```

**Expected output:**
```bash
response:
adi_iio.srv.AttrWriteString_Response(success=True, message='4800.000000000')
```

NOTE: the driver may adjust the requested frequency to the nearest supported value. In this case, it set it to 4800 Hz.

### Step 3.3: Verify the Change

Read it back to confirm:

```bash
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString "{attr_path: 'ad7124-8/input_voltage0-voltage1/sampling_frequency'}"
```

**Expected output:**
```bash
response:
adi_iio.srv.AttrReadString_Response(success=True, message='4800.000000000')
```

### Checkpoint: Writing Attributes

You can now configure the ADC using:
```bash
ros2 service call /adi_iio_node/AttrWriteString adi_iio/srv/AttrWriteString "{attr_path: '<path>', value: '<value>'}"
```

---

## Part 4: Enable Attribute Topics (15 min)

**Goal:** Create ROS2 topics from IIO attributes - THE BRIDGE between services and topics

**ROS2 Concept:** Topics = continuous pub/sub (created on demand via services)

### Step 4.1: Check Current Topics

```bash
ros2 topic list
```

**Expected output:** (still minimal)
```bash
/parameter_events
/rosout
```

### Step 4.2: Examine the AttrEnableTopic Service

```bash
ros2 interface show adi_iio/srv/AttrEnableTopic
```

**Expected output:**
```bash
int8 STRING = 0
int8 INT = 1
int8 DOUBLE = 2
int8 BOOL = 3

string attr_path
string topic_name ""
float64 loop_rate 1.0
int8 type 0 # String: 0, Int: 1, Double: 2, Bool: 3
---
bool success
string message
```

The interface supports different data types and an optional custom topic name.

### Step 4.3: Enable Topic for Raw Attribute

Create a topic that publishes the raw ADC value at 10 Hz:

```bash
ros2 service call /adi_iio_node/AttrEnableTopic adi_iio/srv/AttrEnableTopic "{attr_path: 'ad7124-8/input_voltage0-voltage1/raw', loop_rate: 10.0}"
```

**Expected output:**
```bash
response:
adi_iio.srv.AttrEnableTopic_Response(success=True, message='Success')
```

### Step 4.4: Verify Topic Was Created

```bash
ros2 topic list
```

**Expected output:** (NEW topics appear - both read AND write!)
```bash
/ad7124_8/input_voltage0_voltage1/raw/read
/ad7124_8/input_voltage0_voltage1/raw/write
/parameter_events
/rosout
```

**Note:** The topic name converts hyphens to underscores (`ad7124-8` becomes `ad7124_8`).

### Step 4.5: Echo the Topic Data

```bash
ros2 topic echo /ad7124_8/input_voltage0_voltage1/raw/read
```

**Expected output:** (continuous stream)
```bash
data: '3356827'
---
data: '3356827'
---
data: '3356827'
---
```

Press `Ctrl+C` to stop.

### Step 4.6: Measure Topic Frequency

```bash
ros2 topic hz /ad7124_8/input_voltage0_voltage1/raw/read
```

**Expected output:**
```bash
average rate: 10.012
        min: 0.095s max: 0.105s std dev: 0.00257s window: 12
```

The rate should be approximately 10 Hz as configured.

### Step 4.7: Enable a Second Topic (Optional)

You can enable multiple attribute topics simultaneously:

```bash
ros2 service call /adi_iio_node/AttrEnableTopic adi_iio/srv/AttrEnableTopic "{attr_path: 'ad7124-8/input_voltage2-voltage3/raw', loop_rate: 10.0}"
```

### Checkpoint: Dynamic Topic Creation

You've learned the key concept: **services create topics on demand**

| Before AttrEnableTopic   | After AttrEnableTopic                    |
| ------------------------ | ---------------------------------------- |
| No data topics           | `/ad7124_8/.../raw/read` at 10 Hz        |
| Service-only interaction | Topics for continuous streaming          |
|                          | Both `/read` and `/write` topics created |

---

## Part 5: Buffer Topics (10 min)

**Goal:** High-performance multi-channel data streaming

Buffer topics provide bulk data transfer - capturing multiple samples in a single message.

### Step 5.1: Examine Buffer Services

Buffer topics require a two-step process:

```bash
# First, examine BufferCreate interface
ros2 interface show adi_iio/srv/BufferCreate
```

**Expected output:**
```bash
string device_path
string[] channels
int32 samples_count
---
bool success
string message
std_msgs/MultiArrayLayout layout
        MultiArrayDimension[] dim
                string label
                uint32 size
                uint32 stride
        uint32 data_offset
```

```bash
# Then examine BufferEnableTopic interface
ros2 interface show adi_iio/srv/BufferEnableTopic
```

**Expected output:**
```bash
string device_path
string topic_name
float64 loop_rate 1.0
---
bool success
string message
```

### Step 5.2: Create a Buffer

Create the buffer specifying channels to capture. **Important:** Use channel names WITHOUT the device prefix:

```bash
ros2 service call /adi_iio_node/BufferCreate adi_iio/srv/BufferCreate "{device_path: 'ad7124-8', channels: ['input_voltage0-voltage1'], samples_count: 1024}"
```

**Expected output:**
```bash
response:
adi_iio.srv.BufferCreate_Response(success=True, message='Success', layout=std_msgs.msg.MultiArrayLayout(dim=[std_msgs.msg.MultiArrayDimension(label='samples', size=1024, stride=1024), std_msgs.msg.MultiArrayDimension(label='channels', size=1, stride=1)], data_offset=0))
```

The response includes the layout: 1024 samples x 1 channel.

### Step 5.3: Enable Buffer Topic

Enable the topic to publish buffer data:

```bash
ros2 service call /adi_iio_node/BufferEnableTopic adi_iio/srv/BufferEnableTopic "{device_path: 'ad7124-8', topic_name: '/ad7124_buffer', loop_rate: 10.0}"
```

**Expected output:**
```bash
response:
adi_iio.srv.BufferEnableTopic_Response(success=True, message='Success')
```

### Step 5.4: Verify Topic Was Created

```bash
ros2 topic list
```

**Expected output:**
```bash
/ad7124_buffer
/parameter_events
/rosout
```

### Step 5.5: Echo Buffer Data

```bash
ros2 topic echo /ad7124_buffer --once
```

**Expected output:** (128 samples in one message)
```bash
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
- 1683546
...
---
```

### When to Use Buffer Topics

| Use Case                    | Recommended Approach |
| --------------------------- | -------------------- |
| Learning/debugging          | Attribute topics     |
| Single channel monitoring   | Attribute topics     |
| Multi-channel acquisition   | Buffer topics        |
| High sample rates (>100 Hz) | Buffer topics        |

---

## Summary

### What You Learned

1. **Services-First Architecture:** adi_iio uses services for all interaction, topics are created on demand
2. **IIO Paths:** `device/channel/attribute` hierarchical addressing system
3. **Discovery:** Use `ScanContext`, `ListDevices`, `ListChannels`, `ListAttributes`
4. **Read/Write:** Use `AttrReadString`, `AttrWriteString` to query and configure the ADC
5. **Attribute Topics:** Use `AttrEnableTopic` to create continuous data streams from single attributes
6. **Buffer Topics:** Use `BufferCreate` + `BufferEnableTopic` for high-performance multi-sample streaming

### Quick Reference

Refer to the official documentation for service API details and usage:

- [iio_ros2 Services API and Node Overview](https://analogdevicesinc.github.io/iio_ros2/#services): API reference for available services, node behavior, and architecture.
- [iio_ros2 CLI Service Call Reference](https://analogdevicesinc.github.io/iio_ros2/doc/Examples/01_service_call_reference.html): CLI examples showing how to call services step by step.
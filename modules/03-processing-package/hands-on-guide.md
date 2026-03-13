# Module 3: Hands-on Guide

## Creating a Data Processing Package

## Before You Begin

> **Note:** This guide assumes you are running inside the **devcontainer**. If you haven't opened the project in VS Code with the devcontainer, do so now (Command Palette → "Dev Containers: Reopen in Container"). In this environment, the repository root is also the ROS 2 workspace root. If a terminal does not pick up the workspace overlay after a build, run `source install/setup.bash` once and continue.

### Terminal Setup

You'll need **three terminals** for this hands-on session:

- **Terminal 1:** Runs Module 02's launch file (keeps running)
- **Terminal 2:** Build and run your package (iterate here)
- **Terminal 3:** Validation commands (topic echo, rqt_graph, etc.)

Open three terminals in VS Code (Ctrl+Shift+` or Terminal → New Terminal).


## Prerequisite Verification

Before starting, verify Module 02 is working:

```bash
ros2 launch ad7124_workshop bringup.launch.py
```

In another terminal:

```bash
ros2 topic echo /ad7124_buffer --once
```

**Expected:** Int32MultiArray with data. Press Ctrl+C in both terminals when verified.


## Part 1: Introduction (5 min)

### Why Processing Packages?

In Module 2, we created a complete data acquisition pipeline:

1. adi_iio_node publishes raw ADC counts → `/ad7124_buffer`
2. Launch file orchestrates configuration
3. But the data is still in raw counts, not in human-readable units!

**Processing packages transform data** from one representation to another, enabling downstream analysis and visualization.

### What You'll Build

```
adi_iio_node → /ad7124_buffer (raw counts)
    │
    └─→ adc_processor_node → /ad7124_buffer/mV (millivolts)
```

**By the end of this module:**
- Create a new ROS 2 Python package
- Subscribe to `/ad7124_buffer`, transform via service call
- Publish scaled voltage to `/ad7124_buffer/mV`
- Integrate into the existing launch file


## Development Workflow

Throughout this module, use this iterative pattern:

**Terminal 1 (constant):**
```bash
ros2 launch ad7124_workshop bringup.launch.py
```

**Terminal 2 (iterate):**
```bash
colcon build --packages-select adc_processor && \
  source install/setup.bash && \
  ros2 run adc_processor adc_processor_node --ros-args --log-level debug
```

**Terminal 3 (validate):**
```bash
ros2 topic echo /ad7124_buffer/mV --once
```

**Logging tip:** Use `--ros-args --log-level debug` during development. Default is `info`.


## Part 2: Package Creation (10 min)

### Step 2.1: Create the Package

From the workspace root (in the devcontainer, this is `/adc_workshop_ws`):

```bash
cd src
ros2 pkg create --build-type ament_python adc_processor \
    --dependencies rclpy std_msgs adi_iio
```

**Expected output:**
```
going to create a new ros2 package 'adc_processor'...
creating package (using package template) '../adc_processor'
```

> **Note:** The `--dependencies` flag populates `package.xml` with these dependencies, but you still need to manually configure `setup.py` entry points.

### Step 2.2: Examine the Structure

```bash
tree src/adc_processor/
```

**Expected structure:**
```
src/adc_processor/
├── adc_processor/
│   └── __init__.py
├── package.xml
├── resource/adc_processor
├── setup.cfg
├── setup.py
└── test/
```

### Step 2.3: Review Package Configuration

Open `src/adc_processor/package.xml`:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd"?>
<package format="3">
  <name>adc_processor</name>
  <version>0.0.0</version>
  <description>ADC data processing package</description>
  <maintainer email="you@example.com">Your Name</maintainer>
  <license>Apache License 2.0</license>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>
  <depend>adi_iio</depend>
  ...
</package>
```

**Key point:** All dependencies from `--dependencies` are listed as `<depend>` tags.

### Step 2.4: Configure setup.py Entry Points

Open `src/adc_processor/setup.py`. Find the `entry_points` section:

```python
entry_points={
    'console_scripts': [
    ],
},
```

Add the executable entry:

```python
entry_points={
    'console_scripts': [
        'adc_processor_node = adc_processor.adc_processor_node:main',
    ],
},
```

This tells ROS 2 that running `ros2 run adc_processor adc_processor_node` should call the `main()` function in `adc_processor/adc_processor_node.py`.


## Part 3: Create the Node File (10 min)

### Step 3.1: Create adc_processor_node.py

Create the file `src/adc_processor/adc_processor/adc_processor_node.py` with this minimal template:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from adi_iio.srv import AttrReadString


class ADCProcessor(Node):
    def __init__(self):
        super().__init__('adc_processor_node')

        # Subscription to raw buffer
        self.subscription = self.create_subscription(
            Int32MultiArray,
            '/ad7124_buffer',
            self.buffer_callback,
            10
        )

        # Publisher for processed data (mV as integers)
        self.publisher = self.create_publisher(
            Int32MultiArray,
            '/ad7124_buffer/mV',
            10
        )

        # Service client for scale attribute
        self.client = self.create_client(
            AttrReadString,
            '/adi_iio_node/AttrReadString'
        )

        # Placeholder for scale value
        self.scale = None

        self.get_logger().info('ADC Processor node initialized')

    def buffer_callback(self, msg):
        """Process raw buffer data"""
        self.get_logger().debug(
            f'Received buffer with {len(msg.data)} samples'
        )


def main(args=None):
    rclpy.init(args=args)
    node = ADCProcessor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Step 3.2: Build and Test Basic Functionality

From the workspace root:

```bash
colcon build --packages-select adc_processor
source install/setup.bash
```

**Expected output:**
```
Summary: 1 package finished [x.xs]
```

### Step 3.3: Run the Node (Terminal 2)

```bash
ros2 run adc_processor adc_processor_node --ros-args --log-level debug
```

**Expected output:**
```
[INFO] [adc_processor_node]: ADC Processor node initialized
[DEBUG] [adc_processor_node]: Received buffer with 1024 samples
[DEBUG] [adc_processor_node]: Received buffer with 1024 samples
...
```

Press Ctrl+C to stop.

### Stage 1 Checkpoint

- [ ] `ros2 pkg list | grep adc_processor` shows package
- [ ] Node runs without errors
- [ ] Node logs "Received buffer with X samples"


## Part 4: Implement Service Client (15 min)

### Step 4.1: Understand the Service Interface

First, inspect the service definition:

```bash
ros2 interface show adi_iio/srv/AttrReadString
```

**Expected output:**
```
string attr_path
---
bool success
string value
```

This service takes an attribute path (like `'ad7124-8/input_voltage0-voltage1/scale'`) and returns its value.

### Step 4.2: Add Service Request Method

Add this method to the `ADCProcessor` class in `adc_processor_node.py`:

```python
def request_scale(self):
    """Request scale factor from adi_iio_node"""
    request = AttrReadString.Request()
    request.attr_path = 'ad7124-8/input_voltage0-voltage1/scale'

    # Block until service is available
    while not self.client.wait_for_service(timeout_sec=1.0):
        self.get_logger().info('Waiting for AttrReadString service...')

    future = self.client.call_async(request)
    future.add_done_callback(self.scale_response_callback)


def scale_response_callback(self, future):
    """Handle scale response"""
    try:
        response = future.result()
        if response.success:
            self.scale = float(response.value)
            self.get_logger().info(f'Scale retrieved: {self.scale}')
        else:
            self.get_logger().error('Failed to retrieve scale')
    except Exception as e:
        self.get_logger().error(f'Service call failed: {e}')
```

### Step 4.3: Call request_scale in __init__

Modify the `__init__` method to request the scale when the node starts:

```python
def __init__(self):
    super().__init__('adc_processor_node')

    # ... subscription and publisher setup ...

    # Service client for scale attribute
    self.client = self.create_client(
        AttrReadString,
        '/adi_iio_node/AttrReadString'
    )

    # Placeholder for scale value
    self.scale = None

    self.get_logger().info('ADC Processor node initialized')

    # Request scale value
    self.request_scale()
```

### Step 4.4: Rebuild and Test

```bash
colcon build --packages-select adc_processor
```

Run with Module 02 bringup in Terminal 1:

**Terminal 1:**
```bash
ros2 launch ad7124_workshop bringup.launch.py
```

**Terminal 2:**
```bash
ros2 run adc_processor adc_processor_node --ros-args --log-level debug
```

**Expected output in Terminal 2:**
```
[INFO] [adc_processor_node]: ADC Processor node initialized
[INFO] [adc_processor_node]: Waiting for AttrReadString service...
[INFO] [adc_processor_node]: Scale retrieved: 1.25
[DEBUG] [adc_processor_node]: Received buffer with 1024 samples
```

Press Ctrl+C to stop.

### Stage 2 Checkpoint

- [ ] `ros2 service list | grep AttrReadString` shows service
- [ ] Node logs "Scale retrieved: X" on startup
- [ ] Scale value is printed (should be around 1.25)


## Part 5: Implement Data Transformation (15 min)

### Step 5.1: Publisher Setup

The publisher is already created in `__init__` (using Int32MultiArray for mV values). Now we need to update `buffer_callback` to use it.

### Step 5.2: Implement Scaling in buffer_callback

Replace the `buffer_callback` method with:

```python
def buffer_callback(self, msg):
    """Process raw buffer data"""
    if self.scale is None:
        self.get_logger().warn('Scale not yet available, skipping')
        return

    self.get_logger().debug(
        f'Received buffer with {len(msg.data)} samples'
    )

    # Convert raw counts to millivolts (as integer)
    # Formula: mV = int(raw_count * scale)  (scale is already in mV)
    mv_data = [int(raw * self.scale) for raw in msg.data]

    # Create output message
    output = Int32MultiArray()
    output.layout = msg.layout  # Copy layout from input
    output.data = mv_data

    # Publish
    self.publisher.publish(output)
    self.get_logger().debug(f'Published {len(mv_data)} mV samples')
```

### Step 5.3: Rebuild and Test

```bash
colcon build --packages-select adc_processor
```

Run the test again:

**Terminal 1:**
```bash
ros2 launch ad7124_workshop bringup.launch.py
```

**Terminal 2:**
```bash
ros2 run adc_processor adc_processor_node --ros-args --log-level debug
```

**Terminal 3 (validation):**
```bash
ros2 topic echo /ad7124_buffer/mV --once
```

**Expected output in Terminal 3:**
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
- 2103
- 2105
- 2101
...
```

The values should be around 2000-2100 mV for typical input.

### Step 5.4: Verify Topic Frequency

In Terminal 3:

```bash
ros2 topic hz /ad7124_buffer/mV
```

**Expected output:**
```
average rate: 10.012
        min: 0.095s max: 0.105s std dev: 0.00257s
```

Should match the input buffer rate (~10 Hz).

### Stage 3 Checkpoint

- [ ] `ros2 topic list` shows `/ad7124_buffer/mV`
- [ ] `ros2 topic echo /ad7124_buffer/mV --once` shows float values in millivolts
- [ ] `ros2 topic hz /ad7124_buffer/mV` matches input rate (~10 Hz)


## Part 6: Launch Integration (10 min)

### Step 6.1: Update ad7124_workshop Package Dependency

Open `src/modules/02-sensor-bringup/ad7124_workshop/package.xml` and add:

```xml
<exec_depend>adc_processor</exec_depend>
```

This tells ROS 2 that `ad7124_workshop`'s bringup depends on the `adc_processor` package being available.

### Step 6.2: Modify bringup.launch.py

Open `src/modules/02-sensor-bringup/ad7124_workshop/launch/bringup.launch.py` and add the processor node definition.

First, add the import at the top:

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.event_handlers import OnExecutionComplete
from launch.event_handlers import OnProcessExit
from launch.event_handlers import OnProcessStart
from launch.actions import RegisterEventHandler
```

Then, find where the `adi_iio_node` is created. After the event handlers section, add:

```python
# ADC Processor node - runs after buffer is enabled
adc_processor_node = Node(
    package='adc_processor',
    executable='adc_processor_node',
    name='adc_processor_node',
    output='screen',
    arguments=['--ros-args', '--log-level', 'info'],
)

on_buffer_enabled = RegisterEventHandler(
    OnExecutionComplete(
        target_action=buffer_setup,
        on_completion=[adc_processor_node],
    )
)
```

### Step 6.3: Update LaunchDescription

Add `on_buffer_enabled` to the return statement:

```python
return LaunchDescription([
    # ... existing items ...
    on_buffer_complete,
    on_buffer_enabled,  # Add this
])
```

### Step 6.4: Rebuild Both Packages

```bash
colcon build --packages-select ad7124_workshop adc_processor
```

**Expected output:**
```
Starting >>> adc_processor
Starting >>> ad7124_workshop
Finished <<< adc_processor [x.xs]
Finished <<< ad7124_workshop [x.xs]

Summary: 2 packages finished [x.xs]
```

### Step 6.5: Test Full Pipeline

**Terminal 1:**
```bash
ros2 launch ad7124_workshop bringup.launch.py
```

**Expected output:**
```
[INFO] [launch]: All log files can be found below ...
[INFO] [adi_iio_node-1]: process started with pid [12345]
[INFO] [adi_iio_node-1] [...]: Creating context...
[config_attributes-2] response: ...
[buffer_setup-3] response: ...
[adc_processor_node-4]: process started with pid [12350]
[adc_processor_node-4] [INFO] [...]: ADC Processor node initialized
[adc_processor_node-4] [INFO] [...]: Scale retrieved: 1.25
```

### Step 6.6: Verify Graph Structure

**Terminal 3:**
```bash
rqt_graph
```

**Expected graph:**
```
adi_iio_node → /ad7124_buffer → adc_processor_node → /ad7124_buffer/mV
```

You should see:
- `adi_iio_node` publishes to `/ad7124_buffer`
- `adc_processor_node` subscribes to `/ad7124_buffer` and publishes to `/ad7124_buffer/mV`

### Stage 4 Checkpoint

- [ ] Single launch command brings up entire system
- [ ] No errors in Terminal 1 output
- [ ] `rqt_graph` shows correct message flow
- [ ] `ros2 topic echo /ad7124_buffer/mV --once` shows millivolt data


## Part 7: Verification & Diagnostics (10 min)

### Complete Verification Checklist

Run through this checklist with the full bringup running:

| Check                  | Command                                    | Expected Result                           |
| ---------------------- | ------------------------------------------ | ----------------------------------------- |
| Both nodes running     | `ros2 node list`                           | `/adi_iio_node` and `/adc_processor_node` |
| Input buffer topic     | `ros2 topic list \| grep buffer`           | `/ad7124_buffer` present                  |
| Output processed topic | `ros2 topic list \| grep mV`               | `/ad7124_buffer/mV` present               |
| Input data format      | `ros2 topic echo /ad7124_buffer --once`    | Int32MultiArray (raw counts)              |
| Output data format     | `ros2 topic echo /ad7124_buffer/mV --once` | Int32MultiArray (mV)                      |
| Input data rate        | `ros2 topic hz /ad7124_buffer`             | ~10 Hz                                    |
| Output data rate       | `ros2 topic hz /ad7124_buffer/mV`          | ~10 Hz                                    |
| Node parameters        | `ros2 param list`                          | Both nodes listed                         |
| Services available     | `ros2 service list \| grep adi_iio`        | AttrReadString, etc.                      |
| Graph visualization    | `rqt_graph`                                | Correct message flow                      |

### Troubleshooting Tips

**If adc_processor_node doesn't start:**
- Check Terminal 1 output for errors
- Verify `ad7124_workshop` was rebuilt after modifying `bringup.launch.py`
- Ensure `adc_processor` is listed in `ad7124_workshop/package.xml` dependencies

**If `/ad7124_buffer/mV` is empty:**
- Check that `/ad7124_buffer` is actively publishing (use `ros2 topic hz`)
- Verify scale was retrieved (look for "Scale retrieved" log)
- Check processor node logs: `ros2 node info /adc_processor_node`

**If values don't look right:**
- Check the scale value: `ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString "{attr_path: 'ad7124-8/input_voltage0-voltage1/scale'}"`
- Compare mV values to raw values and verify scaling formula


## Summary

### What You Learned

1. **ROS 2 package creation** - Using `ros2 pkg create` and configuring `setup.py`
2. **Package configuration** - Understanding `package.xml` and `setup.py` entry points
3. **Service clients** - Async service calls with callbacks
4. **Pub/Sub transformation** - Subscribe → Transform → Publish pattern
5. **Data type conversion** - Working with Int32MultiArray
6. **Logging levels** - Using debug vs info for development
7. **Launch integration** - Extending existing launch files with event handlers
8. **Debugging tools** - ros2 node, topic, service commands for verification

### Complete Pipeline

```
adi_iio_node (Module 02)
    ↓
/ad7124_buffer (raw counts)
    ↓
adc_processor_node (Module 03)
    ↓
/ad7124_buffer/mV (millivolts)
```

**You've created a complete data processing pipeline!**

### Next Steps (Optional Enhancements)

1. **Multi-channel processing:** Handle both channel 0 and channel 1
2. **Dynamic scaling:** Read scale at subscription time instead of startup
3. **Error handling:** Implement graceful degradation if service unavailable
4. **Unit tests:** Add tests for scaling calculations
5. **Configuration:** Use YAML to make scale factor configurable

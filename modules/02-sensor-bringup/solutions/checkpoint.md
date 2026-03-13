# Module 2: Solutions Checkpoint

## Expected System State After Module Completion

### Package Built Successfully

```bash
$ colcon build --symlink-install --packages-select ad7124_workshop
Starting >>> ad7124_workshop
Finished <<< ad7124_workshop [0.5s]

Summary: 1 package finished
```

### Bringup Output

```bash
$ ros2 launch ad7124_workshop bringup.launch.py
[INFO] [launch]: All log files can be found below /home/...
[INFO] [launch]: Default logging verbosity is set to INFO
[INFO] [adi_iio_node-1]: process started with pid [12345]
[adi_iio_node-1] [INFO] [...] [adi_iio_node]: creating context...
[adi_iio_node-1] [INFO] [...] [adi_iio_node]: setting timeout to 0
[adi_iio_node-1] [INFO] [...] [rclcpp]: Initializing buffers...
[adi_iio_node-1] [INFO] [...] [adi_iio_node]: IIO Node
[ros2-2] response: ...AttrWriteString_Response(success=True, message='0.000149011')
[ros2-3] response: ...AttrWriteString_Response(success=True, message='...')
...
[ros2-5] response: ...BufferCreate_Response(success=True, message='Success'...)
[ros2-6] response: ...BufferEnableTopic_Response(success=True, message='Success')
```

### Topics After Full Bringup

```bash
$ ros2 topic list
/ad7124_buffer
/parameter_events
/rosout
```

### Attribute Verification

```bash
$ ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString \
  "{attr_path: 'ad7124-8/input_voltage0-voltage1/scale'}"
response:
adi_iio.srv.AttrReadString_Response(success=True, message='0.000149011')

$ ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString \
  "{attr_path: 'ad7124-8/input_voltage0-voltage1/sampling_frequency'}"
response:
adi_iio.srv.AttrReadString_Response(success=True, message='4800.000000000')
```

Note: The driver may adjust sampling_frequency to nearest supported value.

### Buffer Topic Output

```bash
$ ros2 topic echo /ad7124_buffer --once
layout:
  dim:
  - label: samples
    size: 400
    stride: 400
  - label: channels
    size: 2
    stride: 2
  data_offset: 0
data:
- 1682586
- 1683546
- 1683546
...
```

### Waveform Visualization

To visually verify data quality, use the visualization script from `iio_ros2`:

```bash
cd /adi_ros2_ws/src/iio_ros2/launch/
python3 visualize_iio_waveform.py --topic /ad7124_buffer
```

You should see a live plot with a clean waveform for each channel. You can also use `rqt_graph` to visualize the data flow between the node and topics.

![Waveform Visualization](../assets/buffer_visualization.png)

![Data Flow (rqt_graph)](../assets/rqt_graph.png)

### Topic Rate

```bash
$ ros2 topic hz /ad7124_buffer
average rate: 1.001
        min: 0.995s max: 1.005s std dev: 0.00257s window: 12
```

---

## Exercise Solutions

### Exercise 1: Config Challenge - Complete config_attributes.launch.py

```python
def generate_launch_description():
    # Configuration values
    scale = '0.000149011'
    sampling_frequency = '1000'

    # Channel 0: input_voltage0-voltage1
    ch0_scale = ExecuteProcess(
        name='ch0_scale',
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

    ch0_sampling_freq = ExecuteProcess(
        name='ch0_sampling_freq',
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

    # Channel 1: input_voltage2-voltage3
    ch1_scale = ExecuteProcess(
        name='ch1_scale',
        cmd=[[
            FindExecutable(name='ros2'),
            ' service call ',
            '/adi_iio_node/AttrWriteString ',
            'adi_iio/srv/AttrWriteString ',
            '"{attr_path: \'ad7124-8/input_voltage2-voltage3/scale\', ',
            f"value: '{scale}'}}\"",
        ]],
        shell=True,
    )

    ch1_sampling_freq = ExecuteProcess(
        name='ch1_sampling_freq',
        cmd=[[
            FindExecutable(name='ros2'),
            ' service call ',
            '/adi_iio_node/AttrWriteString ',
            'adi_iio/srv/AttrWriteString ',
            '"{attr_path: \'ad7124-8/input_voltage2-voltage3/sampling_frequency\', ',
            f"value: '{sampling_frequency}'}}\"",
        ]],
        shell=True,
    )

    return LaunchDescription([
        ch0_scale,
        ch0_sampling_freq,
        ch1_scale,
        ch1_sampling_freq,
    ])
```

### Exercise 2: Buffer Challenge - Complete buffer_setup.launch.py

```python
def generate_launch_description():
    device_path = 'ad7124-8'
    channels = ['input_voltage0-voltage1', 'input_voltage2-voltage3']
    samples_count = 400
    topic_name = '/ad7124_buffer'
    loop_rate = 1.0

    buffer_create = ExecuteProcess(
        name='buffer_create',
        cmd=[[
            FindExecutable(name='ros2'),
            ' service call ',
            '/adi_iio_node/BufferCreate ',
            'adi_iio/srv/BufferCreate ',
            f"\"{{device_path: '{device_path}', ",
            f"channels: {channels}, ",
            f"samples_count: {samples_count}}}\"",
        ]],
        shell=True,
        output='screen',
    )

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

    # Use OnProcessExit for ExecuteProcess actions (not OnExecutionComplete)
    on_buffer_created = RegisterEventHandler(
        OnProcessExit(
            target_action=buffer_create,
            on_exit=[buffer_enable_topic],
        )
    )

    return LaunchDescription([
        buffer_create,
        on_buffer_created,
    ])
```

---

## Verification Checklist

Before proceeding to Module 3, verify:

### Package Build
- [ ] `colcon build --symlink-install --packages-select ad7124_workshop` succeeds
- [ ] `ros2 pkg list | grep ad7124` shows the package

### Launch File Execution
- [ ] `ros2 launch ad7124_workshop bringup.launch.py` starts without errors
- [ ] Node, config, and buffer steps execute in sequence

### Attribute Configuration
- [ ] All 4 attributes configured (2 channels x 2 attributes)
- [ ] AttrReadString returns expected values

### Buffer Streaming
- [ ] `/ad7124_buffer` topic exists
- [ ] Topic publishes MultiArray data
- [ ] Topic rate is approximately 1 Hz

### Understanding
- [ ] Can explain event-driven orchestration
- [ ] Can explain YAML parameter loading
- [ ] Can debug launch file issues using diagnostic commands

---

## Common Issues and Fixes

### Issue: Package not found after build

**Symptom:** `ros2 pkg list` doesn't show ad7124_workshop

**Fix:**
1. Make sure you sourced the workspace: `source install/setup.bash`
2. Check for build errors in the colcon output

### Issue: Config launch file not executing

**Symptom:** Attributes not configured after bringup

**Fix:**
1. Check for Python syntax errors: `python3 -m py_compile <file>`
2. Verify OnProcessStart event handler is registered
3. Check for typos in launch file path

### Issue: Buffer topic not created

**Symptom:** `/ad7124_buffer` doesn't appear in topic list

**Fix:**
1. Verify BufferCreate succeeded (check log output)
2. Verify BufferEnableTopic is in the LaunchDescription return
3. Check OnProcessExit is properly chained (not OnExecutionComplete - that's for IncludeLaunchDescription)

### Issue: Service call fails

**Symptom:** `success=False` in service response

**Fix:**
1. Check attribute path for typos
2. Verify node has finished initializing
3. For BufferCreate: use channel name without device prefix

---

## Key Concepts Summary

| Concept                  | What You Learned                                             |
| ------------------------ | ------------------------------------------------------------ |
| Launch Files             | Python-based orchestration of ROS2 nodes and actions         |
| Node Action              | Starting ROS2 nodes with parameters                          |
| ExecuteProcess           | Running shell commands (e.g., service calls)                 |
| IncludeLaunchDescription | Composing multiple launch files                              |
| RegisterEventHandler     | Reacting to process lifecycle events                         |
| OnProcessStart           | Triggering actions when a Node or process starts             |
| OnProcessExit            | Triggering actions when an ExecuteProcess finishes           |
| OnExecutionComplete      | Triggering actions when an IncludeLaunchDescription finishes |
| YAML Parameters          | Externalizing configuration from code                        |

> **Event Handler Selection:**
> - Use `OnProcessStart` when a Node or ExecuteProcess begins
> - Use `OnProcessExit` when an ExecuteProcess completes (like our service calls)
> - Use `OnExecutionComplete` when an IncludeLaunchDescription completes (like config_attributes in bringup.launch.py)

**You're ready for Module 3!**

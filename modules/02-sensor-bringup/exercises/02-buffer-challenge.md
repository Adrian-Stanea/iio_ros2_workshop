# Exercise 2: Buffer Challenge

## Objective

Complete the `buffer_setup.launch.py` file to enable buffer topic streaming.

## Background

The launch file template already creates the buffer with `BufferCreate`. You need to add the `BufferEnableTopic` service call to create a ROS2 topic.

## Tasks

### Task 1: Check the Service Interface

Run this command to see the required fields:

```bash
ros2 interface show adi_iio/srv/BufferEnableTopic
```

<details>
<summary>Expected Output</summary>

```
string device_path
string topic_name
float64 loop_rate 1.0
---
bool success
string message
```

</details>

### Task 2: Create the BufferEnableTopic ExecuteProcess

Add a new ExecuteProcess that calls the BufferEnableTopic service.

<details>
<summary>Hint</summary>

Use the variables defined at the top of the file:
- `device_path` = 'ad7124-8'
- `topic_name` = '/ad7124_buffer'
- `loop_rate` = 1.0

</details>

### Task 3: Add Sequencing

BufferEnableTopic must run AFTER BufferCreate completes. Use `RegisterEventHandler` with `OnProcessExit`.

> **Note:** For `ExecuteProcess` actions, use `OnProcessExit`. The `OnExecutionComplete` handler is used for `IncludeLaunchDescription` actions.

<details>
<summary>Hint</summary>

```python
on_buffer_created = RegisterEventHandler(
    OnProcessExit(
        target_action=buffer_create,
        on_exit=[buffer_enable_topic],
    )
)
```

</details>

### Task 4: Update the Return Statement

Add the event handler to the LaunchDescription.

## Verification

After rebuilding, run:

```bash
ros2 launch ad7124_workshop bringup.launch.py
```

Then verify the topic:

```bash
ros2 topic list | grep ad7124
ros2 topic echo /ad7124_buffer --once
```

### Visualize the Waveform

The `iio_ros2` package includes a visualization script to verify data quality.
In a new terminal inside the devcontainer:

```bash
cd /adi_ros2_ws/src/iio_ros2/launch/
python3 visualize_iio_waveform.py --topic /ad7124_buffer
```

You should see a live plot of the sampled waveform. Use `rqt_graph` to inspect the data flow between nodes and topics.

![Waveform Visualization](../assets/buffer_visualization.png)

![Data Flow (rqt_graph)](../assets/rqt_graph.png)

## Success Criteria

- [ ] `/ad7124_buffer` topic exists
- [ ] Topic publishes MultiArray data
- [ ] `ros2 topic hz` shows ~1 Hz rate
- [ ] Waveform visualization shows a clean signal (not noise)

# Exercise 3: Launch Integration

**Goal:** Integrate your processor node into Module 02's launch system.

---

## Step 3.1: Add Package Dependency

Edit `modules/02-sensor-bringup/ad7124_workshop/package.xml`, add before `</package>`:

```xml
<exec_depend>adc_processor</exec_depend>
```

---

## Step 3.2: Extend bringup.launch.py

Open `modules/02-sensor-bringup/ad7124_workshop/launch/bringup.launch.py` and add:

**Import (at top):**
```python
from launch_ros.actions import Node  # Already imported
```

**Node definition (after buffer_setup):**
```python
# ADC Processor Node
adc_processor_node = Node(
    package='adc_processor',
    executable='adc_processor_node',
    name='adc_processor_node',
    output='screen',
)
```

**Event handler (after on_config_complete):**
```python
# Start processor after buffer setup completes
on_buffer_complete = RegisterEventHandler(
    OnExecutionComplete(
        target_action=buffer_setup,
        on_completion=[adc_processor_node],
    )
)
```

**Add to LaunchDescription:**
```python
return LaunchDescription([
    adi_iio_node,
    on_node_start,
    on_config_complete,
    on_buffer_complete,  # Add this line
])
```

---

## Step 3.3: Rebuild Both Packages

From the workspace root:

```bash
colcon build --packages-select ad7124_workshop adc_processor
source install/setup.bash
```

---

## Step 3.4: Test Full Pipeline

```bash
ros2 launch ad7124_workshop bringup.launch.py
```

**Expected logs:**
```
[adi_iio_node-1] [INFO]: IIO Node started
[adc_processor_node-2] [INFO]: Scale value: 0.000149011
[adc_processor_node-2] [INFO]: ADC Processor Node started!
```

---

## Step 3.5: Validate with rqt_graph

```bash
rqt_graph
```

**Expected:** Graph shows adi_iio_node → adc_processor_node

---

## Step 3.6: Visualize Output (Optional)

If the `visualize_iio_waveform.py` script is available in your workspace:

```bash
python3 $(ros2 pkg prefix iio_ros2)/share/iio_ros2/launch/visualize_iio_waveform.py --topic /ad7124_buffer/mV
```

Alternatively, use `rqt_plot` for basic visualization:

```bash
rqt_plot /ad7124_buffer/mV/data[0]
```

**Expected:** Live plot showing millivolt waveform.

---

## Checkpoint

- [ ] Single launch command brings up entire system
- [ ] Both nodes appear in `ros2 node list`
- [ ] `rqt_graph` shows correct connections
- [ ] Waveform visualization works with mV topic

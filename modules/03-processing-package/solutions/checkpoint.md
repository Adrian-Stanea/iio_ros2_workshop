# Module 3: Solutions Checkpoint
# Module 3: Solutions Checkpoint

## Expected System State After Module Completion

### Package Built Successfully

```bash
$ colcon build --packages-select adc_processor
Starting >>> adc_processor
Finished <<< adc_processor [0.5s]

Summary: 1 package finished
```

### Full Pipeline Running

```bash
$ ros2 launch ad7124_workshop bringup.launch.py
[INFO] [launch]: All log files can be found below /home/...
[INFO] [adi_iio_node-1]: process started with pid [...]
[INFO] [adc_processor_node-2]: process started with pid [...]
[adc_processor_node-2] [INFO] [...]: Scale value: 0.000149011
[adc_processor_node-2] [INFO] [...]: ADC Processor Node started!
```

### Topics After Full Bringup

```bash
$ ros2 topic list
/ad7124_buffer
/ad7124_buffer/mV
/parameter_events
/rosout
```

### Processed Data Output

```bash
$ ros2 topic echo /ad7124_buffer/mV --once
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
- 250
- 251
...
```

---

## Verification Checklist

### Package Build
- [ ] `colcon build --packages-select adc_processor` succeeds
- [ ] `ros2 pkg list | grep adc_processor` shows the package

### Node Functionality
- [ ] Node starts without errors
- [ ] Scale value retrieved successfully (check logs)
- [ ] `/ad7124_buffer/mV` topic exists
- [ ] Topic publishes Int32MultiArray with scaled values
- [ ] Topic rate matches input (~10 Hz)

### Launch Integration
- [ ] `ad7124_workshop/package.xml` includes `<exec_depend>adc_processor</exec_depend>`
- [ ] `bringup.launch.py` includes processor node with event handler
- [ ] `ros2 launch ad7124_workshop bringup.launch.py` brings up full pipeline

### Visualization
- [ ] `rqt_graph` shows adi_iio_node → adc_processor_node connection
- [ ] `visualize_iio_waveform.py --topic /ad7124_buffer/mV` shows millivolt waveform

---

## Common Issues and Fixes

### Issue: "Package not found" after build

**Symptom:** `ros2 pkg list` doesn't show adc_processor

**Fix:**
1. Make sure you sourced the workspace: `source install/setup.bash`
2. Check for build errors in the colcon output

### Issue: Service call times out

**Symptom:** Node hangs waiting for service

**Fix:**
1. Verify `adi_iio_node` is running: `ros2 node list`
2. Check service exists: `ros2 service list | grep AttrReadString`

### Issue: Scale value is 0 or incorrect

**Symptom:** Output values are 0 or wrong magnitude

**Fix:**
1. Check the `attr_path` is correct: `'ad7124-8/input_voltage0-voltage1/scale'`
2. Verify response parsing: `float(response.message)`

### Issue: Entry point not found

**Symptom:** `ros2 run adc_processor adc_processor_node` fails

**Fix:**
1. Check `setup.py` has correct entry_points format
2. Rebuild: `colcon build --packages-select adc_processor`
3. Re-source: `source install/setup.bash`

---

## Key Concepts Summary

| Concept                 | What You Learned                            |
| ----------------------- | ------------------------------------------- |
| `ros2 pkg create`       | Scaffold a Python package with dependencies |
| `package.xml`           | Declare runtime dependencies                |
| `setup.py` entry_points | Register executable nodes                   |
| Service Client          | Programmatically call ROS2 services         |
| Pub/Sub transformation  | Subscribe, process, republish pattern       |
| Logging levels          | `--ros-args --log-level debug`              |
| `OnExecutionComplete`   | Sequence launch actions                     |

**You've completed Module 3!**

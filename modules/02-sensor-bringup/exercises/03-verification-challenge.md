# Exercise 3: Verification & Diagnostics

## Objective

Learn the systematic verification process for launch file bringup.

## Background

When running a launch file, multiple components must work together. This exercise teaches you how to verify each component and diagnose common issues.

## Verification Checklist

Work through this checklist with the bringup running:

### 1. Node Running

```bash
ros2 node list
```

**Expected:** `/adi_iio_node` present

**If missing:** Check Terminal 1 for startup errors

---

### 2. Services Available

```bash
ros2 service list | grep adi_iio
```

**Expected:** All adi_iio services listed (AttrReadString, BufferCreate, etc.)

**If missing:** Node may have crashed - check logs

---

### 3. Attributes Configured

Check each configured attribute:

```bash
# Channel 0 scale
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString \
  "{attr_path: 'ad7124-8/input_voltage0-voltage1/scale'}"
```

**Expected:** `message='0.000149011'`

**If wrong value:** Check config_attributes.launch.py values

---

### 4. Buffer Topic Exists

```bash
ros2 topic list | grep ad7124
```

**Expected:** `/ad7124_buffer`

**If missing:** BufferEnableTopic may have failed

---

### 5. Data Streaming

```bash
ros2 topic echo /ad7124_buffer --once
```

**Expected:** MultiArray with `data` containing sample values

**If empty:** Buffer may not have been created

---

### 6. Visualize the Waveform

The `iio_ros2` package includes a visualization script that plots buffer data in real time.
In a new terminal inside the devcontainer, run:

```bash
cd /adi_ros2_ws/src/iio_ros2/launch/
python3 visualize_iio_waveform.py --topic /ad7124_buffer
```

**Expected:** A live plot showing the sampled waveform for each channel.

![Waveform Visualization](../assets/buffer_visualization.png)

You can also inspect the data flow between nodes and topics using `rqt_graph`:

![Data Flow (rqt_graph)](../assets/rqt_graph.png)

---

### 7. Topic Rate

```bash
ros2 topic hz /ad7124_buffer
```

**Expected:** ~1 Hz (matching configured loop_rate)

**If different:** Check loop_rate parameter

---

## Diagnostic Commands Reference

| What to Check      | Command                     |
| ------------------ | --------------------------- |
| Running nodes      | `ros2 node list`            |
| Available services | `ros2 service list`         |
| Available topics   | `ros2 topic list`           |
| Service interface  | `ros2 interface show <srv>` |
| Topic type         | `ros2 topic info <topic>`   |
| Topic data         | `ros2 topic echo <topic>`   |
| Topic rate         | `ros2 topic hz <topic>`     |
| Node info          | `ros2 node info <node>`     |

## Success Criteria

- [ ] All checklist items verified
- [ ] Can explain what each diagnostic command shows
- [ ] Understand the bringup sequence (node → config → buffer)

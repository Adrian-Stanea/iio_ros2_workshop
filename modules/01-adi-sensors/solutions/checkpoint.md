# Module 1: Solutions Checkpoint

## Expected System State After Module Completion

### Services Available

After starting `adi_iio_node`, running `ros2 service list` should show:

```
/adi_iio_node/AttrDisableTopic
/adi_iio_node/AttrEnableTopic
/adi_iio_node/AttrReadString
/adi_iio_node/AttrWriteString
/adi_iio_node/BufferCreate
/adi_iio_node/BufferDestroy
/adi_iio_node/BufferDisableTopic
/adi_iio_node/BufferEnableTopic
/adi_iio_node/BufferRead
/adi_iio_node/BufferRefill
/adi_iio_node/BufferWrite
/adi_iio_node/ListAttributes
/adi_iio_node/ListChannels
/adi_iio_node/ListDevices
/adi_iio_node/ScanContext
/adi_iio_node/describe_parameters
/adi_iio_node/get_parameter_types
/adi_iio_node/get_parameters
/adi_iio_node/list_parameters
/adi_iio_node/set_parameters
/adi_iio_node/set_parameters_atomically
```

### Topics After Enabling Attribute Topics

After completing Part 4 of the hands-on guide:

```bash
$ ros2 topic list
/ad7124_8/input_voltage0_voltage1/raw/read
/ad7124_8/input_voltage0_voltage1/raw/write
/parameter_events
/rosout
```

**Note:** Topic names use underscores instead of hyphens (`ad7124-8` becomes `ad7124_8`).

### Expected Service Responses

#### ListDevices
```
response:
adi_iio.srv.ListDevices_Response(success=True, message='Found 6 devices', data=['cpu_thermal', 'rp1_adc', 'pwmfan', 'rpi_volt', 'ad7124-8', 'ad7124-8-dev0'])
```

#### ListChannels for ad7124-8
```
response:
adi_iio.srv.ListChannels_Response(success=True, message='Found 9 channels in device: ad7124-8', data=['ad7124-8/input_voltage0-voltage1', 'ad7124-8/input_voltage2-voltage3', 'ad7124-8/input_voltage4-voltage5', 'ad7124-8/input_voltage6-voltage7', 'ad7124-8/input_voltage8-voltage9', 'ad7124-8/input_voltage10-voltage11', 'ad7124-8/input_voltage12-voltage13', 'ad7124-8/input_voltage14-voltage15', 'ad7124-8/input_temp'])
```

#### AttrReadString for raw
```
response:
adi_iio.srv.AttrReadString_Response(success=True, message='8388552')
```

#### AttrEnableTopic success
```
response:
adi_iio.srv.AttrEnableTopic_Response(success=True, message='Success')
```

### Topic Echo Output

```bash
$ ros2 topic echo /ad7124_8/input_voltage0_voltage1/raw/read
data: '3356827'
---
data: '3356827'
---
data: '3356827'
---
```

### Topic Frequency

```bash
$ ros2 topic hz /ad7124_8/input_voltage0_voltage1/raw/read
average rate: 10.012
        min: 0.095s max: 0.105s std dev: 0.00257s window: 12
```

### Buffer Topic Output

```bash
$ ros2 topic echo /ad7124_buffer --once
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

---

## Exercise Solutions

### Exercise 1: Discovery Challenge

**Q1: Available devices**
```
ad7124-8, cpu_thermal, rp1_adc, pwmfan, rpi_volt (on Raspberry Pi 5)
```

**Q2: Channel count**
```
9 channels for AD7124-8 (8 differential + 1 temperature)
```

**Q4: IIO Path for scale on channel 2-3**
```
ad7124-8/input_voltage2-voltage3/scale
```

### Exercise 2: Configuration Challenge

**Task 2: Voltage calculation example**
```
If raw = 8388552 and scale = 0.000149011
Voltage = 8388552 * 0.000149011 = ~1250 mV = 1.25V
```

**Bonus: Why raw is read-only**
The `raw` attribute represents the actual ADC reading from hardware. Writing to it doesn't make physical sense - you can't tell the ADC what voltage is at its input.

### Exercise 3: Topic Challenge

**Task 3: Topic naming pattern**
```
/ad7124_8/input_voltage4_voltage5/raw/read
/ad7124_8/input_voltage0_voltage1/scale/read

Pattern: /<attr_path_with_underscores>/read
Note: Hyphens are converted to underscores in topic names
```

**Task 4: Multiple topics for same attribute**
Calling AttrEnableTopic on an already-enabled attribute will return success but won't create a duplicate topic.

---

## Verification Checklist

Before proceeding to Module 2, verify:

### Basic Functionality
- [ ] `ros2 run adi_iio adi_iio_node` starts without errors
- [ ] `ros2 service list` shows adi_iio services
- [ ] `ListDevices` returns `ad7124-8`

### IIO Path Understanding
- [ ] Can construct correct paths for any device/channel/attribute
- [ ] Understand differential channel naming (voltageX-voltageY)

### Service Operations
- [ ] `AttrReadString` successfully reads attributes
- [ ] `AttrWriteString` successfully modifies writable attributes
- [ ] Can verify changes with read-after-write pattern

### Attribute Topic Creation
- [ ] `AttrEnableTopic` creates new topics
- [ ] Topics appear in `ros2 topic list` (note: underscores instead of hyphens)
- [ ] `ros2 topic echo` shows continuous data
- [ ] `ros2 topic hz` confirms expected frequency

### Buffer Topic Creation
- [ ] `BufferCreate` succeeds with channels array (without device prefix)
- [ ] `BufferEnableTopic` creates the buffer topic
- [ ] `ros2 topic echo /ad7124_buffer --once` shows multi-sample data

---

## Common Issues and Fixes

### Issue: Services not found
**Symptom:** `ros2 service list` doesn't show adi_iio services
**Fix:**
1. Verify adi_iio_node is running in Terminal 1
2. Use `docker compose exec ros2 /ros_entrypoint.sh bash` for Terminal 2

### Issue: IIO path not found
**Symptom:** Service returns error about invalid path
**Fix:**
1. Use `ListDevices` → `ListChannels` → `ListAttributes` to discover correct paths
2. Check for typos in device/channel names

### Issue: BufferCreate fails
**Symptom:** `success=False` or channel not found error
**Fix:** Use channel names WITHOUT device prefix:
- Correct: `['input_voltage0-voltage1']`
- Wrong: `['ad7124-8/input_voltage0-voltage1']`

### Issue: Topic not publishing
**Symptom:** Topic exists but `ros2 topic echo` shows nothing
**Fix:**
1. Check service response for errors
2. Verify attribute is readable with `AttrReadString`
3. Check loop_rate is > 0

### Issue: Topic name not found
**Symptom:** Can't echo topic with hyphenated name
**Fix:** Topic names use underscores:
- Service uses: `ad7124-8/input_voltage0-voltage1/raw`
- Topic name becomes: `/ad7124_8/input_voltage0_voltage1/raw/read`

---

## Key Concepts Summary

| Concept          | What You Learned                                                 |
| ---------------- | ---------------------------------------------------------------- |
| Services-First   | adi_iio uses services, topics created on demand                  |
| IIO Paths        | `device/channel/attribute` hierarchy                             |
| Discovery        | ScanContext → ListDevices → ListChannels → ListAttributes        |
| Read/Write       | AttrReadString, AttrWriteString for configuration                |
| Attribute Topics | AttrEnableTopic creates continuous streams for single attributes |
| Buffer Topics    | BufferCreate + BufferEnableTopic for multi-sample streaming      |
| Topic Naming     | Hyphens become underscores in topic names                        |

**You're ready for Module 2!**

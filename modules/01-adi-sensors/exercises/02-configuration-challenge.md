# Exercise 2: Configuration Challenge

## Objective

Practice reading and writing device configuration attributes.

## Background

Configuring an ADC involves adjusting various parameters like sampling frequency, gain, and filtering. This exercise helps you understand how to read current settings and modify them.

## Challenge Tasks

### Task 1: Read All Key Parameters

Read the following attributes for channel `input_voltage0-voltage1`:

1. `raw` - Current ADC reading
2. `scale` - Conversion factor to voltage
3. `sampling_frequency` - Current sample rate

**Record your findings:**

| Attribute          | Value |
| ------------------ | ----- |
| raw                |       |
| scale              |       |
| sampling_frequency |       |

<details>
<summary>Commands</summary>

```bash
# Raw value
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString "{attr_path: 'ad7124-8/input_voltage0-voltage1/raw'}"

# Scale
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString "{attr_path: 'ad7124-8/input_voltage0-voltage1/scale'}"

# Sampling frequency
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString "{attr_path: 'ad7124-8/input_voltage0-voltage1/sampling_frequency'}"
```

</details>

### Task 2: Calculate Voltage

Using the raw and scale values you read:

**Calculate the input voltage:**

```
Voltage = raw * scale = _______ * _______ = _______ V
```

### Task 3: Change Sampling Frequency

1. Read the current sampling frequency
2. Change it to a different value (try 4800 or 19200)
3. Read it back to verify the change

**What sampling frequency values are valid?**

<details>
<summary>Hint</summary>

Try writing an invalid value and observe the error message. Valid values depend on the ADC configuration.

Common values for AD7124-8: 9600, 19200, 4800, 2400, 1200, 600, etc.

</details>

### Task 4: Multi-Channel Configuration

Configure the sampling frequency for **three different channels** to three different values:

| Channel                   | Target Frequency |
| ------------------------- | ---------------- |
| `input_voltage0-voltage1` | 9600             |
| `input_voltage2-voltage3` | 4800             |
| `input_voltage4-voltage5` | 19200            |

<details>
<summary>Solution</summary>

```bash
ros2 service call /adi_iio_node/AttrWriteString adi_iio/srv/AttrWriteString "{attr_path: 'ad7124-8/input_voltage0-voltage1/sampling_frequency', value: '9600'}"

ros2 service call /adi_iio_node/AttrWriteString adi_iio/srv/AttrWriteString "{attr_path: 'ad7124-8/input_voltage2-voltage3/sampling_frequency', value: '4800'}"

ros2 service call /adi_iio_node/AttrWriteString adi_iio/srv/AttrWriteString "{attr_path: 'ad7124-8/input_voltage4-voltage5/sampling_frequency', value: '19200'}"
```

</details>

## Bonus Challenge

**Find read-only attributes:**

Some attributes can be read but not written. Try to write to the `raw` attribute:

```bash
ros2 service call /adi_iio_node/AttrWriteString adi_iio/srv/AttrWriteString "{attr_path: 'ad7124-8/input_voltage0-voltage1/raw', value: '0'}"
```

What happens? Why?

## Success Criteria

- [ ] Can read any attribute using correct IIO path
- [ ] Can write configuration attributes
- [ ] Understand the read-verify pattern (read → write → read to confirm)
- [ ] Can calculate voltage from raw + scale
- [ ] Know which attributes are read-only vs read-write

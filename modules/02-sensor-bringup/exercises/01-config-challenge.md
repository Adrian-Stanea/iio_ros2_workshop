# Exercise 1: Config Challenge

## Objective

Complete the `config_attributes.launch.py` file to configure attributes for both differential channels.

## Background

The launch file template already configures the **scale** attribute for channel 0. You need to add the remaining attribute configurations.

## Tasks

### Task 1: Add sampling_frequency for Channel 0

The scale is already set. Now add the sampling_frequency configuration.

<details>
<summary>Hint</summary>

Follow the same pattern as `ch0_scale`. Change the attribute name from `scale` to `sampling_frequency` and use the `sampling_frequency` variable.

</details>

### Task 2: Add scale and sampling_frequency for Channel 1

Channel 1 is `input_voltage2-voltage3`. Configure both attributes.

<details>
<summary>Hint</summary>

Copy the channel 0 patterns and change `input_voltage0-voltage1` to `input_voltage2-voltage3`.

</details>

### Task 3: Update the Return Statement

Add all new ExecuteProcess actions to the LaunchDescription.

## Verification

After rebuilding, run:

```bash
ros2 launch ad7124_workshop bringup.launch.py
```

Then verify each attribute:

```bash
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString \
  "{attr_path: 'ad7124-8/input_voltage0-voltage1/sampling_frequency'}"
```

## Success Criteria

- [ ] Channel 0 scale configured
- [ ] Channel 0 sampling_frequency configured
- [ ] Channel 1 scale configured
- [ ] Channel 1 sampling_frequency configured
- [ ] All AttrReadString calls return expected values

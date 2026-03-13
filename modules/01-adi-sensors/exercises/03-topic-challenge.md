# Exercise 3: Dynamic Topic Challenge

## Objective

Practice creating and managing ROS2 topics from IIO attributes.

## Background

This is the key skill of this module: understanding how to bridge the services-first architecture to continuous data streams.

## Challenge Tasks

### Task 1: Create Your First Topic

Create a topic for the `raw` attribute at 5 Hz (not 10 Hz as in the hands-on guide):

```bash
# Your command here
```

**Verify:**
- [ ] Topic appears in `ros2 topic list`
- [ ] `ros2 topic hz` shows ~5 Hz

<details>
<summary>Solution</summary>

```bash
ros2 service call /adi_iio_node/AttrEnableTopic adi_iio/srv/AttrEnableTopic "{attr_path: 'ad7124-8/input_voltage0-voltage1/raw', loop_rate: 5.0}"
```

</details>

### Task 2: Multiple Topics

Create topics for THREE different attributes simultaneously:

| Attribute                          | Rate  |
| ---------------------------------- | ----- |
| `raw` (channel 0-1)                | 10 Hz |
| `raw` (channel 2-3)                | 10 Hz |
| `sampling_frequency` (channel 0-1) | 1 Hz  |

After creating all topics, run:
```bash
ros2 topic list | grep ad7124
```

**How many topics do you see?**

<details>
<summary>Solution</summary>

```bash
ros2 service call /adi_iio_node/AttrEnableTopic adi_iio/srv/AttrEnableTopic "{attr_path: 'ad7124-8/input_voltage0-voltage1/raw', loop_rate: 10.0}"

ros2 service call /adi_iio_node/AttrEnableTopic adi_iio/srv/AttrEnableTopic "{attr_path: 'ad7124-8/input_voltage2-voltage3/raw', loop_rate: 10.0}"

ros2 service call /adi_iio_node/AttrEnableTopic adi_iio/srv/AttrEnableTopic "{attr_path: 'ad7124-8/input_voltage0-voltage1/sampling_frequency', loop_rate: 1.0}"
```

You should see 3 topics (plus parameter_events and rosout).

</details>

### Task 3: Topic Naming Pattern

Without creating any more topics, predict the topic name for:

| Attribute Path                           | Predicted Topic Name |
| ---------------------------------------- | -------------------- |
| `ad7124-8/input_voltage4-voltage5/raw`   |                      |
| `ad7124-8/input_voltage0-voltage1/scale` |                      |

<details>
<summary>Solution</summary>

- `/ad7124-8/input_voltage4-voltage5/raw/read`
- `/ad7124-8/input_voltage0-voltage1/scale/read`

The pattern is: `/<attr_path>/read`

</details>

### Task 4: Compare Topic Rates

Create two topics with different rates for the same channel:

1. Create a topic at 1 Hz
2. Note: Can you create a second topic for the same attribute at a different rate?

<details>
<summary>Discussion</summary>

Try this:
```bash
# First at 1 Hz
ros2 service call /adi_iio_node/AttrEnableTopic adi_iio/srv/AttrEnableTopic "{attr_path: 'ad7124-8/input_voltage4-voltage5/raw', loop_rate: 1.0}"

# Then try 10 Hz for the same attribute
ros2 service call /adi_iio_node/AttrEnableTopic adi_iio/srv/AttrEnableTopic "{attr_path: 'ad7124-8/input_voltage4-voltage5/raw', loop_rate: 10.0}"
```

What happens? Does it create a second topic or update the existing one?

</details>

### Task 5: Disable Topics

Use `AttrDisableTopic` to remove a topic you created:

```bash
# First, check the service interface
ros2 interface show adi_iio/srv/AttrDisableTopic

# Then disable a topic
ros2 service call /adi_iio_node/AttrDisableTopic adi_iio/srv/AttrDisableTopic "{attr_path: 'ad7124-8/input_voltage0-voltage1/raw'}"
```

**Verify:**
- [ ] Topic no longer appears in `ros2 topic list`
- [ ] `ros2 topic echo` on that topic shows no data

## Bonus Challenge: Monitoring Script

Write a bash one-liner that:
1. Enables a topic
2. Waits 5 seconds
3. Measures the topic frequency
4. Disables the topic

<details>
<summary>Solution</summary>

```bash
ros2 service call /adi_iio_node/AttrEnableTopic adi_iio/srv/AttrEnableTopic "{attr_path: 'ad7124-8/input_voltage0-voltage1/raw', loop_rate: 10.0}" && \
sleep 2 && \
timeout 3 ros2 topic hz /ad7124-8/input_voltage0-voltage1/raw/read && \
ros2 service call /adi_iio_node/AttrDisableTopic adi_iio/srv/AttrDisableTopic "{attr_path: 'ad7124-8/input_voltage0-voltage1/raw'}"
```

</details>

## Success Criteria

- [ ] Can create topics at custom frequencies
- [ ] Can manage multiple topics simultaneously
- [ ] Understand the topic naming convention
- [ ] Can disable topics when no longer needed
- [ ] Understand the relationship between services and topics

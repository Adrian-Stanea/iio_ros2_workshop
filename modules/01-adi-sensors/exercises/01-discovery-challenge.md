# Exercise 1: Discovery Challenge

## Objective

Practice using the IIO path system to discover and explore hardware without being given explicit paths.

## Background

You're working with an IIO device but don't know its exact configuration. Use the adi_iio discovery services to answer the questions below.

## Challenge Questions

Answer each question by executing the appropriate service calls.

### Question 1: Device Discovery

**What IIO devices are available in your system?**

<details>
<summary>Hint</summary>

Use the `ListDevices` service. No parameters needed.

</details>

<details>
<summary>Solution</summary>

```bash
ros2 service call /adi_iio_node/ListDevices adi_iio/srv/ListDevices
```

</details>

### Question 2: Channel Count

**How many channels does the ad7124-8 have?**

<details>
<summary>Hint</summary>

Use `ListChannels` with the device path as `iio_path`.

</details>

<details>
<summary>Solution</summary>

```bash
ros2 service call /adi_iio_node/ListChannels adi_iio/srv/ListChannels "{iio_path: 'ad7124-8'}"
```

Count the channels in the response.

</details>

### Question 3: Available Attributes

**What attributes are available on channel `input_voltage0-voltage1`?**

<details>
<summary>Hint</summary>

Use `ListAttributes` with the full channel path.

</details>

<details>
<summary>Solution</summary>

```bash
ros2 service call /adi_iio_node/ListAttributes adi_iio/srv/ListAttributes "{iio_path: 'ad7124-8/input_voltage0-voltage1'}"
```

</details>

### Question 4: Build-Your-Own Path

**Construct the IIO path to read the `scale` attribute of channel `input_voltage2-voltage3`:**

Write the path without executing (no peeking at solutions!):

```
Your answer: _________________________________
```

<details>
<summary>Solution</summary>

```
ad7124-8/input_voltage2-voltage3/scale
```

Full command:
```bash
ros2 service call /adi_iio_node/AttrReadString adi_iio/srv/AttrReadString "{attr_path: 'ad7124-8/input_voltage2-voltage3/scale'}"
```

</details>

## Bonus Challenge

**Explore another IIO device (if available):**

If your system has other IIO devices (check with `ListDevices`), explore their channels and attributes using the same pattern.

## Success Criteria

- [ ] Can list all IIO devices without referring to documentation
- [ ] Can navigate device → channel → attribute hierarchy
- [ ] Can construct correct IIO paths for any attribute
- [ ] Understand the naming convention for differential channels

# Exercise 2: Service Client and Processing

**Goal:** Implement the scale retrieval service client, scaling logic, and publisher.

**Reference:** [rclpy minimal_client](https://github.com/ros2/examples/tree/humble/rclpy/services/minimal_client)

---

## Step 2.1: Add Service Client Import

Add to your node file:

```python
from adi_iio.srv import AttrReadString
```

---

## Step 2.2: Create Service Client

In `__init__`, create a client and call the service to get the scale value:

<details>
<summary>Hint: Service client pattern</summary>

```python
# Create client
client = self.create_client(AttrReadString, '/adi_iio_node/AttrReadString')

# Wait for service
while not client.wait_for_service(timeout_sec=1.0):
    self.get_logger().info('Waiting for service...')

# Create request
request = AttrReadString.Request()
request.attr_path = 'ad7124-8/input_voltage0-voltage1/scale'

# Call synchronously
future = client.call_async(request)
rclpy.spin_until_future_complete(self, future)
response = future.result()

# Parse result
self.scale = float(response.message)
```

</details>

---

## Step 2.3: Add Publisher

The Int32MultiArray type is already imported. Add the publisher:

```python
# In __init__:
self.publisher = self.create_publisher(
    Int32MultiArray,
    '/ad7124_buffer/mV',
    10
)
```

---

## Step 2.4: Implement Scaling in Callback

In `buffer_callback`:

1. Apply scaling: `mV = int(raw * scale)` (scale is already in mV)
2. Build Int32MultiArray message
3. Publish

<details>
<summary>Hint: Scaling logic</summary>

```python
scaled_data = [int(raw * self.scale) for raw in msg.data]

out_msg = Int32MultiArray()
out_msg.layout = msg.layout
out_msg.data = scaled_data

self.publisher.publish(out_msg)
```

</details>

---

## Step 2.5: Test

```bash
# Terminal 1: Module 02 launch running
# Terminal 2: Run your node
ros2 run adc_processor adc_processor_node

# Terminal 3: Verify output
ros2 topic echo /ad7124_buffer/mV --once
```

**Expected:** Integer values in millivolt range (e.g., 2103, 2105)

---

## Checkpoint

- [ ] Scale value retrieved (check logs)
- [ ] `/ad7124_buffer/mV` topic exists
- [ ] Output values are in millivolt range
- [ ] Topic rate matches input (~10 Hz)

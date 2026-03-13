# Exercise 1: Package Creation Challenge

**Goal:** Create and configure a ROS2 Python package for the ADC processor.

---

## Step 1.1: Create the Package

Use `ros2 pkg create` to scaffold a new Python package:

```bash
cd src
ros2 pkg create --build-type ament_python adc_processor \
    --dependencies rclpy std_msgs adi_iio
```

**Expected output:**
```
going to create a new package
package name: adc_processor
...
creating ./adc_processor/package.xml
creating ./adc_processor/setup.py
```

---

## Step 1.2: Examine the Structure

```bash
tree adc_processor/
```

**Expected:**
```
adc_processor/
├── adc_processor/
│   └── __init__.py
├── package.xml
├── resource/
│   └── adc_processor
├── setup.cfg
├── setup.py
└── test/
```

---

## Step 1.3: Add the Node Template

Copy the minimal processor template to your package. From the workspace root:

```bash
cp modules/03-processing-package/code-templates/minimal_processor.py \
   src/adc_processor/adc_processor/adc_processor_node.py
```

Alternatively, create the file manually by copying the content from the hands-on guide (Part 3, Step 3.1).

---

## Step 1.4: Configure Entry Points

Edit `setup.py` to register the executable:

<details>
<summary>Hint: entry_points format</summary>

```python
entry_points={
    'console_scripts': [
        'adc_processor_node = adc_processor.adc_processor_node:main',
    ],
},
```

</details>

---

## Step 1.5: Build and Verify

From the workspace root:

```bash
colcon build --packages-select adc_processor
source install/setup.bash
ros2 pkg list | grep adc_processor
```

**Expected:** `adc_processor` appears in the list.

---

## Step 1.6: Run the Node

With Module 02's launch running in Terminal 1:

```bash
ros2 run adc_processor adc_processor_node --ros-args --log-level debug
```

**Expected:** Logs showing "Received buffer with X samples"

---

## Checkpoint

- [ ] Package created with correct dependencies
- [ ] setup.py has entry_points configured
- [ ] `colcon build` succeeds
- [ ] Node runs and logs buffer data

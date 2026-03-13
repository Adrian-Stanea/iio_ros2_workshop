# Verification

This guide verifies connectivity between your Windows host and the RPi5.

## 1. Open Project in Devcontainer

1. Open VS Code
2. **File** > **Open Folder** > select `adi_ros2/docs/training`
3. VS Code detects `.devcontainer/devcontainer.json`
4. Click **"Reopen in Container"** when prompted

   Or use Command Palette: `Ctrl+Shift+P` > "Dev Containers: Reopen in Container"

5. Wait for container to build

**Verify:** Terminal prompt shows `/adc_workshop_ws`

## 2. Test IIO Connection to RPi5

In the devcontainer terminal, replace `<rpi5-ip>` with your RPi5's IP address:

```bash
iio_info -u ip:<rpi5-ip>
```

Example:
```bash
iio_info -u ip:192.168.1.50
```

**Expected output:**

```
IIO context has 1 devices:
    iio:device0: ad7124-8
        4 channels found:
            voltage0: ...
            voltage1: ...
            voltage2: ...
            voltage3: ...
```

---

## 3. Quick Read Test

Verify you can read data from the sensor:

```bash
iio_readdev -u ip:<rpi5-ip> -b 256 -s 10 ad7124-8 voltage0-voltage1
```

**Expected:** some characters printed associated with the raw ADC data

---

## Setup Complete!

You have successfully:
- Configured your Windows development environment
- Set up RPi5 with the AD7124 sensor
- Verified network connectivity from the devcontainer

Proceed to [Module 1: Interacting with ADI Sensors](../01-adi-sensors/README.md)

---

## Optional: Verify ROS2 Environment

```bash
# Check ROS2 is available
ros2 --version

# List ADI packages
ros2 pkg list | grep adi
```

**Expected:** `adi_iio` appears in the package list

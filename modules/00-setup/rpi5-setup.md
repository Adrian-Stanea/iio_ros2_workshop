# RPi5 Setup

This guide covers setting up the Raspberry Pi 5 with the AD7124 sensor.

## 1. Flash Kuiper Linux

### Option A: Workshop Image (Recommended)

Download the pre-configured workshop image:

> **Download:** [Workshop Image](#) *(link coming soon)*

This image includes:

- Device tree overlays for AD7124

- Docker CLI


**Verify:**
1. Insert SD card into RPi5
2. Connect power, monitor, keyboard
3. Boot and login with `analog` / `analog`

## 2. Connect AD7124 to RPi5

>**Power off RPi5 before connecting!**

### GPIO Header Reference

![RPi5 Pinout](assets/rpi5-pinout.png)

### AD7124 to RPi5 Connections

![AD7124 to RPi5 Connections](assets/ad7124-to-rpi5-connections.png)

## 3. Connect M2K Signal Path

The M2K generates test signals that the AD7124 measures.

![M2K to AD7124 Connections](assets/m2k-to-ad7124-connections.png)

Use jumper wires to make connections as described in the diagram.


## 4. Boot and verify AD7124 detected:
```bash
iio_info | grep ad7124
```

Expected output includes: `ad7124-8`

---

## 5. Get RPi5 IP Address

```bash
hostname -I
```

Note this IP address (e.g., `192.168.1.50`). You'll need it to connect from your host machine.

**Tip:** For a consistent IP, configure DHCP reservation on your router or set a static IP on the RPi5.

---

## Next Steps

Proceed to [Verification](verification.md)

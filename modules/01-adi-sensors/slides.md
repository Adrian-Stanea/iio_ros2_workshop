---
marp: true
theme: default
paginate: true
header: "Module 1: Interacting with ADI Sensors via ROS2"
footer: "Analog Devices, Inc."
---

# Module 1: Interacting with ADI Sensors via ROS2

**Duration:** 20 minutes lecture + 40 minutes hands-on

---

## ROS2 Communication Patterns

```mermaid
graph LR
    subgraph Services ["Services: Request/Response"]
        C1[Client] -->|"1. Request"| S1[Server]
        S1 -->|"2. Response"| C1
    end

    subgraph Topics ["Topics: Publish/Subscribe"]
        P[Publisher] -->|"Continuous"| T((Topic))
        T --> Sub1[Subscriber 1]
        T --> Sub2[Subscriber 2]
    end
```

| Aspect       | Services         | Topics            |
| ------------ | ---------------- | ----------------- |
| **Pattern**  | Request/Response | Publish/Subscribe |
| **Timing**   | Synchronous      | Asynchronous      |
| **Use Case** | Commands, config | Data streaming    |

<!--
Speaker Notes:
- Services are like HTTP requests - you ask, you get an answer
- Topics are like radio broadcasts - publishers transmit, anyone tunes in
- adi_iio is different from most drivers
-->

---

## The adi_iio Difference: Services-First

**Typical ROS2 driver:** Auto-publishes data on startup

**adi_iio:** NO topics by default - created ON DEMAND

```mermaid
graph TB
    subgraph ADI ["adi_iio Architecture"]
        N2[adi_iio_node] --> SVC[Services Only]
        SVC -->|"AttrEnableTopic"| T2[Topics Created On Demand]
        T2 --> S2[subscriber]
    end

    style SVC fill:#fbbc04
    style T2 fill:#34a853,color:#fff
```

**Why?** Control, efficiency, flexibility for 100s of IIO devices

---

## IIO Path Hierarchy

```
Context (root)
├── Device: ad7124-8
│   ├── Channel: input_voltage0-voltage1
│   │   ├── Attribute: raw
│   │   ├── Attribute: scale
│   │   └── Attribute: sampling_frequency
│   └── Channel: input_voltage2-voltage3
└── Device: (other IIO devices)
```

**Path Format:** `device/channel/attribute`

```
"ad7124-8"                              → Device
"ad7124-8/input_voltage0-voltage1"      → Channel
"ad7124-8/input_voltage0-voltage1/raw"  → Attribute
```

---

## AD7124-8 Differential Channels

```mermaid
graph LR
    subgraph Inputs ["Physical Inputs"]
        AIN0["AIN0"]
        AIN1["AIN1"]
        AIN2["AIN2"]
        AIN3["AIN3"]
    end

    subgraph Differential ["Differential Channels"]
        D1["voltage0-voltage1\n(AIN0 - AIN1)"]
        D2["voltage2-voltage3\n(AIN2 - AIN3)"]
    end

    AIN0 --> D1
    AIN1 --> D1
    AIN2 --> D2
    AIN3 --> D2
```

Channel naming: `input_voltageX-voltageY` = Differential (AINX - AINY)

---

## adi_iio Services

```mermaid
graph TB
    subgraph Discovery ["Discovery"]
        SC["ScanContext"]
        LD["ListDevices"]
        LC["ListChannels"]
        LA["ListAttributes"]
    end

    subgraph ReadWrite ["Read/Write"]
        ARS["AttrReadString"]
        AWS["AttrWriteString"]
    end

    subgraph TopicControl ["Topic Control"]
        AET["AttrEnableTopic"]
        BET["BufferEnableTopic"]
    end

    SC --> LD --> LC --> LA
```

---

## From Services to Topics

```mermaid
sequenceDiagram
    participant CLI as ros2 service call
    participant Node as adi_iio_node
    participant Topic as New Topic

    Note over CLI,Topic: Before: No data topics

    CLI->>Node: AttrEnableTopic(path, rate=10.0)
    Node-->>Topic: Creates topic
    Node-->>CLI: Success

    Note over CLI,Topic: After: Topic publishes at 10 Hz

    loop Every 100ms
        Node->>Topic: Publish value
    end
```

---

## Attribute Topics vs Buffer Topics

| Attribute Topics        | Buffer Topics     |
| ----------------------- | ----------------- |
| One attribute at a time | Multiple channels |
| String messages         | Structured data   |
| Lower rates             | High-performance  |

```mermaid
graph LR
    subgraph Attr ["Attribute Topic"]
        A1["AttrEnableTopic"] --> AT["single value stream"]
    end

    subgraph Buffer ["Buffer Topic"]
        B1["BufferEnableTopic"] --> BT["multi-sample array"]
    end
```

---

## Complete Workflow

```mermaid
graph LR
    A["1. Start Node"] --> B["2. Discover"]
    B --> C["3. Configure"]
    C --> D["4. Enable Topics"]
    D --> E["5. Use Data"]

    style A fill:#4285f4,color:#fff
    style E fill:#34a853,color:#fff
```

1. `ros2 run adi_iio adi_iio_node`
2. `ListDevices` → `ListChannels` → `ListAttributes`
3. `AttrReadString` / `AttrWriteString`
4. `AttrEnableTopic` or `BufferEnableTopic`
5. `ros2 topic echo` or custom nodes

---

## Hands-on Overview

| Part | Activity                | Duration |
| ---- | ----------------------- | -------- |
| 1    | Discovery & IIO Paths   | 10 min   |
| 2    | Read Attributes         | 5 min    |
| 3    | Write Attributes        | 5 min    |
| 4    | Enable Attribute Topics | 10 min   |
| 5    | Buffer Topics           | 10 min   |

**Hardware:** AD7124-8 ADC + Raspberry Pi 5 + Docker

---

## Key Takeaways

1. **Services-First:** adi_iio uses services; topics created on demand

2. **IIO Paths:** `device/channel/attribute` hierarchy

3. **Discovery:** ScanContext → ListDevices → ListChannels → ListAttributes

4. **Bridge:** AttrEnableTopic / BufferEnableTopic create topics

5. **Control Flow:** Services for config, Topics for streaming

#!/usr/bin/env python3
"""
ADC Processor Node - Minimal Template

This node subscribes to the raw buffer topic and logs received data.
Your task: Add service client, scaling logic, and publisher.

Stage 2 imports you'll need:
    from adi_iio.srv import AttrReadString
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray


class AdcProcessorNode(Node):
    def __init__(self):
        super().__init__('adc_processor_node')

        # Subscriber to buffer topic
        self.subscription = self.create_subscription(
            Int32MultiArray,
            '/ad7124_buffer',
            self.buffer_callback,
            10
        )

        self.get_logger().info('ADC Processor Node started!')
        self.get_logger().info('Subscribed to /ad7124_buffer')

    def buffer_callback(self, msg):
        """Process incoming buffer data."""
        sample_count = len(msg.data)
        self.get_logger().debug(f'Received buffer with {sample_count} samples')

        # TODO: Implement scaling and publishing
        # 1. Get scale value via service client (do this once in __init__)
        #    - Service: /adi_iio_node/AttrReadString
        #    - attr_path: 'ad7124-8/input_voltage0-voltage1/scale'
        # 2. Apply scale: mV = int(raw * scale)  (scale is already in mV)
        # 3. Publish to /ad7124_buffer/mV as Int32MultiArray


def main(args=None):
    rclpy.init(args=args)
    node = AdcProcessorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

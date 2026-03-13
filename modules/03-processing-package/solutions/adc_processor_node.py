#!/usr/bin/env python3
"""
ADC Processor Node - Complete Solution

Subscribes to raw ADC buffer, retrieves scale via service client,
applies scaling, and publishes millivolt values as integers.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from adi_iio.srv import AttrReadString


class AdcProcessorNode(Node):
    def __init__(self):
        super().__init__('adc_processor_node')

        # Create service client and get scale value
        self.scale = self._get_scale_value()
        self.get_logger().info(f'Scale value: {self.scale}')

        # Publisher for processed data (mV as integers)
        self.publisher = self.create_publisher(
            Int32MultiArray,
            '/ad7124_buffer/mV',
            10
        )

        # Subscriber to buffer topic
        self.subscription = self.create_subscription(
            Int32MultiArray,
            '/ad7124_buffer',
            self.buffer_callback,
            10
        )

        self.get_logger().info('ADC Processor Node started!')
        self.get_logger().info('Subscribed to /ad7124_buffer')
        self.get_logger().info('Publishing to /ad7124_buffer/mV')

    def _get_scale_value(self) -> float:
        """Retrieve scale value from adi_iio_node via service call."""
        client = self.create_client(AttrReadString, '/adi_iio_node/AttrReadString')

        self.get_logger().info('Waiting for AttrReadString service...')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')

        request = AttrReadString.Request()
        request.attr_path = 'ad7124-8/input_voltage0-voltage1/scale'

        self.get_logger().debug(f'Calling service with attr_path: {request.attr_path}')
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        response = future.result()
        if response.success:
            scale = float(response.message)
            self.get_logger().info(f'Retrieved scale: {scale}')
            return scale
        else:
            self.get_logger().error(f'Failed to get scale: {response.message}')
            raise RuntimeError(f'Failed to get scale: {response.message}')

    def buffer_callback(self, msg):
        """Process incoming buffer data and publish scaled values."""
        if len(msg.data) == 0:
            self.get_logger().warn('Received empty buffer')
            return

        # Apply scaling: mV = raw * scale (scale is already in mV)
        scaled_data = [int(raw * self.scale) for raw in msg.data]

        # Build output message preserving layout
        out_msg = Int32MultiArray()
        out_msg.layout = msg.layout
        out_msg.data = scaled_data

        self.publisher.publish(out_msg)

        sample_count = len(msg.data)
        self.get_logger().debug(
            f'Processed {sample_count} samples, '
            f'range: {min(scaled_data)} - {max(scaled_data)} mV'
        )


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

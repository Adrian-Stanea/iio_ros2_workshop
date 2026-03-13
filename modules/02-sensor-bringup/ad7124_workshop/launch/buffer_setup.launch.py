# Copyright 2025 Analog Devices, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
AD7124 Buffer Setup Launch File

This launch file creates a buffer and enables a topic for streaming data.

Two-step process:
1. BufferCreate - Allocates buffer memory for specified channels
2. BufferEnableTopic - Creates a ROS2 topic that publishes buffer data

IMPORTANT: BufferEnableTopic must run AFTER BufferCreate completes!
Use RegisterEventHandler with OnProcessExit for proper sequencing.

Exercise: Complete the TODOs to enable the buffer topic.

Hints:
- Check the BufferEnableTopic interface:
  ros2 interface show adi_iio/srv/BufferEnableTopic
- Expected topic name: /ad7124_buffer
- Suggested loop_rate: 1.0 (Hz)
"""

from launch import LaunchDescription
from launch.actions import ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import FindExecutable


def generate_launch_description():
    # Configuration values
    device_path = 'ad7124-8'
    channels = ['input_voltage0-voltage1', 'input_voltage2-voltage3']
    samples_count = 400
    topic_name = '/ad7124_buffer'
    loop_rate = 1.0

    # =========================================================================
    # Step 1: Create the buffer (COMPLETE - this is your reference)
    # =========================================================================

    # BufferCreate allocates memory for capturing samples
    # Note: channels array uses channel names WITHOUT the device prefix
    buffer_create = ExecuteProcess(
        name='buffer_create',
        cmd=[[
            FindExecutable(name='ros2'),
            ' service call ',
            '/adi_iio_node/BufferCreate ',
            'adi_iio/srv/BufferCreate ',
            f"\"{{device_path: '{device_path}', ",
            f"channels: {channels}, ",
            f"samples_count: {samples_count}}}\"",
        ]],
        shell=True,
        output='screen',
    )

    # =========================================================================
    # Step 2: Enable the buffer topic (TODO)
    # =========================================================================

    # TODO 1: Create BufferEnableTopic service call
    #
    # The BufferEnableTopic service requires:
    #   - device_path: The IIO device (use the variable above)
    #   - topic_name: The ROS2 topic to create (use the variable above)
    #   - loop_rate: Publishing frequency in Hz (use the variable above)
    #
    # First, check the interface to see exact field names:
    #   ros2 interface show adi_iio/srv/BufferEnableTopic
    #
    # Follow the pattern from buffer_create above.
    #
    # buffer_enable_topic = ExecuteProcess(
    #     name='buffer_enable_topic',
    #     cmd=[[
    #         # YOUR CODE HERE
    #     ]],
    #     shell=True,
    #     output='screen',
    # )

    # =========================================================================
    # Sequencing: BufferEnableTopic must run AFTER BufferCreate completes
    # =========================================================================

    # TODO 2: Add event handler for proper sequencing
    #
    # Use RegisterEventHandler with OnProcessExit to ensure buffer_enable_topic
    # runs only after buffer_create has finished.
    #
    # Pattern:
    # on_buffer_created = RegisterEventHandler(
    #     OnProcessExit(
    #         target_action=buffer_create,
    #         on_exit=[buffer_enable_topic],
    #     )
    # )

    # =========================================================================
    # Return launch description
    # =========================================================================

    # Currently only buffer_create is active (topic won't be enabled)
    return LaunchDescription([
        buffer_create,
        # on_buffer_created,
    ])

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
AD7124 Attribute Configuration Launch File

This launch file configures the AD7124 channels using service calls.
Each ExecuteProcess runs a ros2 service call command.

Exercise: Complete the TODOs to configure all attributes for both channels.

Hints:
- Use ListAttributes to discover available attributes:
  ros2 service call /adi_iio_node/ListAttributes adi_iio/srv/ListAttributes \\
    "{iio_path: 'ad7124-8/input_voltage0-voltage1'}"
- Attribute path pattern: ad7124-8/<channel>/<attribute>
- Channel names: input_voltage0-voltage1, input_voltage2-voltage3
"""

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import FindExecutable


def generate_launch_description():
    # Configuration values
    scale = '0.000149011'
    sampling_frequency = '1000'

    # =========================================================================
    # Channel 0: input_voltage0-voltage1
    # =========================================================================

    # COMPLETE: Set scale for channel 0 (this is your reference example)
    ch0_scale = ExecuteProcess(
        name='ch0_scale',
        cmd=[[
            FindExecutable(name='ros2'),
            ' service call ',
            '/adi_iio_node/AttrWriteString ',
            'adi_iio/srv/AttrWriteString ',
            '"{attr_path: \'ad7124-8/input_voltage0-voltage1/scale\', ',
            f"value: '{scale}'}}\"",
        ]],
        shell=True,
    )


    # TODO 1: Set sampling_frequency for channel 0
    # Follow the same pattern as ch0_scale above, but:
    # - Change the attribute name from 'scale' to 'sampling_frequency'
    # - Use the sampling_frequency variable instead of scale
    #
    # ch0_sampling_freq = ExecuteProcess(
    #     cmd=[[
    #         # YOUR CODE HERE
    #     ]],
    #     shell=True,
    # )

    # =========================================================================
    # Channel 1: input_voltage2-voltage3
    # =========================================================================

    # TODO 2: Set scale for channel 1
    # Follow the same pattern as ch0_scale, but change the channel name
    # from 'input_voltage0-voltage1' to 'input_voltage2-voltage3'
    #
    # ch1_scale = ExecuteProcess(
    #     cmd=[[
    #         # YOUR CODE HERE
    #     ]],
    #     shell=True,
    # )

    # TODO 3: Set sampling_frequency for channel 1
    #
    # ch1_sampling_freq = ExecuteProcess(
    #     cmd=[[
    #         # YOUR CODE HERE
    #     ]],
    #     shell=True,
    # )

    # =========================================================================
    # Return launch description
    # =========================================================================

    # Currently only ch0_scale is active
    return LaunchDescription([
        ch0_scale,
        # ch0_sampling_freq,
        # ch1_scale,
        # ch1_sampling_freq,
    ])

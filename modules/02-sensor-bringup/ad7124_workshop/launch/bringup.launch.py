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
AD7124 Workshop Bringup Launch File

This launch file orchestrates:
1. Starting the adi_iio_node with parameters from YAML config
2. Running attribute configuration after node starts
3. Running buffer setup after configuration completes

Key Concepts:
- IncludeLaunchDescription: Compose launch files
- RegisterEventHandler: React to process events
- OnProcessStart: Trigger actions when a process starts
- OnExecutionComplete: Trigger actions when a process completes
"""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    RegisterEventHandler,
)
from launch.event_handlers import OnExecutionComplete, OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    # Get package directories
    pkg_dir = get_package_share_directory('ad7124_workshop')

    # Path to YAML config file
    config_file = os.path.join(pkg_dir, 'config', 'ad7124.yaml')

    # 1. Start the adi_iio_node with parameters from config file
    adi_iio_node = Node(
        package='adi_iio',
        executable='adi_iio_node',
        name='adi_iio_node',
        output='screen',
        emulate_tty=True,
        parameters=[config_file],
    )

    # 2. Include config_attributes launch file (runs after node starts)
    # config_attributes = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(pkg_dir, 'launch', 'config_attributes.launch.py')
    #     ),
    # )

    # Event handler: When adi_iio_node starts -> run config_attributes
    # on_node_start = RegisterEventHandler(
    #     OnProcessStart(
    #         target_action=adi_iio_node,
    #         on_start=[config_attributes],
    #     )
    # )

    # 3. Include buffer_setup launch file (runs after config completes)
    # buffer_setup = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(pkg_dir, 'launch', 'buffer_setup.launch.py')
    #     ),
    # )

    # Event handler: When config_attributes completes -> run buffer_setup
    # on_config_complete = RegisterEventHandler(
    #     OnExecutionComplete(
    #         target_action=config_attributes,
    #         on_completion=[buffer_setup],
    #     )
    # )

    return LaunchDescription([
        adi_iio_node,
        # on_node_start,
        # on_config_complete,
    ])

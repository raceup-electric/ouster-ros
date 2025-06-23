# Copyright 2023 Ouster, Inc.
#
# Modified by RaceUP team, original file: driver.launch.py from ouster-ros package
#  the lifecycle transitions are handled by the node (auto_start)
#  there is no rviz option
#  when finalized it doesn't shutdown everything

"""Launch a sensor node along with os_cloud and os_"""

from pathlib import Path
import launch
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import LifecycleNode
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    """
    Generate launch description for running ouster_ros components separately each
    component will run in a separate process).
    """
    ouster_ros_pkg_dir = get_package_share_directory('ouster_ros')
    default_params_file = \
        Path(ouster_ros_pkg_dir) / 'config' / 'driver_params.yaml'
    params_file = LaunchConfiguration('params_file')
    params_file_arg = DeclareLaunchArgument('params_file',
                                            default_value=str(
                                                default_params_file),
                                            description='name or path to the parameters file to use.')

    ouster_ns = LaunchConfiguration('ouster_ns')
    ouster_ns_arg = DeclareLaunchArgument(
        'ouster_ns', default_value='ouster')

    os_driver_name = LaunchConfiguration('os_driver_name')
    os_driver_name_arg = DeclareLaunchArgument(
        'os_driver_name', default_value='os_driver')

    os_driver = LifecycleNode(
        package='ouster_ros',
        executable='os_driver',
        name=os_driver_name,
        namespace=ouster_ns,
        parameters=[params_file, {'auto_start': True}],
        output='screen',
    )

    return launch.LaunchDescription([
        params_file_arg,
        ouster_ns_arg,
        os_driver_name_arg,
        os_driver,
    ])

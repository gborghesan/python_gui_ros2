from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='python_gui',
            executable='gui_sender',
            name='sender',
            parameters=[
            {"xml_button_file":  get_package_share_directory('python_gui')+"/xml/default.xml" },
        ]
        ),
    ])

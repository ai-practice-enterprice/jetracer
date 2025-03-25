from launch import LaunchDescription
from ament_index_python import get_package_share_directory
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument , ExecuteProcess
from launch.substitutions import LaunchConfiguration , PythonExpression

def generate_launch_description():
    robot_controllers = PathJoinSubstitution([
        get_package_share_directory("jetracer_description"),
            "config",
            "jetracer_controllers.yaml"
    ])

    robot_namespace = LaunchConfiguration('ns')
    robot_namespace_arg = DeclareLaunchArgument(
        name='ns',
        description='[ARG] required namespace to keep nodes and topics separate when running multiple robots in the same simulation'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')
    use_sim_time_arg = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='false',
        description='[ARG] tells the robot_state_publisher to use the simulation time or just unix timestamp'
    )


    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        namespace=robot_namespace,
        arguments=['joint_state_broadcaster',
                    '--switch-timeout', '10',
        ],
    )

    # ackermann_steering_controller_spawner = Node(
    #     package='controller_manager',
    #     executable='spawner',
    #     namespace=robot_namespace,
    #     arguments=['ackermann_steering_controller',
    #                '--param-file',robot_controllers,
    #                '--switch-timeout', '60'
    #     ],
    #     remappings=[
    #         ("/ackermann_steering_controller/tf_odometry","tf")
    #     ]
    # )

    return LaunchDescription([
        use_sim_time_arg,
        robot_namespace_arg,
        joint_state_broadcaster_spawner,
        # RegisterEventHandler(
        #     event_handler=OnProcessExit(
        #         target_action=joint_state_broadcaster_spawner,
        #         on_exit=[ackermann_steering_controller_spawner]
        #     ))        
    ])
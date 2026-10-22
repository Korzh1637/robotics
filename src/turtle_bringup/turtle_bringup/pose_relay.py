import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from turtlesim_msgs.msg import Pose


class PoseRelay(Node):
    def __init__(self):
        super().__init__('pose_relay')

        self.declare_parameter('subscriber_reliability', 'best_effort')
        sub_rel_str = self.get_parameter('subscriber_reliability').value
        sub_rel = (ReliabilityPolicy.RELIABLE
                   if sub_rel_str == 'reliable'
                   else ReliabilityPolicy.BEST_EFFORT)

        sub_qos = QoSProfile(
            reliability=sub_rel,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        self.sub = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_cb, sub_qos)

        pub_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        self.pub = self.create_publisher(Pose, 'sensor_pose', pub_qos)

    def pose_cb(self, msg):
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PoseRelay()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
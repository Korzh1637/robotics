import math

import rclpy
from geometry_msgs.msg import Twist
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node
from turtlesim_msgs.msg import Pose

from .control import choose_command


def validate_params(linear_speed, turn_rate, publish_hz):
    """Чистая функция валидации. Возвращает (ok, reason)."""
    for name, val in [('linear_speed', linear_speed),
                        ('turn_rate', turn_rate),
                        ('publish_hz', publish_hz)]:
        if not isinstance(val, (int, float)) or math.isnan(float(val)):
            return False, f'{name} is NaN or not a number'
    if not (0.0 <= float(linear_speed) <= 1.0):
        return False, f'linear_speed {linear_speed} out of [0, 1]'
    if not (-1.0 <= float(turn_rate) <= 1.0):
        return False, f'turn_rate {turn_rate} out of [-1, 1]'
    if not (1.0 <= float(publish_hz) <= 30.0):
        return False, f'publish_hz {publish_hz} out of [1, 30]'
    return True, 'ok'


class PatrolNode(Node):
    def __init__(self):
        super().__init__('patrol')

        self.declare_parameter('linear_speed', 0.5)
        self.declare_parameter('turn_rate', 0.3)
        self.declare_parameter('publish_hz', 10.0)

        self._linear_speed = 0.5
        self._turn_rate = 0.3
        self._publish_hz = 10.0

        self.last_pose = None
        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self._on_pose, 10)
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        self.timer = self.create_timer(1.0 / self._publish_hz, self._on_timer)

        self.add_on_set_parameters_callback(self._on_set_parameters)

    def _on_pose(self, msg):
        self.last_pose = msg

    def _on_timer(self):
        twist = choose_command(self.last_pose, self._linear_speed, self._turn_rate)
        self.cmd_pub.publish(twist)

    def _on_set_parameters(self, params):
        new_lin = self._linear_speed
        new_turn = self._turn_rate
        new_hz = self._publish_hz

        for p in params:
            if p.name == 'linear_speed':
                new_lin = p.value
            elif p.name == 'turn_rate':
                new_turn = p.value
            elif p.name == 'publish_hz':
                new_hz = p.value

        ok, reason = validate_params(new_lin, new_turn, new_hz)
        if not ok:
            self.get_logger().warning(f'reject params: {reason}')
            return SetParametersResult(successful=False, reason=reason)

        self._linear_speed = new_lin
        self._turn_rate = new_turn

        if new_hz != self._publish_hz:
            self.timer.cancel()
            self._publish_hz = new_hz
            self.timer = self.create_timer(1.0 / self._publish_hz, self._on_timer)
            self.get_logger().info(f'timer rebuilt, period={1.0/self._publish_hz:.4f}s')
        else:
            self._publish_hz = new_hz

        return SetParametersResult(successful=True)


def main(args=None):
    rclpy.init(args=args)
    node = PatrolNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
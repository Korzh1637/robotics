from geometry_msgs.msg import Twist


def choose_command(pose, linear_speed, turn_rate):
    """Чистая функция: возвращает команду на основе позы."""
    twist = Twist()
    if pose is None:
        twist.linear.x = 0.0
        twist.angular.z = 0.0
    else:
        twist.linear.x = float(linear_speed)
        twist.angular.z = float(turn_rate)
    return twist

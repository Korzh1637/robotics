import pytest
from patrol.control import choose_command
from patrol.patrol import validate_params


@pytest.mark.parametrize('lin,turn,hz,ok', [
    (0.5, 0.3, 10.0, True),
    (0.0, 0.0, 1.0, True),
    (1.0, 1.0, 30.0, True),
    (1.0, -1.0, 15.0, True),
    (0.5, 0.3, 5.0, True),
    (0.5, 0.3, 0.0, False),
    (-0.1, 0.3, 10.0, False),
    (1.1, 0.3, 10.0, False),
    (0.5, 1.5, 10.0, False),
    (0.5, 0.3, 0.5, False),
    (0.5, 0.3, 31.0, False),
    (float('nan'), 0.3, 10.0, False),
    (0.5, float('nan'), 10.0, False),
    (0.5, 0.3, float('nan'), False),
])
def test_validate_params(lin, turn, hz, ok):
    assert validate_params(lin, turn, hz)[0] is ok


def test_zero_hz_reason():
    ok, reason = validate_params(0.5, 0.3, 0.0)
    assert not ok
    assert 'publish_hz' in reason


def test_choose_command_no_pose():
    twist = choose_command(None, 0.5, 0.3)
    assert twist.linear.x == 0.0
    assert twist.angular.z == 0.0


def test_choose_command_with_pose():
    class MockPose:
        pass
    pose = MockPose()

    twist = choose_command(pose, 0.7, -0.5)
    assert twist.linear.x == 0.7
    assert twist.angular.z == -0.5


def test_choose_command_respects_parameters():
    class MockPose:
        pass
    pose = MockPose()

    twist1 = choose_command(pose, 0.3, 0.2)
    twist2 = choose_command(pose, 0.8, -0.9)

    assert twist1.linear.x == 0.3
    assert twist1.angular.z == 0.2
    assert twist2.linear.x == 0.8
    assert twist2.angular.z == -0.9
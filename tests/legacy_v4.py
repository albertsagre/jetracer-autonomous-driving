"""Verbatim copy of the speed-mode logic from road_following_V4 (as run on the car).

Only change: widget reads/writes replaced by a function argument and return
value (``throttle_slider.value`` -> ``throttle``, ``speed_slider.value`` -> ``mode``).
Used as the reference (oracle) for the refactored scheduler.
"""


def legacy_v4_throttle(throttle, steering, mode):  # noqa: C901 - intentionally verbatim
    steering_max = 0.13
    steering_min = -0.13

    if mode == 0:
        throttle = 0

    elif mode == 1:
        if (steering<=steering_max and steering>=steering_min and throttle<0.14 and throttle>0.11):  # noqa: E501
            throttle += 0.001
        elif((steering>steering_max or steering<steering_min) and throttle>0.12):
            throttle += - 0.001

    elif mode == 2:
        if (steering<=steering_max and steering>=steering_min and throttle<0.15 and throttle>0.11):  # noqa: E501
            throttle += 0.001
        elif((steering>steering_max or steering<steering_min) and throttle>0.13):
            throttle += - 0.001

    elif mode == 3:
        if (steering<=steering_max and steering>=steering_min and throttle<0.15 and throttle>0.11):  # noqa: E501
            throttle += 0.001
        elif((steering>steering_max or steering<steering_min) and throttle>0.14):
            throttle += - 0.001

    elif mode == 4:
        if (steering<=steering_max and steering>=steering_min and throttle<0.16 and throttle>0.11):  # noqa: E501
            throttle += 0.001
        elif((steering>steering_max or steering<steering_min) and throttle>0.15):
            throttle += - 0.001

    elif mode == 5:
        if (steering<=steering_max and steering>=steering_min and throttle<0.17 and throttle>0.11):  # noqa: E501
            throttle += 0.001
        elif((steering>steering_max or steering<steering_min) and throttle>0.16):
            throttle += - 0.001

    elif mode == 6:
        if (steering<=steering_max and steering>=steering_min and throttle<0.18 and throttle>0.11):  # noqa: E501
            throttle += 0.001
        elif((steering>steering_max or steering<steering_min) and throttle>0.17):
            throttle += - 0.001

    elif mode == 7:
        if (steering<=steering_max and steering>=steering_min and throttle<0.19 and throttle>0.11):  # noqa: E501
            throttle += 0.001
        elif((steering>steering_max or steering<steering_min) and throttle>0.18):
            throttle += - 0.001

    elif mode == 8:
        if (steering<=steering_max and steering>=steering_min and throttle<0.2 and throttle>0.11):  # noqa: E501
            throttle += 0.001
        elif((steering>steering_max or steering<steering_min) and throttle>0.19):
            throttle += - 0.001

    else:
        throttle = throttle

    return throttle

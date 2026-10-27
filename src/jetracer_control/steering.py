"""Steering law and image-coordinate helpers.

The network regresses a target point ``(x, y)`` in normalised image
coordinates ([-1, 1], origin at the image centre). Only ``x`` is used for
lateral control, through a static proportional law::

    steering = clip(gain * x + bias, -1, 1)

On the car the gain was negative (about -0.65) because of the servo
orientation of the chassis.
"""

from typing import Tuple

__all__ = ["steering_command", "normalized_to_pixel"]


def steering_command(network_x: float, gain: float, bias: float = 0.0) -> float:
    """Map the network's horizontal target to a saturated steering command."""
    steering = network_x * gain + bias
    return max(-1.0, min(1.0, steering))


def normalized_to_pixel(x: float, y: float, width: int, height: int) -> Tuple[int, int]:
    """Convert a normalised target point to pixel coordinates for overlays.

    Note: the archived V2-V4 notebooks set ``y = output[0]`` instead of
    ``output[1]``, so the overlay point always lay on the image diagonal.
    This helper takes both coordinates explicitly (see docs/known-issues.md).
    """
    px = int(width * (x / 2.0 + 0.5))
    py = int(height * (y / 2.0 + 0.5))
    return px, py

"""Steering-based throttle scheduler (iteration 4, "speed modes").

This is the speed-control logic that ran on the car in
``notebooks/07_road_following_v4_speed_modes.ipynb``, extracted from the
UI callback and rewritten as a small, table-driven, testable function.

Behaviour
---------
The scheduler is called once per camera frame (15 fps on the car). It is a
rate-limited, two-level controller driven by the steering command:

* **Straight** (``|steering| <= steering_threshold``): throttle ramps *up* by
  ``step`` per frame, but only while it is inside the armed band
  ``(arm_floor, straight_ceiling)``.
* **Corner** (``|steering| > steering_threshold``): throttle ramps *down* by
  ``step`` per frame while it is above ``corner_floor``.
* **Mode 0**: throttle is forced to 0 (also used by the emergency stop).
* Otherwise the throttle is held.

The ``arm_floor`` (0.11) sits just below the throttle at which the car starts
to move (~0.12 with a well-charged battery). Below it the scheduler never
accelerates, so the operator has to "arm" the car by setting an initial
throttle above the floor: a deliberate safety interlock.

``tests/test_speed_scheduler.py`` checks this implementation against a
verbatim copy of the original notebook code on 200,000 random inputs and
on closed-loop sequences.
"""

from typing import Dict, NamedTuple

__all__ = [
    "SpeedMode",
    "SPEED_MODES",
    "STEERING_THRESHOLD",
    "ARM_FLOOR",
    "RAMP_STEP",
    "next_throttle",
]


class SpeedMode(NamedTuple):
    """Throttle band of one speed mode (normalised throttle units, 0..1)."""

    straight_ceiling: float  # ramp-up stops once throttle reaches this value
    corner_floor: float  # ramp-down stops once throttle reaches this value


# Values tuned experimentally on the test track (thesis, section 7.4.3).
# Mode 3 shares the straight ceiling of mode 2 in the original tuning;
# it is kept as-is to stay faithful to the tested configuration.
SPEED_MODES: Dict[int, SpeedMode] = {
    1: SpeedMode(straight_ceiling=0.14, corner_floor=0.12),
    2: SpeedMode(straight_ceiling=0.15, corner_floor=0.13),
    3: SpeedMode(straight_ceiling=0.15, corner_floor=0.14),
    4: SpeedMode(straight_ceiling=0.16, corner_floor=0.15),
    5: SpeedMode(straight_ceiling=0.17, corner_floor=0.16),
    6: SpeedMode(straight_ceiling=0.18, corner_floor=0.17),
    7: SpeedMode(straight_ceiling=0.19, corner_floor=0.18),
    8: SpeedMode(straight_ceiling=0.20, corner_floor=0.19),
}

STEERING_THRESHOLD = 0.13  # |steering| above this counts as a corner
ARM_FLOOR = 0.11  # no acceleration below this throttle (operator must arm)
RAMP_STEP = 0.001  # throttle change per frame (0.015 / s at 15 fps)
STOP_MODE = 0


def next_throttle(
    throttle: float,
    steering: float,
    mode: int,
    steering_threshold: float = STEERING_THRESHOLD,
    arm_floor: float = ARM_FLOOR,
    step: float = RAMP_STEP,
) -> float:
    """Return the throttle command for the next frame.

    Args:
        throttle: current throttle command.
        steering: steering command after gain and bias, nominally in [-1, 1].
        mode: speed mode; 0 stops the car, 1..8 select a band from
            ``SPEED_MODES``. Unknown modes hold the current throttle.
        steering_threshold: straight/corner decision threshold.
        arm_floor: throttle below which the scheduler never accelerates.
        step: ramp increment per call.
    """
    if mode == STOP_MODE:
        return 0
    band = SPEED_MODES.get(mode)
    if band is None:
        return throttle

    # Comparisons are written exactly as in the original notebook so the
    # floating-point behaviour is bit-for-bit identical.
    straight = steering <= steering_threshold and steering >= -steering_threshold
    if straight and arm_floor < throttle < band.straight_ceiling:
        return throttle + step
    if not straight and throttle > band.corner_floor:
        return throttle - step
    return throttle

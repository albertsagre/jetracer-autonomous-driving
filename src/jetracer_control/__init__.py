"""Hardware-independent control logic extracted from the JetRacer notebooks."""

from .speed_scheduler import SPEED_MODES, SpeedMode, next_throttle
from .steering import normalized_to_pixel, steering_command

__all__ = [
    "SPEED_MODES",
    "SpeedMode",
    "next_throttle",
    "normalized_to_pixel",
    "steering_command",
]
__version__ = "1.0.0"

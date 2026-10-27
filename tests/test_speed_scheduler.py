import random

import pytest
from legacy_v4 import legacy_v4_throttle

from jetracer_control.speed_scheduler import (
    ARM_FLOOR,
    RAMP_STEP,
    SPEED_MODES,
    STEERING_THRESHOLD,
    next_throttle,
)

MODES = list(range(0, 10))  # 0..8 plus one unknown mode (9)


# --- Equivalence with the code that ran on the car -------------------------


def test_equivalent_to_v4_on_random_inputs():
    rng = random.Random(2023)
    for _ in range(200_000):
        throttle = rng.uniform(-0.01, 0.21)
        steering = rng.uniform(-1.2, 1.2)
        mode = rng.choice(MODES)
        assert next_throttle(throttle, steering, mode) == legacy_v4_throttle(
            throttle, steering, mode
        )


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize(
    "throttle",
    [0.0, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2],
)
@pytest.mark.parametrize("steering", [-STEERING_THRESHOLD, STEERING_THRESHOLD, -0.5, 0.0, 0.5])
def test_equivalent_to_v4_on_boundaries(mode, throttle, steering):
    assert next_throttle(throttle, steering, mode) == legacy_v4_throttle(throttle, steering, mode)


def test_equivalent_to_v4_closed_loop():
    """Feed each implementation its own output for long random runs (state drift check)."""
    rng = random.Random(7)
    for _ in range(200):
        a = b = rng.choice([0.0, 0.115, 0.12, 0.15])
        for _ in range(500):
            steering = rng.choice([0.0, 0.05, -0.1, 0.3, -0.6])
            mode = rng.choice(MODES) if rng.random() < 0.02 else 8
            a = next_throttle(a, steering, mode)
            b = legacy_v4_throttle(b, steering, mode)
            assert a == b


# --- Behavioural properties ------------------------------------------------


@pytest.mark.parametrize("throttle", [0.0, 0.12, 0.2])
def test_mode_zero_stops(throttle):
    assert next_throttle(throttle, 0.0, 0) == 0


def test_unknown_mode_holds_throttle():
    assert next_throttle(0.15, 0.0, 42) == 0.15


@pytest.mark.parametrize("mode", sorted(SPEED_MODES))
def test_not_armed_never_accelerates(mode):
    throttle = ARM_FLOOR - 0.005
    for _ in range(100):
        throttle = next_throttle(throttle, 0.0, mode)
    assert throttle == ARM_FLOOR - 0.005


@pytest.mark.parametrize("mode", sorted(SPEED_MODES))
def test_straight_converges_to_ceiling_without_overshoot(mode):
    band = SPEED_MODES[mode]
    throttle = 0.12
    for _ in range(200):
        throttle = next_throttle(throttle, 0.0, mode)
    assert band.straight_ceiling - 1e-9 <= throttle < band.straight_ceiling + RAMP_STEP


@pytest.mark.parametrize("mode", sorted(SPEED_MODES))
def test_corner_decays_to_floor(mode):
    band = SPEED_MODES[mode]
    throttle = band.straight_ceiling
    for _ in range(200):
        throttle = next_throttle(throttle, 0.6, mode)
    assert band.corner_floor - RAMP_STEP < throttle <= band.corner_floor + 1e-9


def test_throttle_never_exceeds_safety_limit():
    rng = random.Random(1)
    throttle = 0.12
    for _ in range(50_000):
        throttle = next_throttle(throttle, rng.uniform(-1, 1), rng.choice(range(1, 9)))
        assert throttle <= 0.2 + RAMP_STEP


def test_steering_symmetry():
    for s in (0.05, 0.13, 0.2, 0.9):
        for mode in SPEED_MODES:
            assert next_throttle(0.15, s, mode) == next_throttle(0.15, -s, mode)

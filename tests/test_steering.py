import pytest

from jetracer_control.steering import normalized_to_pixel, steering_command


@pytest.mark.parametrize(
    "x, gain, bias, expected",
    [
        (0.0, -0.65, 0.0, 0.0),
        (0.5, -0.65, 0.0, -0.325),
        (0.5, -0.65, 0.1, -0.225),
        (2.0, 1.0, 0.0, 1.0),  # saturates high
        (-2.0, 1.0, 0.0, -1.0),  # saturates low
    ],
)
def test_steering_command(x, gain, bias, expected):
    assert steering_command(x, gain, bias) == pytest.approx(expected)


def test_pixel_mapping_corners_and_centre():
    assert normalized_to_pixel(-1, -1, 224, 224) == (0, 0)
    assert normalized_to_pixel(0, 0, 224, 224) == (112, 112)
    assert normalized_to_pixel(1, 1, 224, 224) == (224, 224)


def test_pixel_mapping_uses_independent_y():
    # Regression test for the archived notebooks, which plotted (x, x).
    px, py = normalized_to_pixel(0.5, -0.5, 224, 224)
    assert px != py

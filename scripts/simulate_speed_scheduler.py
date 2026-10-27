"""Offline replay of the speed scheduler on a synthetic steering profile.

This is NOT measured vehicle data. It replays the exact control logic used
on the car (``jetracer_control.next_throttle``) at the camera rate (15 fps)
on a hand-made straight/corner/straight/corner steering trace, to visualise
how the throttle command responds in two speed modes.

Usage:
    python scripts/simulate_speed_scheduler.py  # writes docs/images/speed_scheduler_response.png
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from jetracer_control import SPEED_MODES, next_throttle  # noqa: E402
from jetracer_control.speed_scheduler import STEERING_THRESHOLD  # noqa: E402

FPS = 15
ARMED_THROTTLE = 0.12  # operator sets this before selecting a speed mode
OUT = Path(__file__).resolve().parents[1] / "docs" / "images" / "speed_scheduler_response.png"

INK, INK_2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
SERIES = {4: "#2a78d6", 8: "#eb6834"}  # categorical slots 1 and 2


def steering_profile() -> np.ndarray:
    """Straight 6 s, left corner 2.5 s, straight 6 s, right corner 2.5 s, smoothed."""
    segments = [(6.0, 0.0), (2.5, 0.55), (6.0, 0.0), (2.5, -0.45)]
    raw = np.concatenate([np.full(int(d * FPS), s) for d, s in segments])
    kernel = np.ones(8) / 8  # ~0.5 s smoothing, like a real corner entry/exit
    smooth = np.convolve(np.pad(raw, (4, 3), mode="edge"), kernel, mode="valid")
    noise = np.random.default_rng(0).normal(0, 0.03, smooth.size)
    return smooth + noise


def run(mode: int, steering: np.ndarray) -> np.ndarray:
    throttle, out = ARMED_THROTTLE, []
    for s in steering:
        throttle = next_throttle(throttle, float(s), mode)
        out.append(throttle)
    return np.array(out)


def main() -> None:
    steering = steering_profile()
    t = np.arange(steering.size) / FPS

    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.edgecolor": INK_2,
            "axes.labelcolor": INK_2,
            "xtick.color": INK_2,
            "ytick.color": INK_2,
        }
    )
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(9, 5.2), sharex=True, gridspec_kw={"height_ratios": [1, 1.4]}
    )
    fig.patch.set_facecolor("#fcfcfb")

    ax1.axhspan(-STEERING_THRESHOLD, STEERING_THRESHOLD, color=GRID, lw=0)
    ax1.plot(t, steering, color=INK_2, lw=1.5)
    ax1.text(
        0.2, STEERING_THRESHOLD + 0.03, "straight band |steering| ≤ 0.13", color=INK_2, fontsize=9
    )
    ax1.set_ylabel("steering cmd")
    ax1.set_title("Steering input (synthetic lap)", loc="left", color=INK, fontsize=11)

    for mode, color in SERIES.items():
        band = SPEED_MODES[mode]
        thr = run(mode, steering)
        ax2.plot(t, thr, color=color, lw=2, label=f"mode {mode}")
        ax2.text(t[-1] + 0.2, thr[-1], f"mode {mode}", color=INK, va="center", fontsize=9)
        ax2.axhline(band.straight_ceiling, color=color, lw=0.8, ls=":", alpha=0.8)
    ax2.set_ylabel("throttle cmd")
    ax2.set_xlabel("time [s]  (15 fps, 0.001 per frame ramp)")
    ax2.set_title(
        "Throttle command from the speed scheduler (dotted: straight ceiling)",
        loc="left",
        color=INK,
        fontsize=11,
    )
    ax2.legend(frameon=False, loc="lower right")

    for ax in (ax1, ax2):
        ax.set_facecolor("#fcfcfb")
        ax.grid(axis="y", color=GRID, lw=0.8)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    ax2.set_xlim(0, t[-1] + 1.6)

    fig.text(
        0.01,
        0.005,
        "Offline replay of the on-car control logic - not measured vehicle data.",
        color=INK_2,
        fontsize=8,
    )
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(OUT, dpi=150)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

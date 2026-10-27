# Reproducing the setup

## 1. Hardware

Assemble the [Waveshare JetRacer Pro AI Kit](https://www.waveshare.com/wiki/JetRacer_Pro_AI_Kit)
(Jetson Nano 4 GB, IMX219 CSI camera, chassis, ESC, servo, battery pack). Use a ≥ 64 GB microSD card.

## 2. Flash the OS image

1. Download the Waveshare `jetracer_pro_ws.zip` image (Ubuntu 18.04, JetPack 4.5.1, with `jetracer`,
   `jetcam`, `torch2trt` and JupyterLab pre-installed) from the Waveshare wiki.
2. Flash it with [balenaEtcher](https://etcher.balena.io/) and let it verify.
3. First boot with monitor/keyboard, connect to Wi-Fi. The OLED shows the IP address, power mode
   (use `MAXN`), battery voltage/current/charge and CPU/GPU/RAM usage.

## 3. Remote access

Open `http://<jetracer_ip>:8888` in a Chromium-based browser (needed for the gamepad API).
Default JupyterLab password on the image: `jetson`. Change it if the car is on a shared network.

> In my setup, connecting from Windows did not work while Linux did; use a Linux laptop if you hit the same issue.

## 4. Fix the IMX219 colour cast (ISP override)

```bash
wget https://www.arducam.com/downloads/Jetson/Camera_overrides.tar.gz
tar zxvf Camera_overrides.tar.gz
sudo cp camera_overrides.isp /var/nvidia/nvcam/settings/
sudo chmod 664 /var/nvidia/nvcam/settings/camera_overrides.isp
sudo chown root:root /var/nvidia/nvcam/settings/camera_overrides.isp
```

Source: [Arducam, "Fix Red Tint with ISP Tuning"](https://docs.arducam.com/Nvidia-Jetson-Camera/Application-note/Fix-Red-Tint-with-ISP-Tuning/).

## 5. Run the notebooks in order

Copy `notebooks/` to `~/jetracer/notebooks/` on the car (they import `utils.py` and `xy_dataset.py`
from the upstream notebooks folder).

| Step | Notebook | Purpose |
|---|---|---|
| 1 | `01_basic_motion` | Check steering/throttle, set `throttle_gain` (0.2 used) |
| 2 | `02_teleoperation` | Pair the gamepad (find its index on html5gamepad.com), check drivetrain |
| 3 | `03_interactive_regression` | Collect and label data, train ResNet-18 (5–10 epochs for a first model), save `.pth` |
| 4 | `04_road_following_v1_baseline` | Convert to TensorRT FP16, first autonomous run |
| 5 | `07_road_following_v4_speed_modes` | Final version: set a starting throttle > 0.11, choose a speed mode |

**Safety:** keep throttle ≤ 0.15 for first runs, keep the RC transmitter in hand for manual override and
give the car space. See [known issues](known-issues.md) #1 about the emergency stop.

## 6. Run the hardware-independent part on a PC

```bash
pip install -e ".[dev]"
pytest -q                                  # unit + equivalence tests
python scripts/simulate_speed_scheduler.py # regenerates docs/images/speed_scheduler_response.png
```

# Third-party work and attribution

This repository mixes upstream example code with my own work. To be explicit about what is whose:

| Path | Origin | License |
|---|---|---|
| `notebooks/01_basic_motion.ipynb` | [NVIDIA-AI-IOT/jetracer](https://github.com/NVIDIA-AI-IOT/jetracer), as shipped in the Waveshare JetRacer Pro image; local calibration values only | MIT (upstream) |
| `notebooks/02_teleoperation.ipynb` | NVIDIA-AI-IOT/jetracer; gamepad axis mapping changed | MIT (upstream) |
| `notebooks/03_interactive_regression.ipynb` | NVIDIA-AI-IOT/jetracer; unchanged | MIT (upstream) |
| `notebooks/04_road_following_v1_baseline.ipynb` | NVIDIA-AI-IOT/jetracer; my model file and gain | MIT (upstream) |
| `notebooks/05–07_road_following_v2–v4_*.ipynb` | **My work**, built on the upstream baseline | MIT (this repo) |
| `src/`, `tests/`, `scripts/`, `docs/` | **My work** | MIT (this repo) |
| `docs/thesis/` | My bachelor's thesis (UPC, 2023) | © Albert Sagré Martínez, all rights reserved |
| `docs/images/` | My own photos and screenshots, taken from the thesis | © Albert Sagré Martínez |

Other credits:

- **JetRacer / JetCam / torch2trt**: NVIDIA-AI-IOT open-source projects used at runtime (not redistributed here).
- **Waveshare JetRacer Pro AI Kit**: hardware and the JetPack 4.5.1 SD-card image.
- The callback-based (`camera.observe`) control loop used from iteration 2 onwards was inspired by
  [haroonhublikar12/Self-driving-Car-Using-Machine-Learning-and-Neural-Networks](https://github.com/haroonhublikar12/Self-driving-Car-Using-Machine-Learning-and-Neural-Networks).
- Camera ISP override for the IMX219 sensor: [Arducam application note](https://docs.arducam.com/Nvidia-Jetson-Camera/Application-note/Fix-Red-Tint-with-ISP-Tuning/).

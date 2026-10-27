# Known issues: code review of the archived notebooks (2026)

The notebooks in `notebooks/` are kept **exactly as they ran on the car in 2022** so the thesis results stay
reproducible. Reviewing them again with a few years of vehicle validation experience, these are the
issues I would fix. Items marked ✅ are already addressed in `src/jetracer_control`.

| # | Severity | Where | Issue | Impact | Fix |
|---|---|---|---|---|---|
| 1 | **High (safety)** | V4 | The STOP button only sets `speed_slider.value = 0`; the throttle is actually set to 0 inside the camera callback. If the camera/perception loop stalls, STOP does not stop the car and the last throttle stays applied. The RC transmitter's manual override was the only independent fallback. | Emergency stop depends on the component most likely to fail. | STOP must write `car.throttle = 0` directly, and a watchdog should zero the throttle if no frame has been processed for > N ms. |
| 2 | Medium | V2–V4 | No perception-loop watchdog or frame-age check in general (see #1). | Stale commands on stalls. | Timestamp each frame; command zero throttle on timeout. |
| 3 | Medium | V3–V4 | Controller state (throttle) lives in a UI widget (`throttle_slider.value`). | Control logic coupled to the UI, impossible to unit test. | ✅ Extracted to a pure function `next_throttle(throttle, steering, mode)`, proven equivalent to V4 by tests. |
| 4 | Medium | 03 (upstream) | Training and "evaluate" use the same dataset; no held-out validation split, and the reported loss is training loss. Driving quality was judged qualitatively on the track. | Over-fitting is invisible; no objective comparison between iterations. | Hold-out split by recording session; log validation MSE in pixels; define a track KPI (interventions per lap, lap time). |
| 5 | Low | V2–V4 | Overlay uses `y = float(output[0])` (should be `output[1]`). | Displayed target point always on the image diagonal. **Steering is not affected** (only `x` is used). | ✅ `normalized_to_pixel(x, y, …)` takes both coordinates; regression test added. |
| 6 | Low | V2 | `steering_value_slider` is linked to `car.steering` *and* `car.steering = x` is written each frame: two writers on the same actuator command. | Ambiguous command path. | Removed in V3/V4 (link commented out); single writer. |
| 7 | Low | V3–V4 | Throttle ramp uses `+=` in floating point and stops one step past the band edge (e.g. 0.189 instead of 0.19). | Negligible numerically; makes bands slightly asymmetric. | Clamp to the band limits after each step (kept as-is in the refactor to preserve equivalence). |
| 8 | Low | 03 (upstream) | `except e: pass` raises `NameError` if an exception occurs during training. | Training errors are masked by a different error. | `except Exception as exc:` and report it. |
| 9 | Cosmetic | V2–V4 | Unused globals (`blocked_slider`, `robot`) and imports inherited from upstream examples. | Readability. | Remove. |

Trained weights (`*.pth`, TensorRT engines) and the collected datasets are not included: they are large and
hardware-specific (a TensorRT engine is tied to the device and JetPack version it was built on).

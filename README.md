# gpu-benchy 
![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![OpenGL](https://img.shields.io/badge/OpenGL-Legacy-orange)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)

A lightweight Python CLI tool that benchmarks GPU rendering performance across multiple resolutions using OpenGL and GLFW. Automatically detects available GPUs, runs a fixed-function triangle render test, and reports the highest resolution that maintains **≥30 FPS**.

## Features
- **Cross-platform GPU detection** (Linux, Windows, macOS)
- **Auto-installs dependencies** (`glfw`, `PyOpenGL`) on first run
- **Multi-resolution testing** from `128x128` up to `12288x6480`
- **3-second benchmark window** per resolution with real-time FPS tracking
- **Smart cutoff reporting** (finds max resolution at ≥30 FPS)
- **Headless-friendly** (benchmark windows are hidden during execution)

## Prerequisites
- Python 3.6+
- Working OpenGL drivers
- Internet connection (first time)
- A running display server (Linux/macOS) or desktop session (Windows)

## Usage
Simply run the script directly. Missing Python packages will be installed automatically:

```bash
python gpu-benchy.py
```

## Example Output
```
Found 2 GPU(s):
  [0] NVIDIA GeForce RTX 4070
  [1] Intel(R) UHD Graphics 630

=== Benchmarking GPU 0: NVIDIA GeForce RTX 4070 ===
128x128: 14520.33 FPS
240x240: 9841.12 FPS
...
7680x4320: 45.20 FPS
12288x6480: 22.15 FPS
[RESULT] NVIDIA GeForce RTX 4070 can render up to 7680x4320 at ≥30 FPS
```

## License  
[GNU Lesser General Public License v2.1](LICENSE) - Feel free to use and modify

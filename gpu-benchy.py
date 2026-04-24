#!/usr/bin/env python3
import sys
import subprocess
import importlib
import time
import platform
import os

# Required packages
REQUIRED = ["glfw", "PyOpenGL"]

def ensure_packages():
    for pkg in REQUIRED:
        try:
            importlib.import_module(pkg)
            print(f"[OK] {pkg} already installed")
        except ImportError:
            print(f"[INSTALL] Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

ensure_packages()

import glfw
import OpenGL.GL as gl

def get_all_gpus():
    """Cross-platform GPU detection using OS commands"""
    system = platform.system()
    gpus = []
    try:
        if system == "Linux":
            out = subprocess.check_output(["lspci"], text=True)
            for line in out.splitlines():
                if "VGA compatible controller" in line or "3D controller" in line:
                    gpus.append(line.split(":")[-1].strip())
        elif system == "Windows":
            out = subprocess.check_output(["wmic", "path", "win32_videocontroller", "get", "name"], text=True)
            gpus = [line.strip() for line in out.splitlines() if line.strip() and "Name" not in line]
        elif system == "Darwin":
            out = subprocess.check_output(["system_profiler", "SPDisplaysDataType"], text=True)
            for line in out.splitlines():
                if "Chipset Model:" in line:
                    gpus.append(line.split(":")[-1].strip())
    except Exception as e:
        print(f"[WARN] OS GPU detection failed: {e}")
    return gpus

resolutions = [
    (128,128), (240,240), (480,480), (720,720),
    (1920,1080), (3840,2160), (7680,4320), (12288,6480)
]

def render_scene():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glBegin(gl.GL_TRIANGLES)
    gl.glColor3f(1,0,0); gl.glVertex2f(-0.5,-0.5)
    gl.glColor3f(0,1,0); gl.glVertex2f(0.5,-0.5)
    gl.glColor3f(0,0,1); gl.glVertex2f(0.0,0.5)
    gl.glEnd()

def benchmark_gpu(gpu_name, gpu_index):
    print(f"\n=== Benchmarking GPU {gpu_index}: {gpu_name} ===")
    results = {}
    
    for w,h in resolutions:
        if not glfw.init():
            raise Exception("GLFW init failed")
            
        glfw.window_hint(glfw.RESIZABLE, False)
        # Hide window during benchmark for cleaner output
        glfw.window_hint(glfw.VISIBLE, False) 
        
        window = glfw.create_window(w, h, "Benchmark", None, None)
        if not window:
            print(f"[SKIP] Failed to create {w}x{h} context for {gpu_name}")
            continue
            
        glfw.make_context_current(window)
        
        frames = 0
        start = time.time()
        while time.time() - start < 3:  # run 3 seconds
            render_scene()
            glfw.swap_buffers(window)
            glfw.poll_events()
            frames += 1
            
        fps = frames / 3.0
        results[f"{w}x{h}"] = fps
        print(f"{w}x{h}: {fps:.2f} FPS")
        
        glfw.destroy_window(window)
        glfw.terminate()
        
    if results:
        cutoff = max([res for res, fps in results.items() if fps >= 30], 
                     key=lambda r: resolutions.index(tuple(map(int, r.split('x')))), 
                     default="None")
        print(f"[RESULT] {gpu_name} can render up to {cutoff} at ≥30 FPS")
    else:
        print("[RESULT] No valid frames captured.")

# Main
all_gpus = get_all_gpus()
if not all_gpus:
    print("[ERROR] No GPUs detected. Check drivers.")
    sys.exit(1)

print(f"\nFound {len(all_gpus)} GPU(s):")
for i, gpu in enumerate(all_gpus):
    print(f"  [{i}] {gpu}")

# Run benchmarks
for i, gpu in enumerate(all_gpus):
    benchmark_gpu(gpu, i)

# Internet Speed Monitor & Diagnostic Dashboard

A modern, real-time network throughput monitor and on-demand Ookla speed test dashboard built with **FastAPI**, **psutil**, **speedtest-cli**, and a custom dark-glassmorphic frontend.

---

## Motivation & Problem Statement

Whenever network connectivity on a laptop slows down or feels unstable, the usual workflow involves opening a browser, searching for "check net", navigating to an external speed test site, and waiting through ad-heavy pages just to diagnose latency and bandwidth.

This project solves that friction by providing:
1. **Continuous Real-Time Bandwidth Tracking**: Live per-second download and upload traffic tracking right in your browser or terminal using `psutil`.
2. **One-Click Speed Benchmark**: On-demand maximum bandwidth and latency testing against Ookla speed test servers using `speedtest-cli` running in a non-blocking background thread.

---

## Features

- **Live Bandwidth Telemetry**: Automatically measures byte delta every second across active network interfaces via `psutil.net_io_counters()`.
- **Asynchronous Ookla Benchmark**: Tests maximum download, upload, and latency over secure HTTPS without blocking or freezing the live monitor.
- **Glassmorphic Floating Widget**: A sleek, dark-mode status pill with pulsing live status beacon, tabular monospace metrics to prevent visual jitter, and smooth action transitions.
- **Dual Interface Modes**:
  - **Web Dashboard**: Interactive web GUI accessible on `http://127.0.0.1:8000`.
  - **CLI Monitor**: Terminal-only live throughput counter.
- **Clean Architecture**: Standardized Python package structure with clean separation between backend endpoints, static assets, and templates.

---

## Project Structure

```text
InternetSpeedProject/
│
├── src/
│   └── internetspeedproject/
│       ├── __init__.py           # Package exports & main() server launcher
│       ├── app.py                # FastAPI app (background monitor, routes, speed test worker)
│       ├── main.py               # Terminal monitor loop & CLI entry point
│       │
│       ├── static/
│       │   ├── style.css         # Glassmorphism styling, ambient mesh, and animations
│       │   └── script.js         # Polling logic, speed test lifecycle & error handling
│       │
│       └── templates/
│           └── index.html        # Clean HTML5 dashboard structure
│
├── .gitignore                    # Environment, IDE, and build cache rules
├── .python-version               # Python version pinning (>=3.12)
├── pyproject.toml                # Project metadata, dependencies, and CLI script definitions
├── README.md                     # Documentation & engineering notes
└── uv.lock                       # Deterministic dependency lockfile
```

---

## Tech Stack & Dependencies

- **Language**: Python >= 3.12
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Web Framework**: [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)
- **Templating**: [Jinja2](https://jinja.palletsprojects.com/)
- **System Metrics**: [psutil](https://github.com/giampaolo/psutil)
- **Bandwidth Benchmark**: [speedtest-cli](https://github.com/sivel/speedtest-cli)

---

## Getting Started

### 1. Installation

Clone the repository and sync the dependencies using `uv`:

```bash
uv sync
```

### 2. Running the Web Application

Launch the FastAPI web server using the registered package script:

```bash
uv run internetspeedproject
```

Or run directly with auto-reload for development:

```bash
uv run uvicorn internetspeedproject.app:app --reload
```

Then open your browser at **`http://127.0.0.1:8000`**.

### 3. Running the Terminal Monitor

To track live internet speeds directly in your console:

```bash
uv run python -m internetspeedproject.main
```

---

## API Endpoints

| Method | Endpoint            | Description                                               |
| ------ | ------------------- | --------------------------------------------------------- |
| `GET`  | `/`                 | Serves the primary web dashboard (`index.html`).          |
| `GET`  | `/live`             | Returns instantaneous download and upload speeds in Mbps. |
| `POST` | `/speedtest`        | Dispatches an asynchronous Ookla speed test in a worker.  |
| `GET`  | `/speedtest-result` | Returns the state and latest result of the speed test.    |

---

## Engineering Notes & Updates

### 16 NOV 2026 Updates
1. Basic problem: when internet connectivity fails, searching and navigating third-party sites introduces unnecessary friction.
2. Goal: create a lightweight, responsive dashboard that tracks useful real-time data and runs speed tests on demand.
3. Tested manual benchmarks with Ookla `speedtest-cli`.
4. Utilized `psutil` for real-time continuous bandwidth metrics and integrated `speedtest` for maximum bandwidth benchmarks.
5. Resolved race conditions in frontend polling and hardened backend socket timeouts and HTTPS probe configurations.

![CI](https://github.com/Hanningtone03/build-your-own-docker/actions/workflows/ci.yml/badge.svg)

# Build Your Own Docker

A container runtime in Python; process isolation, memory limits, image management, container lifecycle.

## How it works

Images are directory trees with isolated filesystems. Containers run commands inside those trees with their own hostname. On Linux, namespaces handle isolation and cgroups limit memory. State is tracked to disk.

## Project structure

```
src/
├── cli.py
├── container.py
├── namespace.py
├── cgroups.py
└── image.py
```

## Running locally

```bash
python -m src.cli run mycontainer "echo hello from container"
python -m src.cli ps
python -m src.cli images
```

## Tech

- Python 3
- `os`, `subprocess`, `ctypes` modules
- Linux namespaces and cgroups (graceful fallback on Windows)
- No external dependencies

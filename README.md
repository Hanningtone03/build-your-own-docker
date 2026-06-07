# Build Your Own Docker

A container runtime built from scratch in Python — supports process isolation, memory limits, image management, and container lifecycle.

## How it works

Docker uses two Linux kernel features under the hood — namespaces for isolation and cgroups for resource limits. This project implements both from scratch:

- Creates lightweight filesystem images with isolated directory trees
- Runs commands inside isolated containers with their own hostname
- Applies memory limits using cgroups on Linux
- Tracks container state and lifecycle to disk
- Provides a CLI interface mimicking Docker commands

## Project structure

```
src/
├── cli.py          
├── container.py    
├── namespace.py    
├── cgroups.py      
├── image.py        
└── __init__.py     
```

## Running locally

```bash
python -m src.cli run <name> <command>
python -m src.cli ps
python -m src.cli stop <container_id>
python -m src.cli images
python -m src.cli rmi <image_name>
```

## Example

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

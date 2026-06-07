import os
import json
import time
import threading
from .image import Image
from .namespace import run_isolated
from .cgroups import CGroup

CONTAINERS_FILE = "containers.json"

def load_containers():
    if os.path.exists(CONTAINERS_FILE):
        with open(CONTAINERS_FILE) as f:
            return json.load(f)
    return {}

def save_containers(containers):
    with open(CONTAINERS_FILE, "w") as f:
        json.dump(containers, f, indent=2)

def run(name, command, image_name="base", memory_mb=128):
    image = Image()
    rootfs = image.get(image_name)

    if not rootfs:
        print(f"Image '{image_name}' not found. Creating it...")
        rootfs = image.create(image_name)

    container_id = f"{name}-{int(time.time())}"
    containers = load_containers()
    containers[container_id] = {
        "id": container_id,
        "name": name,
        "image": image_name,
        "command": command,
        "status": "running",
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    save_containers(containers)
    print(f"Starting container {container_id}")
    print(f"Running: {command}")
    print("-" * 40)

    cgroup = CGroup(container_id, memory_limit_mb=memory_mb)
    cgroup.apply(os.getpid())

    exit_code = run_isolated(command, hostname=name, rootfs=None)

    print("-" * 40)
    containers = load_containers()
    if container_id in containers:
        containers[container_id]["status"] = "exited"
        containers[container_id]["exit_code"] = exit_code
        save_containers(containers)

    cgroup.cleanup()
    print(f"Container {container_id} exited with code {exit_code}")

def list_containers():
    containers = load_containers()
    if not containers:
        print("No containers.")
        return
    print(f"{'ID':<30} {'NAME':<15} {'IMAGE':<10} {'STATUS':<10} {'COMMAND'}")
    print("-" * 80)
    for c in containers.values():
        print(f"{c['id']:<30} {c['name']:<15} {c['image']:<10} {c['status']:<10} {c['command']}")

def stop(container_id):
    containers = load_containers()
    if container_id in containers:
        containers[container_id]["status"] = "stopped"
        save_containers(containers)
        print(f"Container {container_id} stopped.")
    else:
        print(f"Container {container_id} not found.")
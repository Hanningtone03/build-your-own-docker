import os
import platform

def is_linux():
    return platform.system() == "Linux"

class CGroup:
    def __init__(self, name, memory_limit_mb=128, cpu_shares=512):
        self.name = name
        self.memory_limit = memory_limit_mb * 1024 * 1024
        self.cpu_shares = cpu_shares
        self.cgroup_path = f"/sys/fs/cgroup/memory/{name}"

    def apply(self, pid):
        if not is_linux():
            print(f"cgroups: skipping on Windows (would limit memory to {self.memory_limit // (1024*1024)}MB)")
            return
        os.makedirs(self.cgroup_path, exist_ok=True)
        with open(f"{self.cgroup_path}/memory.limit_in_bytes", "w") as f:
            f.write(str(self.memory_limit))
        with open(f"{self.cgroup_path}/cgroup.procs", "w") as f:
            f.write(str(pid))
        print(f"cgroup applied: {self.memory_limit // (1024*1024)}MB limit for pid {pid}")

    def cleanup(self):
        if not is_linux():
            return
        procs_file = f"{self.cgroup_path}/cgroup.procs"
        if os.path.exists(procs_file):
            os.rmdir(self.cgroup_path)
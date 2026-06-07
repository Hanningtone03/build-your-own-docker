import os
import sys
import subprocess
import platform

def is_linux():
    return platform.system() == "Linux"

def run_isolated(command, hostname="container", rootfs=None):
    if is_linux():
        return _run_linux(command, hostname, rootfs)
    else:
        return _run_windows(command, hostname)

def _run_linux(command, hostname, rootfs):
    import ctypes
    CLONE_NEWUTS = 0x04000000
    CLONE_NEWPID = 0x20000000
    CLONE_NEWNS  = 0x00020000

    libc = ctypes.CDLL("libc.so.6", use_errno=True)
    flags = CLONE_NEWUTS | CLONE_NEWPID | CLONE_NEWNS
    if libc.unshare(flags) != 0:
        raise OSError("unshare failed")

    with open("/proc/sys/kernel/hostname", "w") as f:
        f.write(hostname)

    if rootfs:
        os.chroot(rootfs)
        os.chdir("/")

    result = subprocess.run(command, shell=True)
    return result.returncode

def _run_windows(command, hostname):
    env = os.environ.copy()
    env["CONTAINER_HOSTNAME"] = hostname
    result = subprocess.run(command, shell=True, env=env)
    return result.returncode
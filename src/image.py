import os
import shutil

class Image:
    def __init__(self, base_dir="images"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def create(self, name):
        path = os.path.join(self.base_dir, name)
        os.makedirs(path, exist_ok=True)
        for d in ["bin", "etc", "tmp", "var"]:
            os.makedirs(os.path.join(path, d), exist_ok=True)
        with open(os.path.join(path, "etc", "hostname"), "w") as f:
            f.write(name + "\n")
        print(f"Image '{name}' created at {path}")
        return path

    def get(self, name):
        path = os.path.join(self.base_dir, name)
        if os.path.exists(path):
            return path
        return None

    def list_images(self):
        return os.listdir(self.base_dir)

    def delete(self, name):
        path = os.path.join(self.base_dir, name)
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"Image '{name}' deleted.")
        else:
            print(f"Image '{name}' not found.")
import sys
from .container import run, list_containers, stop
from .image import Image

def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: python -m src.cli <command> [options]")
        print("Commands: run, ps, stop, images, rmi")
        return

    command = args[0]

    if command == "run":
        if len(args) < 3:
            print("Usage: python -m src.cli run <name> <command>")
            return
        name = args[1]
        cmd = " ".join(args[2:])
        run(name, cmd)

    elif command == "ps":
        list_containers()

    elif command == "stop":
        if len(args) < 2:
            print("Usage: python -m src.cli stop <container_id>")
            return
        stop(args[1])

    elif command == "images":
        image = Image()
        imgs = image.list_images()
        if not imgs:
            print("No images.")
        else:
            for img in imgs:
                print(img)

    elif command == "rmi":
        if len(args) < 2:
            print("Usage: python -m src.cli rmi <image_name>")
            return
        image = Image()
        image.delete(args[1])

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
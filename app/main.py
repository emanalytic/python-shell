import sys
import os


def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == "exit":
            break
        elif command.startswith("echo"):
            print(command[5:])
        elif command.startswith("type"):
            cmd = command[5:].strip()
            if cmd == "echo":
                print("echo is a shell builtin")
            elif cmd == "type":
                print("type is a shell builtin")
            elif cmd == "exit":
                print("exit is a shell builtin")
            else:
                found = False
                path_dirs = os.environ.get("PATH").split(":")
                for directory in path_dirs:
                    full_path = os.path.join(directory, cmd)
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        print(f"{cmd} is {full_path}")
                        found = True
                        break
                if not found:
                    print(f"{cmd}: not found")
        else:
            print(f"{command}: not found")



if __name__ == "__main__":
    main()

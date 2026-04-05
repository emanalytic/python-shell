import sys
import os

def resolve_cmd(cmd):
    path_dirs = os.environ.get("PATH").split(":")
    for directory in path_dirs:
        full_path = os.path.join(directory, cmd)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    return None



def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        try:
            command = input()
        except EOFError:
            break
        if command.strip() == "":
            continue
        if command == "exit":
            break

        ## builtin commands
        elif command.startswith("echo"):
            print(command[5:])
            continue

        elif command.startswith("type"):
            cmd = command[5:].strip()
            if cmd in ("echo", "type", "exit"):
                print(f"{cmd} is a shell builtin")
            else:
                full_path = resolve_cmd(cmd)
                if full_path:
                    print(f"{cmd} is {full_path}")
                else:
                    print(f"{cmd}: not found")
            continue
        # external command execution 
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]
        full_path = resolve_cmd(cmd)
        if full_path is None:
            print(f"{cmd}: not found")
            continue
        
        pid = os.fork()
        if pid == 0:
            os.execv(full_path, [cmd] + args)
        else:
            os.waitpid(pid, 0)


if __name__ == "__main__":
    main()

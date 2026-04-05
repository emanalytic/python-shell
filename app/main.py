from subprocess import check_call
import sys
import os
import subprocess
from pathlib import Path

def find_executable(cmd):
    path_dirs = os.environ.get("PATH", "").split(":")
    pathext = os.environ.get("PATHEXT", "").split(";")

    ## if cmd already has extension, try directly
    for directory in path_dirs:
        current_path = Path(directory) / cmd
        if current_path.is_file() and os.access(current_path, os.X_OK):
            return current_path

        # try Windows extensions
        for ext in pathext:
            candidate = Path(directory) / (cmd + ext.lower())
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return candidate

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
        

        argv = command.split()
        cmd = argv[0]
        args = argv[1:]

        if cmd == "exit":
            break


        ## builtin commands
        if cmd == "echo":
            print(command[5:])
            continue

        elif cmd == "type":
            if not args:
                print("type: missing argument")
                continue
            
            if args[0] in ("echo", "type", "exit"):
                print(f"{args[0]} is a shell builtin")
            else:
                full_path = find_executable(args[0])
                if full_path:
                    print(f"{args[0]} is {full_path}")
                else:
                    print(f"{args[0]}: not found")
            continue
        # external command execution 
        else:
            try:
                exec_path = find_executable(cmd)
                if exec_path:
                    subprocess.run([exec_path] + args, executable=str(exec_path))
                else:
                    print(f"{cmd}: not found")
            except Exception as e:
                print(e)

if __name__ == "__main__":
    main()

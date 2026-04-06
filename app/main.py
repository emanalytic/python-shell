import sys
import os
import subprocess
import shlex
from pathlib import Path


def find_executable(cmd):
    # use OS-correct path separator
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    pathext = os.environ.get("PATHEXT", "").split(os.pathsep) if os.name == "nt" else [""]

    for directory in path_dirs:
        base = Path(directory)

        # if cmd already contains extension or on Unix
        candidate = base / cmd
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate

        # try windows extension 
        for ext in pathext:
            candidate = base / (cmd + ext)
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return candidate

    return None


class Shell:
    def __init__(self):
        self.builtins = {
            "echo": self.echo,
            "type": self.type_cmd,
            "exit": self.exit_cmd,
            "pwd": self.pwd,
            "cd": self.cd
        }

    #  builtins  
    def echo(self, args):
        if ">" in args:
            index = args.index(">")
            with open(args[index+1], "w") as f:
                f.write(" ".join(args[:index]))
        else:
            print(" ".join(args))  

    def type_cmd(self, args):
        if not args:
            print("type: missing argument")
            return

        cmd = args[0]
        if cmd in self.builtins:
            print(f"{cmd} is a shell builtin")
            return

        path = find_executable(cmd)
        if path:
            print(f"{cmd} is {path}")
        else:
            print(f"{cmd}: not found")

    def exit_cmd(self, args):
        sys.exit(0)

    def pwd(self, args):
        print(os.getcwd())

    def cd(self, args):
        if not args:
            target = os.path.expanduser("~")
        else:
            target = args[0]
            if target == "~":
                target = os.path.expanduser("~")

        try:
            os.chdir(target)
        except FileNotFoundError:
            print(f"cd: {args[0]}: No such file or directory")
        except Exception as e:
            print(f"cd: error: {e}")

    def cat(self, args):
        for file in args:
            try:
                with open(file, "r") as f:
                    print(f.read())
            except FileNotFoundError:
                print(f"cat: {file}: No such file or directory")
            except Exception as e:
                print(f"cat: error: {e}")
        
        

    #execution 

    def execute(self, cmd, args):
        # builtin
        if cmd in self.builtins:
            return self.builtins[cmd](args)
        if cmd == "cat":
            return self.cat(args)

        # external
        exec_path = find_executable(cmd)
        if exec_path:
            try:
                subprocess.run([cmd] + args, executable=exec_path)
            except Exception as e:
                print(f"execution error: {e}")
        else:
            print(f"{cmd}: not found")

    #REPL

    def run(self):
        while True:
            try:
                command = input("$ ")
            except EOFError:
                break

            if not command.strip():
                continue

            try:
                argv = shlex.split(command)
            except ValueError as e:
                print(f"parse error: {e}")
                continue

            cmd = argv[0]
            args = argv[1:]

            self.execute(cmd, args)


def main():
    Shell().run()


if __name__ == "__main__":
    main()
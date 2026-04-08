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



class Command:
    def __init__(self, name, args, stdout=None):
        self.name = name
        self.args = args
        self.stdout = stdout


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
        target = args[0] if args else os.path.expanduser("~")
        if target == "~":
            target = os.path.expanduser("~")

        try:
            os.chdir(target)
        except FileNotFoundError:
            print(f"cd: {target}: No such file or directory")
        except Exception as e:
            print(f"cd: error: {e}")

    #execution

    def run_builtin(self, cmd):
        if cmd.stdout:
            try:
                with open(cmd.stdout, "w") as f:
                    old = sys.stdout
                    sys.stdout = f
                    try:
                        self.builtins[cmd.name](cmd.args)
                    finally:
                        sys.stdout = old
            except Exception as e:
                print(f"error: {e}")
        else:
            self.builtins[cmd.name](cmd.args)

    def run_external(self, cmd):
        exec_path = find_executable(cmd.name)
        if not exec_path:
            print(f"{cmd.name}: not found")
            return

        try:
            if cmd.stdout:
                with open(cmd.stdout, "w") as f:
                    subprocess.run([cmd.name] + cmd.args, executable=exec_path, stdout=f)
            else:
                subprocess.run([cmd.name] + cmd.args, executable=exec_path)
        except Exception as e:
            print(f"execution error: {e}")

    def execute(self, cmd):
        # builtin
        if cmd.name in self.builtins:
            self.run_builtin(cmd)
        else:
            self.run_external(cmd)

    #parsing

    def parse(self, argv):
        stdout = None

        # handle redirection
        for op in (">", "1>", "2>"):
            if op in argv:
                i = argv.index(op)

                if i + 1 >= len(argv):
                    print("syntax error: missing file")
                    return None
                if op == "2>":
                    stderr = argv[i + 1]
                    argv = argv[:i]
                    break

                stdout = argv[i + 1]
                argv = argv[:i]
                break

        if not argv:
            return None

        return Command(argv[0], argv[1:], stdout)

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

            cmd = self.parse(argv)
            if not cmd:
                continue

            self.execute(cmd)


def main():
    Shell().run()


if __name__ == "__main__":
    main()
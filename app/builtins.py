import sys
import os
from app.utils import find_executable

class Builtins:
    def __init__(self):
        self.commands = {
            "echo": self.echo,
            "type": self.type_cmd,
            "exit": self.exit_cmd,
            "pwd": self.pwd,
            "cd": self.cd
        }

    def echo(self, args):
        print(" ".join(args))

    def type_cmd(self, args):
        if not args:
            print("type: missing argument")
            return

        cmd = args[0]
        if cmd in self.commands:
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

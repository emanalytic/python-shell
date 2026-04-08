import sys
import subprocess
from app.utils import find_executable

class Executor:
    def __init__(self, builtins):
        self.builtins = builtins

    def execute(self, cmd):
        if cmd.name in self.builtins.commands:
            self.run_builtin(cmd)
        else:
            self.run_external(cmd)

    def run_builtin(self, cmd):
        if cmd.stdout:
            try:
                with open(cmd.stdout, "w") as f:
                    old = sys.stdout
                    sys.stdout = f
                    try:
                        self.builtins.commands[cmd.name](cmd.args)
                    finally:
                        sys.stdout = old
            except Exception as e:
                print(f"error: {e}")
        else:
            self.builtins.commands[cmd.name](cmd.args)

    def run_external(self, cmd):
        exec_path = find_executable(cmd.name)
        if not exec_path:
            print(f"{cmd.name}: not found")
            return

        stdout_f = None
        stderr_f = None

        try:
            if cmd.stdout:
                stdout_f = open(cmd.stdout, "w")

            if cmd.stderr:
                stderr_f = open(cmd.stderr, "w")

            subprocess.run(
                [cmd.name] + cmd.args,
                executable=exec_path,
                stdout=stdout_f,
                stderr=stderr_f
            )

        except Exception as e:
            print(f"execution error: {e}")

        finally:
            if stdout_f:
                stdout_f.close()
            if stderr_f:
                stderr_f.close()

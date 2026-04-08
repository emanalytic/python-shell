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
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        
        stdout_f = None
        stderr_f = None
        
        try:
            if cmd.stdout:
                stdout_f = open(cmd.stdout, cmd.stdout_mode)
                sys.stdout = stdout_f
            
            if cmd.stderr:
                stderr_f = open(cmd.stderr, cmd.stderr_mode)
                sys.stderr = stderr_f
                
            self.builtins.commands[cmd.name](cmd.args)
        except Exception as e:
            # Depending on how bad the error is, print to stderr if present
            print(f"error: {e}", file=sys.stderr)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            if stdout_f:
                stdout_f.close()
            if stderr_f:
                stderr_f.close()

    def run_external(self, cmd):
        exec_path = find_executable(cmd.name)
        if not exec_path:
            print(f"{cmd.name}: not found")
            return

        stdout_f = None
        stderr_f = None

        try:
            if cmd.stdout:
                stdout_f = open(cmd.stdout, cmd.stdout_mode)

            if cmd.stderr:
                stderr_f = open(cmd.stderr, cmd.stderr_mode)

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

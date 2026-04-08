import shlex
from app.builtins import Builtins
from app.parser import Parser
from app.executor import Executor

def main():
    builtins = Builtins()
    parser = Parser()
    executor = Executor(builtins)

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

        cmd = parser.parse(argv)
        if not cmd:
            continue

        executor.execute(cmd)

if __name__ == "__main__":
    main()
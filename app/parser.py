from app.models import Command

class Parser:
    @staticmethod
    def parse(argv):
        stdout = None
        stderr = None
        stdout_mode = "w"
        stderr_mode = "w"
        i = 0

        while i < len(argv):
            if argv[i] in (">", "1>", "2>", ">>", "1>>", "2>>"):
                if i + 1 >= len(argv):
                    print("syntax error: missing file")
                    return None

                op = argv[i]
                file = argv[i + 1]

                if op in (">", "1>"):
                    stdout = file
                    stdout_mode = "w"
                elif op in (">>", "1>>"):
                    stdout = file
                    stdout_mode = "a"
                elif op == "2>":
                    stderr = file
                    stderr_mode = "w"
                elif op == "2>>":
                    stderr = file
                    stderr_mode = "a"

                del argv[i:i+2]
                continue

            i += 1

        if not argv:
            return None

        return Command(argv[0], argv[1:], stdout, stderr, stdout_mode, stderr_mode)

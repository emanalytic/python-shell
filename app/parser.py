from app.models import Command

class Parser:
    @staticmethod
    def parse(argv):
        stdout = None
        stderr = None
        i = 0

        while i < len(argv):
            if argv[i] in (">", "1>", "2>"):
                if i + 1 >= len(argv):
                    print("syntax error: missing file")
                    return None

                if argv[i] in (">", "1>"):
                    stdout = argv[i + 1]
                else:
                    stderr = argv[i + 1]

                del argv[i:i+2]
                continue

            i += 1

        if not argv:
            return None

        return Command(argv[0], argv[1:], stdout, stderr)

class Command:
    def __init__(self, name, args, stdout=None, stderr=None, stdout_mode="w", stderr_mode="w"):
        self.name = name
        self.args = args
        self.stdout = stdout
        self.stderr = stderr
        self.stdout_mode = stdout_mode
        self.stderr_mode = stderr_mode

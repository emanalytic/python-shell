class Command:
    def __init__(self, name, args, stdout=None, stderr=None):
        self.name = name
        self.args = args
        self.stdout = stdout
        self.stderr = stderr

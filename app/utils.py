import os
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

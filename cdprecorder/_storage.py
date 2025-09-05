import os


DEFAULT_SOCKET_NAME = "erpeto.sock"


def get_runtime_dir() -> str:
    return os.getenv("XDG_RUNTIME_DIR")

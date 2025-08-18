import os
import random
import string
import subprocess

from . import logger


def run(
    sniffer_socket_address: str,
    host: str = "localhost",
    port: int = 8080,
    addon_script: str = "intercept_addon.py",
    binary: str = "mitmdump",
):
    proxy_name: str = "".join(random.choices(string.ascii_letters, k=32))
    module_dir = os.path.dirname(os.path.realpath(__file__))
    addon_path = os.path.join(module_dir, addon_script)
    cli_args = [
        "--mode",
        "regular",
        "--listen-host",
        host,
        "--listen-port",
        str(port),
        "-s",
        addon_path,
        "--set",
        f"socketaddress={sniffer_socket_address}",
        "--set",
        f"proxyname={proxy_name}",
    ]
    args = [binary] + cli_args

    logger.info("Running command: `%s`", " ".join(args))
    # TODO: stderr DEVNULL
    p = subprocess.Popen(args)  # , stdout=subprocess.DEVNULL)

    return p, host, port, proxy_name

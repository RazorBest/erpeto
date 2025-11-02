from __future__ import annotations

import asyncio
import sys

import cdprecorder
from cdprecorder import erpeto, recorder, skopo


async def on_fail(comparator, httpobj1, httpobj2):
    print(f"Comparator failed after {comparator.requests_passed} passes")
    print(f"First  httpobj: {httpobj1}")
    print(f"Second httpobj: {httpobj2}")
    raise Exception("Failure")


async def main() -> None:
    comparator = await skopo.create_mitmproxy_sniffer_comparator(on_fail)

    proxy_url1 = comparator.sniffer1.proxy_url
    proxy_url2 = comparator.sniffer2.proxy_url

    import requests

    def threaded_run1():
        proxies = {"http": proxy_url1, "https": proxy_url1}
        r = requests.get("https://google.com", proxies=proxies, verify=False)
        print("done")
        r = requests.get("https://google.com/test", proxies=proxies, verify=False)
        r = requests.get("https://google.com/test2", proxies=proxies, verify=False)

    def threaded_run2():
        proxies = {"http": proxy_url2, "https": proxy_url2}
        r = requests.get("https://google.com", proxies=proxies, verify=False)
        r = requests.get("https://google.com/test", proxies=proxies, verify=False)
        r = requests.get("https://google.com/test", proxies=proxies, verify=False)

    import threading

    thread1 = threading.Thread(target=threaded_run1, daemon=True)
    thread1.start()
    thread2 = threading.Thread(target=threaded_run2, daemon=True)
    thread2.start()

    await comparator.run()

    time.sleep(20)
    exit()

    """
    cdprecorder.enable_logger()
    cdprecorder.configure_root_logger(stream=sys.stdout)
    start_url = "https://github.com"
    options = recorder.RecorderOptions(start_url)
    await erpeto.run(options)
    """


if __name__ == "__main__":
    asyncio.run(main())

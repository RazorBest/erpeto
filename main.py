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
    sniffer_manager1 = skopo.MitmproxySnifferManager("1")
    sniffer_manager1.start_sniffer_on_thread()
    proxy1 = sniffer_manager1.start_proxy_instance(port=8082)

    sniffer_manager2 = skopo.MitmproxySnifferManager("2")
    sniffer_manager2.start_sniffer_on_thread()
    proxy2 = sniffer_manager2.start_proxy_instance(port=8083)

    print(f"Event loop: {asyncio.get_event_loop()}")
    comparator = skopo.SnifferComparator(
        on_fail, sniffer_manager1.sniffer, sniffer_manager2.sniffer, asyncio.get_event_loop()
    )

    await sniffer_manager1.wait_for_proxy_connection_with_sniffer()
    await sniffer_manager2.wait_for_proxy_connection_with_sniffer()

    print("Waited")

    proxy_url1 = f"http://{proxy1.host}:{proxy1.port}"
    proxy_url2 = f"http://{proxy2.host}:{proxy2.port}"

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

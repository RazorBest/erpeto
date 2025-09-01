import asyncio
import logging
import os
import subprocess
import time
import pathlib
import urllib.request

import pytest
from selenium import webdriver
from selenium_runners import run_csrf_form_submitsuccess

from cdprecorder import erpeto, skopo, recorder


VENV_HTTP_APPS = ".venv_http_apps"


class VenvAppRunner:
    def __init__(self, app_path: str):
        abs_app_path = pathlib.Path(__file__).parent.resolve() / app_path / "app.py"
        python_binary = os.path.join(VENV_HTTP_APPS, "bin/python")
        self.proc = subprocess.Popen(
            [python_binary, abs_app_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def wait_until_up(self, timeout: int = 3):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                ret = self.proc.poll()
                if ret is not None:
                    out, err = self.proc.communicate()
                    raise RuntimeError(f"Processed terminated. retcode: {ret}. stderr: {err}")
                urllib.request.urlopen("http://localhost:5000")
                break
            except urllib.error.URLError:
                time.sleep(0.1)
        else:
            self.proc.kill()
            out, err = self.proc.communicate()
            print(f"stdout: {out}")
            print(f"stderr: {err}")
            raise TimeoutError(f"Timeout exceeded: {timeout} seconds")

    def __del__(self):
        self.proc.terminate()


async def on_fail(comparator, httpobj1, httpobj2):
    logging.error(f"Comparator failed after {comparator.requests_passed} passes")
    logging.error(f"First  httpobj: {httpobj1}")
    logging.error(f"Second httpobj: {httpobj2}")
    raise Exception("Failure")


@pytest.mark.asyncio
async def test_csrf_form_run_csrf_from_submit_success():
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("pycdp").setLevel(logging.WARNING)
    logging.info("Starting web app")
    app = VenvAppRunner("http_apps/csrf_form")
    app.wait_until_up()
    logging.info("Web app started")

    comparator = await skopo.create_mitmproxy_sniffer_comparator(on_fail)

    proxy_url1 = comparator.sniffer1.proxy_url
    proxy_url2 = comparator.sniffer2.proxy_url

    # proxy_url = f"http://{proxy_info.host}:{proxy_info.port}"
    options = webdriver.ChromeOptions()
    cdp_port = 9222
    options.add_argument(f"--remote-debugging-port={cdp_port}")
    options.add_argument(f"--proxy-server={proxy_url1}")
    # options.add_argument("--headless=new")
    capabilities = options.to_capabilities()
    capabilities["acceptInsecureCerts"] = True
    print(options.to_capabilities())
    options.binary_location = "/usr/bin/google-chrome-stable"
    driver = webdriver.Chrome(options)
    logging.info("Instantiated web driver")

    recorder_options = recorder.RecorderOptions(
        "http://local:5000",
        cdp_host="localhost",
        cdp_port=cdp_port,
        collect_all=True,
    )

    sniffer1 = comparator.sniffer1

    async def pass_sniffer():
        print("pass sniffer")
        msg = None
        try:
            while True:
                msg = await sniffer1.get_message()

                logging.debug("Msg: %s", msg)
                logging.debug("Session: %s", msg.session)
                await sniffer1.to_session(msg.session).send_command(skopo.SniffCommand.NOP)
        except asyncio.CancelledError:
            if msg is not None:
                await sniffer1.to_session(msg.session).send_command(skopo.SniffCommand.NOP)
            pass
        except:
            logging.exception("Pass sniffer ended with exception")

    pass_task = asyncio.create_task(pass_sniffer())
    rec = await recorder.init_recorder(recorder_options)
    await asyncio.sleep(2)
    pass_task.cancel()
    try:
        pass_task.result()
    except (asyncio.CancelledError, asyncio.InvalidStateError):
        pass
    except:
        logging.exception("pass_task ended with exception")

    try:
        t1 = asyncio.create_task(asyncio.to_thread(run_csrf_form_submitsuccess, driver))
        t2 = asyncio.create_task(recorder.collect_communications(rec, 30))
        t3 = asyncio.create_task(pass_sniffer())
        done, pending = await asyncio.wait([t1, t2, t3], return_when=asyncio.FIRST_COMPLETED)

        if t2 in done:
            logging.info("Task2 is done")
            logging.info("Result: %s", t2.result())

        if t3 in done:
            logging.info("Task3 is done")

        if t1 in pending:
            raise Exception("Recorder stopped before selenium test")

        if t3 in pending:
            t3.cancel()

        if t2 in pending:
            rec.listener.cancel()
        communications = await t2
    finally:
        await rec.close()

    driver.quit()

    logging.info("Recorded communications")

    actions = erpeto.parse_communications_into_actions(communications)
    erpeto.make_action_ids_consecutive_from_list(actions)
    # actions = await erpeto.run_recorder(recorder_options)
    erpeto.run_analyse(actions)

    # TODO: probably, a sniffer that's not linked to a comparator should not block
    # comparator = skopo.SnifferComparator(on_fail, sniffer_manager1.sniffer, sniffer_manager2.sniffer)

    driver = webdriver.Chrome(options)

    t1 = asyncio.create_task(asyncio.to_thread(run_csrf_form_submitsuccess, driver))
    t2 = asyncio.create_task(asyncio.to_thread(erpeto.run_replicate, actions, [proxy_url2]))
    t3 = asyncio.create_task(comparator.run())

    pair = asyncio.create_task(asyncio.wait([t1, t2], return_when=asyncio.ALL_COMPLETED))
    done, pending = await asyncio.wait([pair, t3], return_when=asyncio.FIRST_COMPLETED)

    logging.debug("Pending state: %s, %s", pair.done(), t3.done())

    t3.cancel()
    if t3 in done:
        assert t3.result() is True
    # comparator.stop()
    return

    # TODO: this probably can't cancel t1 and t2
    for pair in pending:
        pair.cancel()

    if t3 in done:
        res = t3.result()

        assert res is True

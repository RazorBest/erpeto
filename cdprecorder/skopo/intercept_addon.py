from __future__ import annotations

import logging
import pickle
import socket
import sys
from urllib.parse import urlunparse
from typing import Optional, TYPE_CHECKING

from mitmproxy import ctx, http

import common_data
from common_data import SniffConnection, RequestData, ResponseData

# :'(
# Used by pickle to load RequestData and ResponseData
sys.modules["cdprecorder"] = common_data
sys.modules["cdprecorder.common_data"] = common_data
sys.modules["cdprecorder.skopo.common_data"] = common_data

import requests


if TYPE_CHECKING:
    from mitmproxy import http


class WrapperFormatter(logging.Formatter):
    def __init__(self, formatter: loggingFormatter):
        self.formatter = formatter

    def format(self, record: logging.LogRecord):
        msg = self.formatter.format(record)

        msg_prefix = ""
        if hasattr(record, "prefix"):
            msg_prefix = f"[{record.prefix}]"

        return f"{msg_prefix}{msg}"

    def formatTime(self, *args, **kwargs):
        return self.formatter.formatTime(*args, **kwargs)

    def formatException(self, *args, **kwargs):
        return self.formatter.formatException(*args, **kwargs)

    def formatStack(self, *args, **kwargs):
        return self.formatter.formatStack(*args, **kwargs)


class PrefixFilter(logging.Filter):
    def __init__(self, prefix: Optional[str] = None):
        self.prefix = prefix

    def filter(self, record: logging.LogRecord) -> bool:
        if self.prefix is not None:
            record.prefix = self.prefix
        return True


class TheSpy:
    def __init__(self):
        self.data_sender = None
        self.flows = set()

        logging.info("PPpp", extra={"client": "haubau"})

        self.log_filter = PrefixFilter()
        handler = logging.getLogger().handlers[0]
        handler.addFilter(self.log_filter)
        wrapper_formatter = WrapperFormatter(handler.formatter)
        handler.setFormatter(wrapper_formatter)

    def load(self, loader):
        url = f"{ctx.options.listen_host}:{ctx.options.listen_port}"
        self.log_filter.prefix = url

        loader.add_option(
            name="socketaddress",
            # Wow, they really used typing at runtime
            typespec=Optional[str],
            default=None,
            help="Socket address to send request/response pickled data",
        )
        loader.add_option(
            name="proxyname",
            typespec=str,
            default="thespy",
            help="Name used to distinguish different mitmdump instances",
        )

    def start_connection(self, socketaddress: str):
        if self.data_sender is not None:
            self.data_sender.close()
        logging.info("Connecting to %s", socketaddress)
        self.data_sender = SniffConnection(socketaddress)
        assert isinstance(self.proxyname, str)
        self.data_sender.send(self.proxyname)

    def running(self):
        if ctx.options.socketaddress is not None:
            self.start_connection(ctx.options.socketaddress)

    def configure(self, updated: set[str]):
        self.proxyname = ctx.options.proxyname
        logging.info("Set proxyname=%s", self.proxyname)
        if ctx.options.socketaddress is not None:
            self.start_connection(ctx.options.socketaddress)

    def request(self, flow: http.HTTPFlow):
        self.flows.add(id(flow))
        logging.info("Intercepted request")
        mitmreq = flow.request
        # TODO: handle mitmreq.authority
        url = urlunparse(
            (
                mitmreq.scheme,
                f"{mitmreq.host}:{mitmreq.port}",
                # Can this ever be bytes??
                mitmreq.path,
                "",
                "",
                "",
            )
        )

        req = RequestData(
            http_version=mitmreq.http_version,
            method=mitmreq.method,
            url=url,
            headers=list(mitmreq.headers.items(multi=True)),
            raw_content=mitmreq.raw_content,
            trailers=list(mitmreq.trailers.items(multi=True) if mitmreq.trailers else []),
            object_id=id(flow),
        )

        self.data_sender.send(req)

        logging.info("Sent request")
        status = self.data_sender.read_str()

        if status == "REPLACE_RESPONSE":
            r = self.data_sender.read_response_data()

            logging.info("Headers: %s", r.headers)
            headers_bytes = []
            for key, value in r.headers:
                headers_bytes.append((key.encode(), value.encode()))
            resp = http.Response.make(
                status_code=r.status_code,
                content=r.raw_content,
                headers=headers_bytes,
            )
            resp.http_version = r.http_version
            resp.reason = r.reason
            resp.trailers = http.Headers(r.trailers)

            flow.response = resp
        elif status == "REPLACE_REQUEST":
            r = self.data_sender.read_request_data()

            req = http.Request.make(method=r.method, url=r.url, content=r.raw_content, headers=http.Headers(r.headers))
            req.http_version = (r.http_version,)
            req.reason = (r.reason,)
            req.trailers = (http.Headers(r.trailers),)

            flow.request = req

        elif status != "OK":
            raise Exception(f"Unknown status: {status}")

        logging.info("OK Intercepted request")

    def response(self, flow: http.HTTPFlow):
        logging.info("Intercepted response")
        if id(flow) not in self.flows:
            logging.error("Got response before existing request")
        else:
            self.flows.remove(id(flow))

        try:
            mitmres = flow.response
            logging.info("Response headers: %s", mitmres.headers)
            res = ResponseData(
                http_version=mitmres.http_version,
                status_code=mitmres.status_code,
                reason=mitmres.reason,
                headers=list(mitmres.headers.items(multi=True)),
                raw_content=mitmres.raw_content,
                trailers=list(mitmres.trailers.items(multi=True) if mitmres.trailers else []),
                object_id=id(flow),
            )

            logging.info("Constructed ResponseData")

            self.data_sender.send(res)
            logging.info("Sent response")

            status = self.data_sender.read_str()
            logging.info("Got status in response")

            if status == "REPLACE_RESPONSE":
                r = self.data_sender.read_response_data()

                resp = http.Response.make(
                    status_code=r.status_code,
                    content=r.raw_content,
                    headers=http.Headers(r.headers),
                )
                resp.http_version = (r.http_version,)
                resp.reason = (r.reason,)
                resp.trailers = (http.Headers(r.trailers),)

                flow.response = resp
            elif status != "OK":
                raise Exception(f"Unknown status: {status}")

            logging.info("OK Intercepted response")
        except Exception as exc:
            logging.info("Addon Exception: %s", exc)
            raise


addons = [TheSpy()]

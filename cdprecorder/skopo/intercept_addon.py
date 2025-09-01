from __future__ import annotations

import logging
import socket
import sys
from urllib.parse import urlunparse
from typing import Optional, TYPE_CHECKING

from mitmproxy import ctx, http, tcp

from sniff_protocol import (
    RequestData,
    ResponseData,
    SniffCommand,
    SnifferMetadata,
    SnifferProxyClient,
    read_sock_datagram,
    to_sock_datagram,
)


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


class MitmproxySnifferProxyClient(SnifferProxyClient):
    def __init__(self, sockaddr: str):
        super().__init__()
        self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.client.connect(sockaddr)

    def _get_data(self) -> bytes:
        data = read_sock_datagram(self.client)
        return data

    def _send_data(self, data: bytes):
        datagram = to_sock_datagram(data)
        self.client.sendall(datagram)

    def close(self):
        if self.client is not None:
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
            self.client = None

    def __del__(self):
        self.close()


class TheSpy:
    def __init__(self):
        self.client = None
        self.flows = set()

        self.log_filter = PrefixFilter()
        handler = logging.getLogger().handlers[0]
        handler.addFilter(self.log_filter)
        wrapper_formatter = WrapperFormatter(handler.formatter)
        handler.setFormatter(wrapper_formatter)

        self.objid_to_session = {}

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
        if self.client is not None:
            self.client.close()
        logging.info("Connecting to %s", socketaddress)
        self.client = MitmproxySnifferProxyClient(socketaddress)
        assert isinstance(self.proxyname, str)

    def running(self):
        if ctx.options.socketaddress is not None:
            self.start_connection(ctx.options.socketaddress)

    def configure(self, updated: set[str]):
        self.proxyname = ctx.options.proxyname
        logging.info("Set proxyname=%s", self.proxyname)
        if ctx.options.socketaddress is not None:
            self.start_connection(ctx.options.socketaddress)

    def get_session_for_object_id(self, object_id: int):
        if object_id not in self.objid_to_session:
            session = self.client.new_session()
            self.objid_to_session[object_id] = session

        return self.objid_to_session[object_id]

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
            http_version=mitmreq.http_version.encode(),
            method=mitmreq.method.encode(),
            url=url.encode(),
            headers=bytes(mitmreq.headers),
            content=mitmreq.raw_content,
            trailers=bytes(mitmreq.trailers) if mitmreq.trailers else b"",
            meta=SnifferMetadata(object_id=id(flow), timestamp=0, proxyname=self.proxyname),
        )

        session = self.get_session_for_object_id(id(flow))
        session.send_request_data(req)

        logging.info("Sent request")
        command = session.get_command()

        if command.command == SniffCommand.REPLACE:
            if command.response is not None:
                r = command.response

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
            if command.request is not None:
                r = command.request

                req = http.Request.make(
                    method=r.method, url=r.url, content=r.raw_content, headers=http.Headers(r.headers)
                )
                req.http_version = (r.http_version,)
                req.reason = (r.reason,)
                req.trailers = (http.Headers(r.trailers),)

                flow.request = req
        elif command.command != SniffCommand.NOP:
            raise Exception(f"Unknown command: {command.command}")

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
                http_version=mitmres.http_version.encode(),
                status_code=mitmres.status_code,
                reason=mitmres.reason.encode(),
                headers=bytes(mitmres.headers),
                content=mitmres.raw_content,
                trailers=bytes(mitmres.trailers) if mitmres.trailers else b"",
                meta=SnifferMetadata(object_id=id(flow), timestamp=0, proxyname=self.proxyname),
            )

            logging.info("Constructed ResponseData")

            session = self.get_session_for_object_id(id(flow))
            session.send_response_data(res)
            logging.info("Sent response")

            command = session.get_command()
            logging.info("Got command in response")

            if command.command == SniffCommand.REPLACE:
                if command.response is not None:
                    r = command.response

                    resp = http.Response.make(
                        status_code=r.status_code,
                        content=r.raw_content,
                        headers=http.Headers(r.headers),
                    )
                    resp.http_version = (r.http_version,)
                    resp.reason = (r.reason,)
                    resp.trailers = (http.Headers(r.trailers),)

                    flow.response = resp
            elif command.command != SniffCommand.NOP:
                raise Exception(f"Unknown command: {sommand.command}")

            logging.info("OK Intercepted response")
        except Exception as exc:
            logging.info("Addon Exception: %s", exc)
            raise

    def server_connect(self, data):
        logging.info("About to connect to: %s. %s", data.server.address, str(data.server))
        if data.server.address[0] == "local":
            data.server.address = ("127.0.0.1", data.server.address[1])


def tcp_message(flow: tcp.TCPFlow):
    from mitmproxy.utils import strutils

    message = flow.messages[-1]
    # message.content = message.content.replace(b"foo", b"bar")

    logging.info(
        f"tcp_message[from_client={message.from_client}), content={strutils.bytes_to_escaped_str(message.content)}]"
    )


addons = [TheSpy()]

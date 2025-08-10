"""
This module contains type variables used by mypy. It's not used at runtime.
"""

from typing import Optional, Protocol, Union

import requests
from pycdp import cdp
from pycdp.cdp.util import T_JSON_DICT

from .action import HttpAction


class CdpEvent(Protocol):
    def to_json(self) -> T_JSON_DICT: ...


class HttpTarget(Protocol):
    def apply(
        self, action: HttpAction, prev_actions: list[Optional[HttpAction]]
    ) -> None: ...


RequestInfo = Union[
    # cdp.network.RequestWillBeSent,
    cdp.network.Request,
    cdp.network.RequestWillBeSentExtraInfo,
    # cdp.network.ResponseReceived,
    cdp.network.Response,
    cdp.network.ResponseReceivedExtraInfo,
    "HttpAction",
    requests.models.Response,
]

from __future__ import annotations

import cheap_repr
import dataclasses
import logging
from typing import TYPE_CHECKING

from pycdp import cdp

if TYPE_CHECKING:
    from typing import Any, Callable, Type, TypeVar, ParamSpec

    from _typeshed import DataclassInstance

    T = TypeVar("T")
    U = TypeVar("U")
    P = ParamSpec("P")
    P2 = ParamSpec("P2")

    from typing import TypeAlias


__all__ = ["logger", "configure_root_logger", "enable_loggger"]

logger = logging.getLogger(__name__)


DEFAULT_LOG_PATH = ".erpeto_logs.txt"

cheap_repr.cheap_repr.suppression_threshold = 500000
cheap_repr.cheap_repr.max_level = 10


class PreparedReprStr:
    __slots__ = "s"

    def __init__(self, s: str):
        self.s = s

    def __repr__(self) -> str:
        """Returns the actual string, instead of the quoted string."""
        return self.s


def register_custom_repr(
    cls: Type[DataclassInstance],
    full_names: list[str],
    first_names: list[str],
    maxparts: int = 4,
) -> None:
    full_names = list(full_names)
    first_names = list(first_names)
    custom_names = full_names + first_names

    @cheap_repr.register_repr(cls)
    @cheap_repr.maxparts(maxparts)
    def custom_repr(obj: DataclassInstance, helper: cheap_repr.ReprHelper) -> str:
        clsname = obj.__class__.__name__

        full_fields = [f"{name}={repr(getattr(obj, name))}" for name in full_names]
        first_fields = [f"{name}={cheap_repr.cheap_repr(getattr(obj, name))}" for name in first_names]
        custom_fields = full_fields + first_fields

        other_fields = [
            PreparedReprStr(f"{field.name}={cheap_repr.cheap_repr(getattr(obj, field.name))}")
            for field in dataclasses.fields(obj)
            if field.name not in custom_names
        ]

        generic_elements_str = helper.repr_iterable(other_fields, "", "")
        return f"{clsname}(" + ", ".join(custom_fields + [generic_elements_str]) + ")"


cheap_repr.register_repr(cdp.network.LoadingFinished)(cheap_repr.normal_repr)

register_custom_repr(cdp.network.Request, ["method"], ["url"], maxparts=3)
register_custom_repr(cdp.network.RequestWillBeSent, [], ["request_id", "request"], maxparts=4)
register_custom_repr(cdp.network.RequestWillBeSentExtraInfo, [], ["request_id"], maxparts=3)
register_custom_repr(cdp.network.Response, [], ["url"], maxparts=3)
register_custom_repr(cdp.network.ResponseReceived, [], ["request_id", "response"], maxparts=3)
register_custom_repr(cdp.network.ResponseReceivedExtraInfo, [], ["request_id"], maxparts=3)


# cheap_repr.register_repr(cdp.network.ResponseReceived)(cheap_repr.normal_repr)
# cheap_repr.register_repr(cdp.network.ResponseReceivedExtraInfo)(cheap_repr.normal_repr)


@cheap_repr.register_repr(str)
@cheap_repr.maxparts(50)
def custom_repr_str(obj: str, helper: cheap_repr.ReprHelper) -> str:
    return helper.truncate(obj)


# for fixing the kwargs problem, check https://github.com/python/mypy/issues/10574
# or explicitly specify the signature
def configure_root_logger(**kwargs) -> None:  # type: ignore[no-untyped-def]
    kwargs.setdefault("level", logging.DEBUG)
    kwargs.setdefault("encoding", "utf-8")
    kwargs.setdefault("format", "%(asctime)s %(levelno)s %(filename)s:%(lineno)s: %(message)s")
    # From the documentation of logging.basicConfig about the `stream` argument:
    # > Note that this argument is incompatible with filename - if both are
    # present, a ValueError is raised.
    if "stream" not in kwargs:
        kwargs.setdefault("filename", DEFAULT_LOG_PATH)

    logging.basicConfig(**kwargs)

    logging.getLogger("twisted").setLevel(logging.WARNING)
    logging.getLogger("pycdp").setLevel(logging.WARNING)


def enable_logger() -> None:
    logger.setLevel(logging.DEBUG)

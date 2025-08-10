import cheap_repr
import dataclasses
import logging

from pycdp import cdp

__all__ = ["logger", "configure_root_logger", "enable_loggger"]

logger = logging.getLogger(__name__)


DEFAULT_LOG_PATH = ".erpeto_logs.txt"

cheap_repr.cheap_repr.suppression_threshold = 500000
cheap_repr.cheap_repr.max_level = 10


class PreparedReprStr:
    __slots__ = "s"

    def __init__(self, s: str):
        self.s = s

    def __repr__(self):
        """Returns the actual string, instead of the quoted string."""
        return self.s


def register_custom_repr(cls, full_names, first_names, maxparts=4):
    full_names = list(full_names)
    first_names = list(first_names)
    custom_names = full_names + first_names

    @cheap_repr.register_repr(cls)
    @cheap_repr.maxparts(maxparts)
    def custom_repr(obj: cls, helper):
        clsname = obj.__class__.__name__

        full_fields = [f"{name}={repr(getattr(obj, name))}" for name in full_names]
        first_fields = [
            f"{name}={cheap_repr.cheap_repr(getattr(obj, name))}"
            for name in first_names
        ]
        custom_fields = full_fields + first_fields

        other_fields = [
            PreparedReprStr(
                f"{field.name}={cheap_repr.cheap_repr(getattr(obj, field.name))}"
            )
            for field in dataclasses.fields(obj)
            if field.name not in custom_names
        ]

        generic_elements_str = helper.repr_iterable(other_fields, "", "")
        return f"{clsname}(" + ", ".join(custom_fields + [generic_elements_str]) + ")"


cheap_repr.register_repr(cdp.network.LoadingFinished)(cheap_repr.normal_repr)

register_custom_repr(cdp.network.Request, ["method"], ["url"], maxparts=3)
register_custom_repr(
    cdp.network.RequestWillBeSent, [], ["request_id", "request"], maxparts=4
)
register_custom_repr(
    cdp.network.RequestWillBeSentExtraInfo, [], ["request_id"], maxparts=3
)
register_custom_repr(cdp.network.Response, [], ["url"], maxparts=3)
register_custom_repr(
    cdp.network.ResponseReceived, [], ["request_id", "response"], maxparts=3
)
register_custom_repr(
    cdp.network.ResponseReceivedExtraInfo, [], ["request_id"], maxparts=3
)


@cheap_repr.register_repr(dataclasses.Field)
def custom_repr_dataclass(obj: dataclasses.Field, helper):
    return f"{obj.name}={cheap_repr.cheap_repr(obj.value)}"


# cheap_repr.register_repr(cdp.network.ResponseReceived)(cheap_repr.normal_repr)
# cheap_repr.register_repr(cdp.network.ResponseReceivedExtraInfo)(cheap_repr.normal_repr)


@cheap_repr.register_repr(str)
@cheap_repr.maxparts(50)
def custom_repr_str(obj, helper):
    return helper.truncate(obj)


def configure_root_logger(**kwargs) -> None:
    kwargs.setdefault("level", logging.DEBUG)
    kwargs.setdefault("encoding", "utf-8")
    kwargs.setdefault(
        "format", "%(asctime)s %(levelno)s %(filename)s:%(lineno)s: %(message)s"
    )
    # From the documentation of logging.basicConfig about the `stream` argument:
    # > Note that this argument is incompatible with filename - if both are
    # present, a ValueError is raised.
    if "stream" not in kwargs:
        kwargs.setdefault("filename", DEFAULT_LOG_PATH)

    logging.basicConfig(**kwargs)

    logging.getLogger("twisted").setLevel(logging.WARNING)
    logging.getLogger("pycdp").setLevel(logging.WARNING)


def enable_logger():
    logger.setLevel(logging.DEBUG)

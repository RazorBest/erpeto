import enum
import typing
from . import dom as dom, runtime as runtime
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class DOMBreakpointType(enum.Enum):
    SUBTREE_MODIFIED: str
    ATTRIBUTE_MODIFIED: str
    NODE_REMOVED: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> DOMBreakpointType: ...

class CSPViolationType(enum.Enum):
    TRUSTEDTYPE_SINK_VIOLATION: str
    TRUSTEDTYPE_POLICY_VIOLATION: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CSPViolationType: ...

@dataclass
class EventListener:
    type_: str
    use_capture: bool
    passive: bool
    once: bool
    script_id: runtime.ScriptId
    line_number: int
    column_number: int
    handler: typing.Optional[runtime.RemoteObject] = ...
    original_handler: typing.Optional[runtime.RemoteObject] = ...
    backend_node_id: typing.Optional[dom.BackendNodeId] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> EventListener: ...
    def __init__(self, type_, use_capture, passive, once, script_id, line_number, column_number, handler, original_handler, backend_node_id) -> None: ...

def get_event_listeners(object_id: runtime.RemoteObjectId, depth: typing.Optional[int] = None, pierce: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[EventListener]]: ...
def remove_dom_breakpoint(node_id: dom.NodeId, type_: DOMBreakpointType) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def remove_event_listener_breakpoint(event_name: str, target_name: typing.Optional[str] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def remove_instrumentation_breakpoint(event_name: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def remove_xhr_breakpoint(url: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_break_on_csp_violation(violation_types: typing.List[CSPViolationType]) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_dom_breakpoint(node_id: dom.NodeId, type_: DOMBreakpointType) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_event_listener_breakpoint(event_name: str, target_name: typing.Optional[str] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_instrumentation_breakpoint(event_name: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_xhr_breakpoint(url: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

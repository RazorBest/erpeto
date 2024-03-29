import enum
import typing
from . import dom as dom, page as page, runtime as runtime
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class AXNodeId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AXNodeId: ...

class AXValueType(enum.Enum):
    BOOLEAN: str
    TRISTATE: str
    BOOLEAN_OR_UNDEFINED: str
    IDREF: str
    IDREF_LIST: str
    INTEGER: str
    NODE: str
    NODE_LIST: str
    NUMBER: str
    STRING: str
    COMPUTED_STRING: str
    TOKEN: str
    TOKEN_LIST: str
    DOM_RELATION: str
    ROLE: str
    INTERNAL_ROLE: str
    VALUE_UNDEFINED: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AXValueType: ...

class AXValueSourceType(enum.Enum):
    ATTRIBUTE: str
    IMPLICIT: str
    STYLE: str
    CONTENTS: str
    PLACEHOLDER: str
    RELATED_ELEMENT: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AXValueSourceType: ...

class AXValueNativeSourceType(enum.Enum):
    DESCRIPTION: str
    FIGCAPTION: str
    LABEL: str
    LABELFOR: str
    LABELWRAPPED: str
    LEGEND: str
    RUBYANNOTATION: str
    TABLECAPTION: str
    TITLE: str
    OTHER: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AXValueNativeSourceType: ...

@dataclass
class AXValueSource:
    type_: AXValueSourceType
    value: typing.Optional[AXValue] = ...
    attribute: typing.Optional[str] = ...
    attribute_value: typing.Optional[AXValue] = ...
    superseded: typing.Optional[bool] = ...
    native_source: typing.Optional[AXValueNativeSourceType] = ...
    native_source_value: typing.Optional[AXValue] = ...
    invalid: typing.Optional[bool] = ...
    invalid_reason: typing.Optional[str] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AXValueSource: ...
    def __init__(self, type_, value, attribute, attribute_value, superseded, native_source, native_source_value, invalid, invalid_reason) -> None: ...

@dataclass
class AXRelatedNode:
    backend_dom_node_id: dom.BackendNodeId
    idref: typing.Optional[str] = ...
    text: typing.Optional[str] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AXRelatedNode: ...
    def __init__(self, backend_dom_node_id, idref, text) -> None: ...

@dataclass
class AXProperty:
    name: AXPropertyName
    value: AXValue
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AXProperty: ...
    def __init__(self, name, value) -> None: ...

@dataclass
class AXValue:
    type_: AXValueType
    value: typing.Optional[typing.Any] = ...
    related_nodes: typing.Optional[typing.List[AXRelatedNode]] = ...
    sources: typing.Optional[typing.List[AXValueSource]] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AXValue: ...
    def __init__(self, type_, value, related_nodes, sources) -> None: ...

class AXPropertyName(enum.Enum):
    BUSY: str
    DISABLED: str
    EDITABLE: str
    FOCUSABLE: str
    FOCUSED: str
    HIDDEN: str
    HIDDEN_ROOT: str
    INVALID: str
    KEYSHORTCUTS: str
    SETTABLE: str
    ROLEDESCRIPTION: str
    LIVE: str
    ATOMIC: str
    RELEVANT: str
    ROOT: str
    AUTOCOMPLETE: str
    HAS_POPUP: str
    LEVEL: str
    MULTISELECTABLE: str
    ORIENTATION: str
    MULTILINE: str
    READONLY: str
    REQUIRED: str
    VALUEMIN: str
    VALUEMAX: str
    VALUETEXT: str
    CHECKED: str
    EXPANDED: str
    MODAL: str
    PRESSED: str
    SELECTED: str
    ACTIVEDESCENDANT: str
    CONTROLS: str
    DESCRIBEDBY: str
    DETAILS: str
    ERRORMESSAGE: str
    FLOWTO: str
    LABELLEDBY: str
    OWNS: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AXPropertyName: ...

@dataclass
class AXNode:
    node_id: AXNodeId
    ignored: bool
    ignored_reasons: typing.Optional[typing.List[AXProperty]] = ...
    role: typing.Optional[AXValue] = ...
    chrome_role: typing.Optional[AXValue] = ...
    name: typing.Optional[AXValue] = ...
    description: typing.Optional[AXValue] = ...
    value: typing.Optional[AXValue] = ...
    properties: typing.Optional[typing.List[AXProperty]] = ...
    parent_id: typing.Optional[AXNodeId] = ...
    child_ids: typing.Optional[typing.List[AXNodeId]] = ...
    backend_dom_node_id: typing.Optional[dom.BackendNodeId] = ...
    frame_id: typing.Optional[page.FrameId] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AXNode: ...
    def __init__(self, node_id, ignored, ignored_reasons, role, chrome_role, name, description, value, properties, parent_id, child_ids, backend_dom_node_id, frame_id) -> None: ...

def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_partial_ax_tree(node_id: typing.Optional[dom.NodeId] = None, backend_node_id: typing.Optional[dom.BackendNodeId] = None, object_id: typing.Optional[runtime.RemoteObjectId] = None, fetch_relatives: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[AXNode]]: ...
def get_full_ax_tree(depth: typing.Optional[int] = None, frame_id: typing.Optional[page.FrameId] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[AXNode]]: ...
def get_root_ax_node(frame_id: typing.Optional[page.FrameId] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, AXNode]: ...
def get_ax_node_and_ancestors(node_id: typing.Optional[dom.NodeId] = None, backend_node_id: typing.Optional[dom.BackendNodeId] = None, object_id: typing.Optional[runtime.RemoteObjectId] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[AXNode]]: ...
def get_child_ax_nodes(id_: AXNodeId, frame_id: typing.Optional[page.FrameId] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[AXNode]]: ...
def query_ax_tree(node_id: typing.Optional[dom.NodeId] = None, backend_node_id: typing.Optional[dom.BackendNodeId] = None, object_id: typing.Optional[runtime.RemoteObjectId] = None, accessible_name: typing.Optional[str] = None, role: typing.Optional[str] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[AXNode]]: ...

@dataclass
class LoadComplete:
    root: AXNode
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LoadComplete: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, root) -> None: ...

@dataclass
class NodesUpdated:
    nodes: typing.List[AXNode]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> NodesUpdated: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, nodes) -> None: ...

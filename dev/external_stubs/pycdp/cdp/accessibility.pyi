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
    BOOLEAN = 'boolean'
    TRISTATE = 'tristate'
    BOOLEAN_OR_UNDEFINED = 'booleanOrUndefined'
    IDREF = 'idref'
    IDREF_LIST = 'idrefList'
    INTEGER = 'integer'
    NODE = 'node'
    NODE_LIST = 'nodeList'
    NUMBER = 'number'
    STRING = 'string'
    COMPUTED_STRING = 'computedString'
    TOKEN = 'token'
    TOKEN_LIST = 'tokenList'
    DOM_RELATION = 'domRelation'
    ROLE = 'role'
    INTERNAL_ROLE = 'internalRole'
    VALUE_UNDEFINED = 'valueUndefined'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AXValueType: ...

class AXValueSourceType(enum.Enum):
    ATTRIBUTE = 'attribute'
    IMPLICIT = 'implicit'
    STYLE = 'style'
    CONTENTS = 'contents'
    PLACEHOLDER = 'placeholder'
    RELATED_ELEMENT = 'relatedElement'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AXValueSourceType: ...

class AXValueNativeSourceType(enum.Enum):
    DESCRIPTION = 'description'
    FIGCAPTION = 'figcaption'
    LABEL = 'label'
    LABELFOR = 'labelfor'
    LABELWRAPPED = 'labelwrapped'
    LEGEND = 'legend'
    RUBYANNOTATION = 'rubyannotation'
    TABLECAPTION = 'tablecaption'
    TITLE = 'title'
    OTHER = 'other'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AXValueNativeSourceType: ...

@dataclass
class AXValueSource:
    type_: AXValueSourceType
    value: AXValue | None = ...
    attribute: str | None = ...
    attribute_value: AXValue | None = ...
    superseded: bool | None = ...
    native_source: AXValueNativeSourceType | None = ...
    native_source_value: AXValue | None = ...
    invalid: bool | None = ...
    invalid_reason: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AXValueSource: ...

@dataclass
class AXRelatedNode:
    backend_dom_node_id: dom.BackendNodeId
    idref: str | None = ...
    text: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AXRelatedNode: ...

@dataclass
class AXProperty:
    name: AXPropertyName
    value: AXValue
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AXProperty: ...

@dataclass
class AXValue:
    type_: AXValueType
    value: typing.Any | None = ...
    related_nodes: list[AXRelatedNode] | None = ...
    sources: list[AXValueSource] | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AXValue: ...

class AXPropertyName(enum.Enum):
    ACTIONS = 'actions'
    BUSY = 'busy'
    DISABLED = 'disabled'
    EDITABLE = 'editable'
    FOCUSABLE = 'focusable'
    FOCUSED = 'focused'
    HIDDEN = 'hidden'
    HIDDEN_ROOT = 'hiddenRoot'
    INVALID = 'invalid'
    KEYSHORTCUTS = 'keyshortcuts'
    SETTABLE = 'settable'
    ROLEDESCRIPTION = 'roledescription'
    LIVE = 'live'
    ATOMIC = 'atomic'
    RELEVANT = 'relevant'
    ROOT = 'root'
    AUTOCOMPLETE = 'autocomplete'
    HAS_POPUP = 'hasPopup'
    LEVEL = 'level'
    MULTISELECTABLE = 'multiselectable'
    ORIENTATION = 'orientation'
    MULTILINE = 'multiline'
    READONLY = 'readonly'
    REQUIRED = 'required'
    VALUEMIN = 'valuemin'
    VALUEMAX = 'valuemax'
    VALUETEXT = 'valuetext'
    CHECKED = 'checked'
    EXPANDED = 'expanded'
    MODAL = 'modal'
    PRESSED = 'pressed'
    SELECTED = 'selected'
    ACTIVEDESCENDANT = 'activedescendant'
    CONTROLS = 'controls'
    DESCRIBEDBY = 'describedby'
    DETAILS = 'details'
    ERRORMESSAGE = 'errormessage'
    FLOWTO = 'flowto'
    LABELLEDBY = 'labelledby'
    OWNS = 'owns'
    URL = 'url'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AXPropertyName: ...

@dataclass
class AXNode:
    node_id: AXNodeId
    ignored: bool
    ignored_reasons: list[AXProperty] | None = ...
    role: AXValue | None = ...
    chrome_role: AXValue | None = ...
    name: AXValue | None = ...
    description: AXValue | None = ...
    value: AXValue | None = ...
    properties: list[AXProperty] | None = ...
    parent_id: AXNodeId | None = ...
    child_ids: list[AXNodeId] | None = ...
    backend_dom_node_id: dom.BackendNodeId | None = ...
    frame_id: page.FrameId | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AXNode: ...

def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_partial_ax_tree(node_id: dom.NodeId | None = None, backend_node_id: dom.BackendNodeId | None = None, object_id: runtime.RemoteObjectId | None = None, fetch_relatives: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[AXNode]]: ...
def get_full_ax_tree(depth: int | None = None, frame_id: page.FrameId | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[AXNode]]: ...
def get_root_ax_node(frame_id: page.FrameId | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, AXNode]: ...
def get_ax_node_and_ancestors(node_id: dom.NodeId | None = None, backend_node_id: dom.BackendNodeId | None = None, object_id: runtime.RemoteObjectId | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[AXNode]]: ...
def get_child_ax_nodes(id_: AXNodeId, frame_id: page.FrameId | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[AXNode]]: ...
def query_ax_tree(node_id: dom.NodeId | None = None, backend_node_id: dom.BackendNodeId | None = None, object_id: runtime.RemoteObjectId | None = None, accessible_name: str | None = None, role: str | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[AXNode]]: ...

@dataclass
class LoadComplete:
    root: AXNode
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LoadComplete: ...

@dataclass
class NodesUpdated:
    nodes: list[AXNode]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> NodesUpdated: ...

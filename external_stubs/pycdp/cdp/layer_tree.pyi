import typing
from . import dom as dom
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class LayerId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> LayerId: ...

class SnapshotId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SnapshotId: ...

@dataclass
class ScrollRect:
    rect: dom.Rect
    type_: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ScrollRect: ...
    def __init__(self, rect, type_) -> None: ...

@dataclass
class StickyPositionConstraint:
    sticky_box_rect: dom.Rect
    containing_block_rect: dom.Rect
    nearest_layer_shifting_sticky_box: typing.Optional[LayerId] = ...
    nearest_layer_shifting_containing_block: typing.Optional[LayerId] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> StickyPositionConstraint: ...
    def __init__(self, sticky_box_rect, containing_block_rect, nearest_layer_shifting_sticky_box, nearest_layer_shifting_containing_block) -> None: ...

@dataclass
class PictureTile:
    x: float
    y: float
    picture: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PictureTile: ...
    def __init__(self, x, y, picture) -> None: ...

@dataclass
class Layer:
    layer_id: LayerId
    offset_x: float
    offset_y: float
    width: float
    height: float
    paint_count: int
    draws_content: bool
    parent_layer_id: typing.Optional[LayerId] = ...
    backend_node_id: typing.Optional[dom.BackendNodeId] = ...
    transform: typing.Optional[typing.List[float]] = ...
    anchor_x: typing.Optional[float] = ...
    anchor_y: typing.Optional[float] = ...
    anchor_z: typing.Optional[float] = ...
    invisible: typing.Optional[bool] = ...
    scroll_rects: typing.Optional[typing.List[ScrollRect]] = ...
    sticky_position_constraint: typing.Optional[StickyPositionConstraint] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Layer: ...
    def __init__(self, layer_id, offset_x, offset_y, width, height, paint_count, draws_content, parent_layer_id, backend_node_id, transform, anchor_x, anchor_y, anchor_z, invisible, scroll_rects, sticky_position_constraint) -> None: ...

class PaintProfile(list):
    def to_json(self) -> typing.List[float]: ...
    @classmethod
    def from_json(cls, json: typing.List[float]) -> PaintProfile: ...

def compositing_reasons(layer_id: LayerId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[typing.List[str], typing.List[str]]]: ...
def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def load_snapshot(tiles: typing.List[PictureTile]) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, SnapshotId]: ...
def make_snapshot(layer_id: LayerId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, SnapshotId]: ...
def profile_snapshot(snapshot_id: SnapshotId, min_repeat_count: typing.Optional[int] = None, min_duration: typing.Optional[float] = None, clip_rect: typing.Optional[dom.Rect] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[PaintProfile]]: ...
def release_snapshot(snapshot_id: SnapshotId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def replay_snapshot(snapshot_id: SnapshotId, from_step: typing.Optional[int] = None, to_step: typing.Optional[int] = None, scale: typing.Optional[float] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, str]: ...
def snapshot_command_log(snapshot_id: SnapshotId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[dict]]: ...

@dataclass
class LayerPainted:
    layer_id: LayerId
    clip: dom.Rect
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LayerPainted: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, layer_id, clip) -> None: ...

@dataclass
class LayerTreeDidChange:
    layers: typing.Optional[typing.List[Layer]]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LayerTreeDidChange: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, layers) -> None: ...

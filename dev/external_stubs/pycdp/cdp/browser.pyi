import enum
import typing
from . import page as page, target as target
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class BrowserContextID(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> BrowserContextID: ...

class WindowID(int):
    def to_json(self) -> int: ...
    @classmethod
    def from_json(cls, json: int) -> WindowID: ...

class WindowState(enum.Enum):
    NORMAL: str
    MINIMIZED: str
    MAXIMIZED: str
    FULLSCREEN: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> WindowState: ...

@dataclass
class Bounds:
    left: typing.Optional[int] = ...
    top: typing.Optional[int] = ...
    width: typing.Optional[int] = ...
    height: typing.Optional[int] = ...
    window_state: typing.Optional[WindowState] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Bounds: ...
    def __init__(self, left, top, width, height, window_state) -> None: ...

class PermissionType(enum.Enum):
    ACCESSIBILITY_EVENTS: str
    AUDIO_CAPTURE: str
    BACKGROUND_SYNC: str
    BACKGROUND_FETCH: str
    CAPTURED_SURFACE_CONTROL: str
    CLIPBOARD_READ_WRITE: str
    CLIPBOARD_SANITIZED_WRITE: str
    DISPLAY_CAPTURE: str
    DURABLE_STORAGE: str
    FLASH: str
    GEOLOCATION: str
    IDLE_DETECTION: str
    LOCAL_FONTS: str
    MIDI: str
    MIDI_SYSEX: str
    NFC: str
    NOTIFICATIONS: str
    PAYMENT_HANDLER: str
    PERIODIC_BACKGROUND_SYNC: str
    PROTECTED_MEDIA_IDENTIFIER: str
    SENSORS: str
    STORAGE_ACCESS: str
    TOP_LEVEL_STORAGE_ACCESS: str
    VIDEO_CAPTURE: str
    VIDEO_CAPTURE_PAN_TILT_ZOOM: str
    WAKE_LOCK_SCREEN: str
    WAKE_LOCK_SYSTEM: str
    WINDOW_MANAGEMENT: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PermissionType: ...

class PermissionSetting(enum.Enum):
    GRANTED: str
    DENIED: str
    PROMPT: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PermissionSetting: ...

@dataclass
class PermissionDescriptor:
    name: str
    sysex: typing.Optional[bool] = ...
    user_visible_only: typing.Optional[bool] = ...
    allow_without_sanitization: typing.Optional[bool] = ...
    pan_tilt_zoom: typing.Optional[bool] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PermissionDescriptor: ...
    def __init__(self, name, sysex, user_visible_only, allow_without_sanitization, pan_tilt_zoom) -> None: ...

class BrowserCommandId(enum.Enum):
    OPEN_TAB_SEARCH: str
    CLOSE_TAB_SEARCH: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> BrowserCommandId: ...

@dataclass
class Bucket:
    low: int
    high: int
    count: int
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Bucket: ...
    def __init__(self, low, high, count) -> None: ...

@dataclass
class Histogram:
    name: str
    sum_: int
    count: int
    buckets: typing.List[Bucket]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Histogram: ...
    def __init__(self, name, sum_, count, buckets) -> None: ...

def set_permission(permission: PermissionDescriptor, setting: PermissionSetting, origin: typing.Optional[str] = None, browser_context_id: typing.Optional[BrowserContextID] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def grant_permissions(permissions: typing.List[PermissionType], origin: typing.Optional[str] = None, browser_context_id: typing.Optional[BrowserContextID] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def reset_permissions(browser_context_id: typing.Optional[BrowserContextID] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_download_behavior(behavior: str, browser_context_id: typing.Optional[BrowserContextID] = None, download_path: typing.Optional[str] = None, events_enabled: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def cancel_download(guid: str, browser_context_id: typing.Optional[BrowserContextID] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def close() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def crash() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def crash_gpu_process() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_version() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[str, str, str, str, str]]: ...
def get_browser_command_line() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[str]]: ...
def get_histograms(query: typing.Optional[str] = None, delta: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[Histogram]]: ...
def get_histogram(name: str, delta: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, Histogram]: ...
def get_window_bounds(window_id: WindowID) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, Bounds]: ...
def get_window_for_target(target_id: typing.Optional[target.TargetID] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[WindowID, Bounds]]: ...
def set_window_bounds(window_id: WindowID, bounds: Bounds) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_dock_tile(badge_label: typing.Optional[str] = None, image: typing.Optional[str] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def execute_browser_command(command_id: BrowserCommandId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def add_privacy_sandbox_enrollment_override(url: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class DownloadWillBegin:
    frame_id: page.FrameId
    guid: str
    url: str
    suggested_filename: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DownloadWillBegin: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, frame_id, guid, url, suggested_filename) -> None: ...

@dataclass
class DownloadProgress:
    guid: str
    total_bytes: float
    received_bytes: float
    state: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DownloadProgress: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, guid, total_bytes, received_bytes, state) -> None: ...

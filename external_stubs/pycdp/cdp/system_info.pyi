import enum
import typing
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

@dataclass
class GPUDevice:
    vendor_id: float
    device_id: float
    vendor_string: str
    device_string: str
    driver_vendor: str
    driver_version: str
    sub_sys_id: typing.Optional[float] = ...
    revision: typing.Optional[float] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> GPUDevice: ...
    def __init__(self, vendor_id, device_id, vendor_string, device_string, driver_vendor, driver_version, sub_sys_id, revision) -> None: ...

@dataclass
class Size:
    width: int
    height: int
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Size: ...
    def __init__(self, width, height) -> None: ...

@dataclass
class VideoDecodeAcceleratorCapability:
    profile: str
    max_resolution: Size
    min_resolution: Size
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> VideoDecodeAcceleratorCapability: ...
    def __init__(self, profile, max_resolution, min_resolution) -> None: ...

@dataclass
class VideoEncodeAcceleratorCapability:
    profile: str
    max_resolution: Size
    max_framerate_numerator: int
    max_framerate_denominator: int
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> VideoEncodeAcceleratorCapability: ...
    def __init__(self, profile, max_resolution, max_framerate_numerator, max_framerate_denominator) -> None: ...

class SubsamplingFormat(enum.Enum):
    YUV420: str
    YUV422: str
    YUV444: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SubsamplingFormat: ...

class ImageType(enum.Enum):
    JPEG: str
    WEBP: str
    UNKNOWN: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ImageType: ...

@dataclass
class ImageDecodeAcceleratorCapability:
    image_type: ImageType
    max_dimensions: Size
    min_dimensions: Size
    subsamplings: typing.List[SubsamplingFormat]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ImageDecodeAcceleratorCapability: ...
    def __init__(self, image_type, max_dimensions, min_dimensions, subsamplings) -> None: ...

@dataclass
class GPUInfo:
    devices: typing.List[GPUDevice]
    driver_bug_workarounds: typing.List[str]
    video_decoding: typing.List[VideoDecodeAcceleratorCapability]
    video_encoding: typing.List[VideoEncodeAcceleratorCapability]
    image_decoding: typing.List[ImageDecodeAcceleratorCapability]
    aux_attributes: typing.Optional[dict] = ...
    feature_status: typing.Optional[dict] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> GPUInfo: ...
    def __init__(self, devices, driver_bug_workarounds, video_decoding, video_encoding, image_decoding, aux_attributes, feature_status) -> None: ...

@dataclass
class ProcessInfo:
    type_: str
    id_: int
    cpu_time: float
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ProcessInfo: ...
    def __init__(self, type_, id_, cpu_time) -> None: ...

def get_info() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[GPUInfo, str, str, str]]: ...
def get_feature_state(feature_state: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, bool]: ...
def get_process_info() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[ProcessInfo]]: ...

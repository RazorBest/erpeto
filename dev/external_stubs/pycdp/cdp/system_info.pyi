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
    sub_sys_id: float | None = ...
    revision: float | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> GPUDevice: ...

@dataclass
class Size:
    width: int
    height: int
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Size: ...

@dataclass
class VideoDecodeAcceleratorCapability:
    profile: str
    max_resolution: Size
    min_resolution: Size
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> VideoDecodeAcceleratorCapability: ...

@dataclass
class VideoEncodeAcceleratorCapability:
    profile: str
    max_resolution: Size
    max_framerate_numerator: int
    max_framerate_denominator: int
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> VideoEncodeAcceleratorCapability: ...

class SubsamplingFormat(enum.Enum):
    YUV420 = 'yuv420'
    YUV422 = 'yuv422'
    YUV444 = 'yuv444'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SubsamplingFormat: ...

class ImageType(enum.Enum):
    JPEG = 'jpeg'
    WEBP = 'webp'
    UNKNOWN = 'unknown'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ImageType: ...

@dataclass
class ImageDecodeAcceleratorCapability:
    image_type: ImageType
    max_dimensions: Size
    min_dimensions: Size
    subsamplings: list[SubsamplingFormat]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ImageDecodeAcceleratorCapability: ...

@dataclass
class GPUInfo:
    devices: list[GPUDevice]
    driver_bug_workarounds: list[str]
    video_decoding: list[VideoDecodeAcceleratorCapability]
    video_encoding: list[VideoEncodeAcceleratorCapability]
    image_decoding: list[ImageDecodeAcceleratorCapability]
    aux_attributes: dict | None = ...
    feature_status: dict | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> GPUInfo: ...

@dataclass
class ProcessInfo:
    type_: str
    id_: int
    cpu_time: float
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ProcessInfo: ...

def get_info() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, tuple[GPUInfo, str, str, str]]: ...
def get_feature_state(feature_state: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, bool]: ...
def get_process_info() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[ProcessInfo]]: ...

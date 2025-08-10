import enum
import typing
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class GraphObjectId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> GraphObjectId: ...

class ContextType(enum.Enum):
    REALTIME = 'realtime'
    OFFLINE = 'offline'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ContextType: ...

class ContextState(enum.Enum):
    SUSPENDED = 'suspended'
    RUNNING = 'running'
    CLOSED = 'closed'
    INTERRUPTED = 'interrupted'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ContextState: ...

class NodeType(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> NodeType: ...

class ChannelCountMode(enum.Enum):
    CLAMPED_MAX = 'clamped-max'
    EXPLICIT = 'explicit'
    MAX_ = 'max'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ChannelCountMode: ...

class ChannelInterpretation(enum.Enum):
    DISCRETE = 'discrete'
    SPEAKERS = 'speakers'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ChannelInterpretation: ...

class ParamType(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ParamType: ...

class AutomationRate(enum.Enum):
    A_RATE = 'a-rate'
    K_RATE = 'k-rate'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AutomationRate: ...

@dataclass
class ContextRealtimeData:
    current_time: float
    render_capacity: float
    callback_interval_mean: float
    callback_interval_variance: float
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ContextRealtimeData: ...

@dataclass
class BaseAudioContext:
    context_id: GraphObjectId
    context_type: ContextType
    context_state: ContextState
    callback_buffer_size: float
    max_output_channel_count: float
    sample_rate: float
    realtime_data: ContextRealtimeData | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BaseAudioContext: ...

@dataclass
class AudioListener:
    listener_id: GraphObjectId
    context_id: GraphObjectId
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AudioListener: ...

@dataclass
class AudioNode:
    node_id: GraphObjectId
    context_id: GraphObjectId
    node_type: NodeType
    number_of_inputs: float
    number_of_outputs: float
    channel_count: float
    channel_count_mode: ChannelCountMode
    channel_interpretation: ChannelInterpretation
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AudioNode: ...

@dataclass
class AudioParam:
    param_id: GraphObjectId
    node_id: GraphObjectId
    context_id: GraphObjectId
    param_type: ParamType
    rate: AutomationRate
    default_value: float
    min_value: float
    max_value: float
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AudioParam: ...

def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_realtime_data(context_id: GraphObjectId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, ContextRealtimeData]: ...

@dataclass
class ContextCreated:
    context: BaseAudioContext
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ContextCreated: ...

@dataclass
class ContextWillBeDestroyed:
    context_id: GraphObjectId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ContextWillBeDestroyed: ...

@dataclass
class ContextChanged:
    context: BaseAudioContext
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ContextChanged: ...

@dataclass
class AudioListenerCreated:
    listener: AudioListener
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AudioListenerCreated: ...

@dataclass
class AudioListenerWillBeDestroyed:
    context_id: GraphObjectId
    listener_id: GraphObjectId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AudioListenerWillBeDestroyed: ...

@dataclass
class AudioNodeCreated:
    node: AudioNode
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AudioNodeCreated: ...

@dataclass
class AudioNodeWillBeDestroyed:
    context_id: GraphObjectId
    node_id: GraphObjectId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AudioNodeWillBeDestroyed: ...

@dataclass
class AudioParamCreated:
    param: AudioParam
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AudioParamCreated: ...

@dataclass
class AudioParamWillBeDestroyed:
    context_id: GraphObjectId
    node_id: GraphObjectId
    param_id: GraphObjectId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AudioParamWillBeDestroyed: ...

@dataclass
class NodesConnected:
    context_id: GraphObjectId
    source_id: GraphObjectId
    destination_id: GraphObjectId
    source_output_index: float | None
    destination_input_index: float | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> NodesConnected: ...

@dataclass
class NodesDisconnected:
    context_id: GraphObjectId
    source_id: GraphObjectId
    destination_id: GraphObjectId
    source_output_index: float | None
    destination_input_index: float | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> NodesDisconnected: ...

@dataclass
class NodeParamConnected:
    context_id: GraphObjectId
    source_id: GraphObjectId
    destination_id: GraphObjectId
    source_output_index: float | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> NodeParamConnected: ...

@dataclass
class NodeParamDisconnected:
    context_id: GraphObjectId
    source_id: GraphObjectId
    destination_id: GraphObjectId
    source_output_index: float | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> NodeParamDisconnected: ...

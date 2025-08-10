import enum
import typing
from . import dom as dom, page as page
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

@dataclass
class CreditCard:
    number: str
    name: str
    expiry_month: str
    expiry_year: str
    cvc: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CreditCard: ...

@dataclass
class AddressField:
    name: str
    value: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AddressField: ...

@dataclass
class AddressFields:
    fields: list[AddressField]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AddressFields: ...

@dataclass
class Address:
    fields: list[AddressField]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Address: ...

@dataclass
class AddressUI:
    address_fields: list[AddressFields]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AddressUI: ...

class FillingStrategy(enum.Enum):
    AUTOCOMPLETE_ATTRIBUTE = 'autocompleteAttribute'
    AUTOFILL_INFERRED = 'autofillInferred'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> FillingStrategy: ...

@dataclass
class FilledField:
    html_type: str
    id_: str
    name: str
    value: str
    autofill_type: str
    filling_strategy: FillingStrategy
    frame_id: page.FrameId
    field_id: dom.BackendNodeId
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FilledField: ...

def trigger(field_id: dom.BackendNodeId, card: CreditCard, frame_id: page.FrameId | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_addresses(addresses: list[Address]) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class AddressFormFilled:
    filled_fields: list[FilledField]
    address_ui: AddressUI
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AddressFormFilled: ...

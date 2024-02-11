import enum
import typing
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class LoginState(enum.Enum):
    SIGN_IN: str
    SIGN_UP: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> LoginState: ...

class DialogType(enum.Enum):
    ACCOUNT_CHOOSER: str
    AUTO_REAUTHN: str
    CONFIRM_IDP_LOGIN: str
    ERROR: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> DialogType: ...

class DialogButton(enum.Enum):
    CONFIRM_IDP_LOGIN_CONTINUE: str
    ERROR_GOT_IT: str
    ERROR_MORE_DETAILS: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> DialogButton: ...

@dataclass
class Account:
    account_id: str
    email: str
    name: str
    given_name: str
    picture_url: str
    idp_config_url: str
    idp_login_url: str
    login_state: LoginState
    terms_of_service_url: typing.Optional[str] = ...
    privacy_policy_url: typing.Optional[str] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Account: ...
    def __init__(self, account_id, email, name, given_name, picture_url, idp_config_url, idp_login_url, login_state, terms_of_service_url, privacy_policy_url) -> None: ...

def enable(disable_rejection_delay: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def select_account(dialog_id: str, account_index: int) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def click_dialog_button(dialog_id: str, dialog_button: DialogButton) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def dismiss_dialog(dialog_id: str, trigger_cooldown: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def reset_cooldown() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class DialogShown:
    dialog_id: str
    dialog_type: DialogType
    accounts: typing.List[Account]
    title: str
    subtitle: typing.Optional[str]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DialogShown: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, dialog_id, dialog_type, accounts, title, subtitle) -> None: ...

@dataclass
class DialogClosed:
    dialog_id: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DialogClosed: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, dialog_id) -> None: ...

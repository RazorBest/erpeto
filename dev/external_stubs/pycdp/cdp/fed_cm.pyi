import enum
import typing
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class LoginState(enum.Enum):
    SIGN_IN = 'SignIn'
    SIGN_UP = 'SignUp'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> LoginState: ...

class DialogType(enum.Enum):
    ACCOUNT_CHOOSER = 'AccountChooser'
    AUTO_REAUTHN = 'AutoReauthn'
    CONFIRM_IDP_LOGIN = 'ConfirmIdpLogin'
    ERROR = 'Error'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> DialogType: ...

class DialogButton(enum.Enum):
    CONFIRM_IDP_LOGIN_CONTINUE = 'ConfirmIdpLoginContinue'
    ERROR_GOT_IT = 'ErrorGotIt'
    ERROR_MORE_DETAILS = 'ErrorMoreDetails'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> DialogButton: ...

class AccountUrlType(enum.Enum):
    TERMS_OF_SERVICE = 'TermsOfService'
    PRIVACY_POLICY = 'PrivacyPolicy'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AccountUrlType: ...

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
    terms_of_service_url: str | None = ...
    privacy_policy_url: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Account: ...

def enable(disable_rejection_delay: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def select_account(dialog_id: str, account_index: int) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def click_dialog_button(dialog_id: str, dialog_button: DialogButton) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def open_url(dialog_id: str, account_index: int, account_url_type: AccountUrlType) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def dismiss_dialog(dialog_id: str, trigger_cooldown: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def reset_cooldown() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class DialogShown:
    dialog_id: str
    dialog_type: DialogType
    accounts: list[Account]
    title: str
    subtitle: str | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DialogShown: ...

@dataclass
class DialogClosed:
    dialog_id: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DialogClosed: ...

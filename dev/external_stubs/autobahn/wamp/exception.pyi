from _typeshed import Incomplete

__all__ = ['Error', 'SessionNotReady', 'SerializationError', 'InvalidUriError', 'ProtocolError', 'TransportLost', 'ApplicationError', 'NotAuthorized', 'InvalidUri', 'InvalidPayload', 'TypeCheckError']

class Error(RuntimeError): ...
class SessionNotReady(Error): ...
class SerializationError(Error): ...
class InvalidUriError(Error): ...
class ProtocolError(Error): ...
class TransportLost(Error): ...

class ApplicationError(Error):
    INVALID_URI: str
    INVALID_PAYLOAD: str
    PAYLOAD_SIZE_EXCEEDED: str
    NO_SUCH_PROCEDURE: str
    PROCEDURE_ALREADY_EXISTS: str
    PROCEDURE_EXISTS_INVOCATION_POLICY_CONFLICT: str
    NO_SUCH_REGISTRATION: str
    NO_SUCH_SUBSCRIPTION: str
    NO_SUCH_SESSION: str
    INVALID_ARGUMENT: str
    SYSTEM_SHUTDOWN: str
    CLOSE_REALM: str
    GOODBYE_AND_OUT: str
    NOT_AUTHORIZED: str
    AUTHORIZATION_FAILED: str
    AUTHENTICATION_FAILED: str
    NO_AUTH_METHOD: str
    NO_SUCH_REALM: str
    NO_SUCH_ROLE: str
    NO_SUCH_PRINCIPAL: str
    CANCELED: str
    TIMEOUT: str
    NO_ELIGIBLE_CALLEE: str
    ENC_NO_PAYLOAD_CODEC: str
    ENC_TRUSTED_URI_MISMATCH: str
    ENC_DECRYPT_ERROR: str
    TYPE_CHECK_ERROR: str
    kwargs: Incomplete
    error: Incomplete
    enc_algo: Incomplete
    callee: Incomplete
    callee_authid: Incomplete
    callee_authrole: Incomplete
    forward_for: Incomplete
    def __init__(self, error, *args, **kwargs) -> None: ...
    def error_message(self): ...
    def __unicode__(self): ...

class NotAuthorized(Exception): ...
class InvalidUri(Exception): ...
class InvalidPayload(Exception): ...

class TypeCheckError(ApplicationError):
    def __init__(self, *args, **kwargs) -> None: ...

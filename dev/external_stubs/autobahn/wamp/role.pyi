from _typeshed import Incomplete
from autobahn import util

__all__ = ['RoleFeatures', 'RoleBrokerFeatures', 'RoleSubscriberFeatures', 'RolePublisherFeatures', 'RoleDealerFeatures', 'RoleCallerFeatures', 'RoleCalleeFeatures', 'ROLE_NAME_TO_CLASS', 'DEFAULT_CLIENT_ROLES']

class RoleFeatures(util.EqualityMixin):
    ROLE: Incomplete

class RoleBrokerFeatures(RoleFeatures):
    ROLE: str
    publisher_identification: Incomplete
    publication_trustlevels: Incomplete
    pattern_based_subscription: Incomplete
    session_meta_api: Incomplete
    subscription_meta_api: Incomplete
    subscriber_blackwhite_listing: Incomplete
    publisher_exclusion: Incomplete
    subscription_revocation: Incomplete
    event_history: Incomplete
    payload_transparency: Incomplete
    x_acknowledged_event_delivery: Incomplete
    payload_encryption_cryptobox: Incomplete
    event_retention: Incomplete
    def __init__(self, publisher_identification: Incomplete | None = None, publication_trustlevels: Incomplete | None = None, pattern_based_subscription: Incomplete | None = None, session_meta_api: Incomplete | None = None, subscription_meta_api: Incomplete | None = None, subscriber_blackwhite_listing: Incomplete | None = None, publisher_exclusion: Incomplete | None = None, subscription_revocation: Incomplete | None = None, event_history: Incomplete | None = None, payload_transparency: Incomplete | None = None, x_acknowledged_event_delivery: Incomplete | None = None, payload_encryption_cryptobox: Incomplete | None = None, event_retention: Incomplete | None = None, **kwargs) -> None: ...

class RoleSubscriberFeatures(RoleFeatures):
    ROLE: str
    publisher_identification: Incomplete
    publication_trustlevels: Incomplete
    pattern_based_subscription: Incomplete
    subscription_revocation: Incomplete
    event_history: Incomplete
    payload_transparency: Incomplete
    payload_encryption_cryptobox: Incomplete
    def __init__(self, publisher_identification: Incomplete | None = None, publication_trustlevels: Incomplete | None = None, pattern_based_subscription: Incomplete | None = None, subscription_revocation: Incomplete | None = None, event_history: Incomplete | None = None, payload_transparency: Incomplete | None = None, payload_encryption_cryptobox: Incomplete | None = None, **kwargs) -> None: ...

class RolePublisherFeatures(RoleFeatures):
    ROLE: str
    publisher_identification: Incomplete
    subscriber_blackwhite_listing: Incomplete
    publisher_exclusion: Incomplete
    payload_transparency: Incomplete
    x_acknowledged_event_delivery: Incomplete
    payload_encryption_cryptobox: Incomplete
    def __init__(self, publisher_identification: Incomplete | None = None, subscriber_blackwhite_listing: Incomplete | None = None, publisher_exclusion: Incomplete | None = None, payload_transparency: Incomplete | None = None, x_acknowledged_event_delivery: Incomplete | None = None, payload_encryption_cryptobox: Incomplete | None = None, **kwargs) -> None: ...

class RoleDealerFeatures(RoleFeatures):
    ROLE: str
    caller_identification: Incomplete
    call_trustlevels: Incomplete
    pattern_based_registration: Incomplete
    session_meta_api: Incomplete
    registration_meta_api: Incomplete
    shared_registration: Incomplete
    call_timeout: Incomplete
    call_canceling: Incomplete
    progressive_call_results: Incomplete
    registration_revocation: Incomplete
    payload_transparency: Incomplete
    testament_meta_api: Incomplete
    payload_encryption_cryptobox: Incomplete
    def __init__(self, caller_identification: Incomplete | None = None, call_trustlevels: Incomplete | None = None, pattern_based_registration: Incomplete | None = None, session_meta_api: Incomplete | None = None, registration_meta_api: Incomplete | None = None, shared_registration: Incomplete | None = None, call_timeout: Incomplete | None = None, call_canceling: Incomplete | None = None, progressive_call_results: Incomplete | None = None, registration_revocation: Incomplete | None = None, payload_transparency: Incomplete | None = None, testament_meta_api: Incomplete | None = None, payload_encryption_cryptobox: Incomplete | None = None, **kwargs) -> None: ...

class RoleCallerFeatures(RoleFeatures):
    ROLE: str
    caller_identification: Incomplete
    call_timeout: Incomplete
    call_canceling: Incomplete
    progressive_call_results: Incomplete
    payload_transparency: Incomplete
    payload_encryption_cryptobox: Incomplete
    def __init__(self, caller_identification: Incomplete | None = None, call_timeout: Incomplete | None = None, call_canceling: Incomplete | None = None, progressive_call_results: Incomplete | None = None, payload_transparency: Incomplete | None = None, payload_encryption_cryptobox: Incomplete | None = None, **kwargs) -> None: ...

class RoleCalleeFeatures(RoleFeatures):
    ROLE: str
    caller_identification: Incomplete
    call_trustlevels: Incomplete
    pattern_based_registration: Incomplete
    shared_registration: Incomplete
    call_timeout: Incomplete
    call_canceling: Incomplete
    progressive_call_results: Incomplete
    registration_revocation: Incomplete
    payload_transparency: Incomplete
    payload_encryption_cryptobox: Incomplete
    def __init__(self, caller_identification: Incomplete | None = None, call_trustlevels: Incomplete | None = None, pattern_based_registration: Incomplete | None = None, shared_registration: Incomplete | None = None, call_timeout: Incomplete | None = None, call_canceling: Incomplete | None = None, progressive_call_results: Incomplete | None = None, registration_revocation: Incomplete | None = None, payload_transparency: Incomplete | None = None, payload_encryption_cryptobox: Incomplete | None = None, **kwargs) -> None: ...

ROLE_NAME_TO_CLASS: Incomplete
DEFAULT_CLIENT_ROLES: Incomplete

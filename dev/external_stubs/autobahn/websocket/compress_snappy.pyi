from _typeshed import Incomplete
from autobahn.websocket.compress_base import PerMessageCompress, PerMessageCompressOffer, PerMessageCompressOfferAccept, PerMessageCompressResponse, PerMessageCompressResponseAccept

__all__ = ['PerMessageSnappyMixin', 'PerMessageSnappyOffer', 'PerMessageSnappyOfferAccept', 'PerMessageSnappyResponse', 'PerMessageSnappyResponseAccept', 'PerMessageSnappy']

class PerMessageSnappyMixin:
    EXTENSION_NAME: str

class PerMessageSnappyOffer(PerMessageCompressOffer, PerMessageSnappyMixin):
    @classmethod
    def parse(cls, params): ...
    accept_no_context_takeover: Incomplete
    request_no_context_takeover: Incomplete
    def __init__(self, accept_no_context_takeover: bool = True, request_no_context_takeover: bool = False) -> None: ...
    def get_extension_string(self): ...
    def __json__(self): ...

class PerMessageSnappyOfferAccept(PerMessageCompressOfferAccept, PerMessageSnappyMixin):
    offer: Incomplete
    request_no_context_takeover: Incomplete
    no_context_takeover: Incomplete
    def __init__(self, offer, request_no_context_takeover: bool = False, no_context_takeover: Incomplete | None = None) -> None: ...
    def get_extension_string(self): ...
    def __json__(self): ...

class PerMessageSnappyResponse(PerMessageCompressResponse, PerMessageSnappyMixin):
    @classmethod
    def parse(cls, params): ...
    client_no_context_takeover: Incomplete
    server_no_context_takeover: Incomplete
    def __init__(self, client_no_context_takeover, server_no_context_takeover) -> None: ...
    def __json__(self): ...

class PerMessageSnappyResponseAccept(PerMessageCompressResponseAccept, PerMessageSnappyMixin):
    response: Incomplete
    no_context_takeover: Incomplete
    def __init__(self, response, no_context_takeover: Incomplete | None = None) -> None: ...
    def __json__(self): ...

class PerMessageSnappy(PerMessageCompress, PerMessageSnappyMixin):
    @classmethod
    def create_from_response_accept(cls, is_server, accept): ...
    @classmethod
    def create_from_offer_accept(cls, is_server, accept): ...
    server_no_context_takeover: Incomplete
    client_no_context_takeover: Incomplete
    def __init__(self, is_server, server_no_context_takeover, client_no_context_takeover) -> None: ...
    def __json__(self): ...
    def start_compress_message(self) -> None: ...
    def compress_message_data(self, data): ...
    def end_compress_message(self): ...
    def start_decompress_message(self) -> None: ...
    def decompress_message_data(self, data): ...
    def end_decompress_message(self) -> None: ...
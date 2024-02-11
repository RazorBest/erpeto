import json
import pytest

from pycdp import cdp

from .action_serializer import replace_action_body_with_length, replace_date_headers, ActionsJSONEncoder, json_actions_loads
from ..main import collect_communications, HttpCommunication, parse_communications_into_actions

class EventMock:
    """Mock class for generating CDP events and responding to CDP functions."""
    def __init__(self, events):
        self.next_events = events
        self.emitted_events = []

    def get_response_body(self, params):
        request_id = params["requestId"]
        for event in self.emitted_events:
            if event["method"] != "Network.loadingFinished":
                continue
            if event["params"]["requestId"] != request_id:
                continue

            return "*" * int(event["params"]["encodedDataLength"]), False

    async def execute(self, method_generator):
        for method in method_generator:
            if method["method"] == "Network.getResponseBody":
                return self.get_response_body(method["params"])

    def __aiter__(self):
        return self

    async def __anext__(self):
        if len(self.next_events) == 0:
            raise StopAsyncIteration

        event = self.next_events.pop(0)
        self.emitted_events.append(event)

        return cdp.util.parse_json_event(event)

class UrlfilterMock:
    def should_block(self, *args, **kwargs):
        return False

# These communications were parsed by hand from events_youtube.json
YOUTUBE_FIRST_COMMUNICATION = HttpCommunication(
    request_id=cdp.network.RequestId("3A87DEB65CD78F73BE75481B813F000E"),
    ignored=False,
    events=[
        cdp.network.RequestWillBeSent(
            request_id=cdp.network.RequestId("3A87DEB65CD78F73BE75481B813F000E"),
            loader_id=cdp.network.LoaderId("3A87DEB65CD78F73BE75481B813F000E"),
            document_url="http://youtube.com/",
            request=cdp.network.Request(
                url="http://youtube.com/",
                method="GET",
                headers=cdp.network.Headers({
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                }),
                initial_priority=cdp.network.ResourcePriority.VERY_HIGH,
                referrer_policy="strict-origin-when-cross-origin",
                mixed_content_type=cdp.security.MixedContentType.NONE,
                is_same_site=True,
            ),
            timestamp=cdp.network.MonotonicTime(84600.773374),
            wall_time=cdp.network.TimeSinceEpoch(1705002946.163711),
            initiator=cdp.network.Initiator(type_="other"),
            redirect_has_extra_info=False,
            redirect_response=None,
            type_=cdp.network.ResourceType.DOCUMENT,
            frame_id=cdp.page.FrameId("B3DCCB96E4F9C2FA162B31B3F219CE94"),
            has_user_gesture=False,
        ),
        cdp.network.RequestWillBeSent(
            request_id=cdp.network.RequestId("3A87DEB65CD78F73BE75481B813F000E"),
            loader_id=cdp.network.LoaderId("3A87DEB65CD78F73BE75481B813F000E"),
            document_url="https://youtube.com/",
            request=cdp.network.Request(
                url="https://youtube.com/",
                method="GET",
                headers=cdp.network.Headers({
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                }),
                initial_priority=cdp.network.ResourcePriority.VERY_HIGH,
                referrer_policy="strict-origin-when-cross-origin",
                mixed_content_type=cdp.security.MixedContentType.NONE,
                is_same_site=True,
            ),
            timestamp=cdp.network.MonotonicTime(84600.778207),
            wall_time=cdp.network.TimeSinceEpoch(1705002946.168555),
            initiator=cdp.network.Initiator(type_="other"),
            redirect_has_extra_info=True,
            redirect_response=cdp.network.Response(
                url="http://youtube.com/",
                status=307,
                status_text="Internal Redirect",
                headers=cdp.network.Headers({
                    "Cross-Origin-Resource-Policy": "Cross-Origin",
                    "Location": "https://youtube.com/",
                    "Non-Authoritative-Reason": "HSTS"
                }),
                mime_type="",
                connection_reused=False,
                connection_id=0.0,
                encoded_data_length=0.0,
                security_state=cdp.security.SecurityState.INSECURE,
                remote_ip_address="",
                remote_port=0,
                from_disk_cache=False,
                from_service_worker=False,
                from_prefetch_cache=False,
                timing=cdp.network.ResourceTiming(
                    connect_end=-1.0,
                    connect_start=-1.0,
                    dns_end=-1.0,
                    dns_start=-1.0,
                    proxy_end=-1.0,
                    proxy_start=-1.0,
                    push_end=0.0,
                    push_start=0.0,
                    receive_headers_end=0.06,
                    receive_headers_start=0.06,
                    request_time=84600.776614,
                    send_end=0.06,
                    send_start=0.06,
                    ssl_end=-1.0,
                    ssl_start=-1.0,
                    worker_fetch_start=-1.0,
                    worker_ready=-1.0,
                    worker_respond_with_settled=-1.0,
                    worker_start=-1.0,
                ),
                response_time=cdp.network.TimeSinceEpoch(1705002946166.988),
                protocol="http/1.1",
                alternate_protocol_usage=cdp.network.AlternateProtocolUsage.UNSPECIFIED_REASON,
            ),
            type_=cdp.network.ResourceType.DOCUMENT,
            frame_id=cdp.page.FrameId("B3DCCB96E4F9C2FA162B31B3F219CE94"),
            has_user_gesture=False,
        ),
        cdp.network.RequestWillBeSentExtraInfo(
            request_id=cdp.network.RequestId("3A87DEB65CD78F73BE75481B813F000E"),
            associated_cookies=[],
            headers=cdp.network.Headers({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            }),
            connect_timing=cdp.network.ConnectTiming(84600.776614),
            client_security_state=None,
            site_has_cookie_in_other_partition=False,
        ),
        cdp.network.ResponseReceivedExtraInfo(
            request_id=cdp.network.RequestId("3A87DEB65CD78F73BE75481B813F000E"),
            blocked_cookies=[],
            headers=cdp.network.Headers({
                "Cross-Origin-Resource-Policy": "Cross-Origin",
                "Location": "https://youtube.com/",
                "Non-Authoritative-Reason": "HSTS"
            }),
            resource_ip_address_space=cdp.network.IPAddressSpace.UNKNOWN,
            status_code=307,
            headers_text="HTTP/1.1 307 Internal Redirect\r\nLocation: https://youtube.com/\r\nCross-Origin-Resource-Policy: Cross-Origin\r\nNon-Authoritative-Reason: HSTS\r\n\r\n",       
            cookie_partition_key="http://youtube.com",
            cookie_partition_key_opaque=False
        ),
        cdp.network.RequestWillBeSent(
            request_id=cdp.network.RequestId("3A87DEB65CD78F73BE75481B813F000E"),
            loader_id=cdp.network.LoaderId("3A87DEB65CD78F73BE75481B813F000E"),
            document_url="https://www.youtube.com/",
            request=cdp.network.Request(
                url="https://www.youtube.com/",
                method="GET",
                headers=cdp.network.Headers({
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }),
                initial_priority=cdp.network.ResourcePriority.VERY_HIGH,
                referrer_policy="strict-origin-when-cross-origin",
                mixed_content_type=cdp.security.MixedContentType.NONE,
                is_same_site=True,
            ),
            timestamp=cdp.network.MonotonicTime(84600.780652),
            wall_time=cdp.network.TimeSinceEpoch(1705002946.171028),
            initiator=cdp.network.Initiator(type_="other"),
            redirect_has_extra_info=False,
            redirect_response=cdp.network.Response(
                url="https://youtube.com/",
                status=301,
                status_text="",
                headers=cdp.network.Headers({
                    "accept-ch": "Sec-CH-UA-Arch, Sec-CH-UA-Bitness, Sec-CH-UA-Full-Version, Sec-CH-UA-Full-Version-List, Sec-CH-UA-Model, Sec-CH-UA-WoW64, Sec-CH-UA-Form-Factor, Sec-CH-UA-Platform, Sec-CH-UA-Platform-Version",                                                                                                                           "access-control-allow-credentials": "true",                                                                   "access-control-allow-origin": "https://www.youtube.com",                                                     "alt-svc": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000",                                              "cache-control": "private, max-age=31536000",                                                                 "content-length": "0",
                    "content-type": "application/binary",
                    "cross-origin-opener-policy": "same-origin-allow-popups; report-to=\"youtube_main\"",
                    "date": "Thu, 1 Jan 1970 00:00:00 GMT",
                    "expires": "Thu, 1 Jan 1970 00:00:00 GMT",
                    "location": "https://www.youtube.com/",
                    "origin-trial": "AvC9UlR6RDk2crliDsFl66RWLnTbHrDbp+DiY6AYz/PNQ4G4tdUTjrHYr2sghbkhGQAVxb7jaPTHpEVBz0uzQwkAAAB4eyJvcmlnaW4iOiJodHRwczovL3lvdXR1YmUuY29tOjQ0MyIsImZlYXR1cmUiOiJXZWJWaWV3WFJlcXVlc3RlZFdpdGhEZXByZWNhdGlvbiIsImV4cGlyeSI6MTcxOTUzMjc5OSwiaXNTdWJkb21haW4iOnRydWV9",
                    "p3p": "CP=\"This is not a P3P policy! See g.co/p3phelp for more info.\"",
                    "permissions-policy": "ch-ua-arch=*, ch-ua-bitness=*, ch-ua-full-version=*, ch-ua-full-version-list=*, ch-ua-model=*, ch-ua-wow64=*, ch-ua-form-factor=*, ch-ua-platform=*, ch-ua-platform-version=*",
                    "report-to": "{\"group\":\"youtube_main\",\"max_age\":2592000,\"endpoints\":[{\"url\":\"https://csp.withgoogle.com/csp/report-to/youtube_main\"}]}",
                    "server": "ESF",
                    "vary": "Sec-CH-UA-Arch, Sec-CH-UA-Bitness, Sec-CH-UA-Full-Version, Sec-CH-UA-Full-Version-List, Sec-CH-UA-Model, Sec-CH-UA-WoW64, Sec-CH-UA-Form-Factor, Sec-CH-UA-Platform, Sec-CH-UA-Platform-Version",
                    "x-content-type-options": "nosniff",
                    "x-frame-options": "SAMEORIGIN",
                    "x-xss-protection": "0",
                }),
                mime_type="application/binary",
                connection_reused=False,
                connection_id=0.0,
                encoded_data_length=0.0,
                security_state=cdp.security.SecurityState.SECURE,
                remote_ip_address="142.251.208.142",
                remote_port=443,
                from_disk_cache=True,
                from_service_worker=False,
                from_prefetch_cache=False,
                timing=cdp.network.ResourceTiming(
                    connect_end=-1.0,
                    connect_start=-1.0,
                    dns_end=-1.0,
                    dns_start=-1.0,
                    proxy_end=-1.0,
                    proxy_start=-1.0,
                    push_end=0.0,
                    push_start=0.0,
                    receive_headers_end=0.822,
                    receive_headers_start=0.757,
                    request_time=84600.778656,
                    send_end=0.239,
                    send_start=0.239,
                    ssl_end=-1.0,
                    ssl_start=-1.0,
                    worker_fetch_start=-1.0,
                    worker_ready=-1.0,
                    worker_respond_with_settled=-1.0,
                    worker_start=-1.0,
                ),
                response_time=cdp.network.TimeSinceEpoch(1705000332131.541),
                protocol="h3",
                alternate_protocol_usage=cdp.network.AlternateProtocolUsage.UNSPECIFIED_REASON,
                security_details=cdp.network.SecurityDetails(
                    protocol="QUIC",
                    key_exchange="",
                    cipher="AES_128_GCM",
                    certificate_id=cdp.security.CertificateId(0),
                    subject_name="*.google.com",
                    san_list=[
                        "*.google.com",
                        "*.appengine.google.com",
                        "*.bdn.dev",
                        "*.origin-test.bdn.dev",
                        "*.cloud.google.com",
                        "*.crowdsource.google.com",
                        "*.datacompute.google.com",
                        "*.google.ca",
                        "*.google.cl",
                        "*.google.co.in",
                        "*.google.co.jp",
                        "*.google.co.uk",
                        "*.google.com.ar",
                        "*.google.com.au",
                        "*.google.com.br",
                        "*.google.com.co",
                        "*.google.com.mx",
                        "*.google.com.tr",
                        "*.google.com.vn",
                        "*.google.de",
                        "*.google.es",
                        "*.google.fr",
                    ],
                    issuer="GTS CA 1C3",
                    valid_from=cdp.network.TimeSinceEpoch(1700467375.0),
                    valid_to=cdp.network.TimeSinceEpoch(1707724974.0),
                    signed_certificate_timestamp_list=[],
                    certificate_transparency_compliance=cdp.network.CertificateTransparencyCompliance.UNKNOWN,
                    encrypted_client_hello=False,
                    key_exchange_group="X25519",
                    mac=None,
                    server_signature_algorithm=1027,
                ),
            ),
            type_=cdp.network.ResourceType.DOCUMENT,
            frame_id=cdp.page.FrameId("B3DCCB96E4F9C2FA162B31B3F219CE94"),
            has_user_gesture=False,
        ),
        cdp.network.RequestWillBeSentExtraInfo(
            request_id=cdp.network.RequestId("3A87DEB65CD78F73BE75481B813F000E"),
            associated_cookies=[],
            headers=cdp.network.Headers({
                ":authority": "www.youtube.com",
                ":method": "GET",
                ":path": "/"
            }),
            connect_timing=cdp.network.ConnectTiming(84600.783411),
            client_security_state=None,
            site_has_cookie_in_other_partition=False,
        ),
        cdp.network.ResponseReceivedExtraInfo(
            request_id=cdp.network.RequestId("3A87DEB65CD78F73BE75481B813F000E"),
            blocked_cookies=[],
            headers=cdp.network.Headers({
                "accept-ch": "Sec-CH-UA-Arch, Sec-CH-UA-Bitness, Sec-CH-UA-Full-Version, Sec-CH-UA-Full-Version-List, Sec-CH-UA-Model, Sec-CH-UA-WoW64, Sec-CH-UA-Form-Factor, Sec-CH-UA-Platform, Sec-CH-UA-Platform-Version",
                "alt-svc": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000",
                "cache-control": "no-cache, no-store, max-age=0, must-revalidate"
            }),
            resource_ip_address_space=cdp.network.IPAddressSpace.PUBLIC,
            status_code=200,
            headers_text=None,
            cookie_partition_key="https://youtube.com",
            cookie_partition_key_opaque=False,
        ),
        cdp.network.ResponseReceived(
            request_id=cdp.network.RequestId("3A87DEB65CD78F73BE75481B813F000E"),
            loader_id=cdp.network.LoaderId("3A87DEB65CD78F73BE75481B813F000E"),
            timestamp=cdp.network.MonotonicTime(84600.896929),
            type_=cdp.network.ResourceType.DOCUMENT,
            response=cdp.network.Response(
                url="https://www.youtube.com/",
                status=200,
                status_text="",
                headers=cdp.network.Headers({
                    "accept-ch": "Sec-CH-UA-Arch, Sec-CH-UA-Bitness, Sec-CH-UA-Full-Version, Sec-CH-UA-Full-Version-List, Sec-CH-UA-Model, Sec-CH-UA-WoW64, Sec-CH-UA-Form-Factor, Sec-CH-UA-Platform, Sec-CH-UA-Platform-Version",
                    "alt-svc": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000",
                    "cache-control": "no-cache, no-store, max-age=0, must-revalidate"
                }),
                mime_type="text/html",
                connection_reused=False,
                connection_id=0.0,
                encoded_data_length=-1.0,
                security_state=cdp.security.SecurityState.SECURE,

                #headers_text: typing.Optional[str] = None
                #request_headers: typing.Optional[Headers] = None
                remote_ip_address="",
                remote_port=0,
                from_disk_cache=False,
                from_service_worker=True,
                from_prefetch_cache=False,
                #service_worker_router_info: typing.Optional[ServiceWorkerRouterInfo] = None,
                #timing: typing.Optional[ResourceTiming] = None
                service_worker_response_source=cdp.network.ServiceWorkerResponseSource.NETWORK,
                response_time=cdp.network.TimeSinceEpoch(1705002946281.199),
                #cache_storage_cache_name: typing.Optional[str] = None
                protocol="h3",
                alternate_protocol_usage=cdp.network.AlternateProtocolUsage.ALTERNATIVE_JOB_WON_WITHOUT_RACE
                #security_details: typing.Optional[SecurityDetails] = None
            ),
            has_extra_info=False,
            frame_id=cdp.page.FrameId("B3DCCB96E4F9C2FA162B31B3F219CE94"),
        ),
        cdp.network.LoadingFinished(
            request_id=cdp.network.RequestId("3A87DEB65CD78F73BE75481B813F000E"),
            timestamp=cdp.network.MonotonicTime(84601.739592),
            encoded_data_length=0.0,
        ),
    ],
    response_bodies=[b""],
)

YOUTUBE_LAST_COMMUNICATION = HttpCommunication(
    request_id=cdp.network.RequestId("9060.176"),
    ignored=False,
    events=[
        cdp.network.RequestWillBeSent(
            request_id=cdp.network.RequestId("9060.176"),
            loader_id=cdp.network.LoaderId("3A87DEB65CD78F73BE75481B813F000E"),
            document_url="https://www.youtube.com/",
            request=cdp.network.Request(
                url="https://www.youtube.com/youtubei/v1/att/get?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false",
                method="POST",
                headers=cdp.network.Headers({
                    "Authorization": "SAPISIDHASH 1705002947_7846642d73ea512e75fa3c3cab12280f83e7ff7e",
                    "X-Origin": "https://www.youtube.com",
                    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\""
                }),
                initial_priority=cdp.network.ResourcePriority.HIGH,
                referrer_policy="strict-origin-when-cross-origin",

                post_data="{\"engagementType\":\"ENGAGEMENT_TYPE_UNBOUND\",\"context\":{}}",
                has_post_data=True,
                post_data_entries=[
                    cdp.network.PostDataEntry(
                        bytes_="eyJlbmdhZ2VtZW50VHlwZSI6IkVOR0FHRU1FTlRfVFlQRV9VTkJPVU5EIiwiY29udGV4dCI6e319",
                    ),
                ],
                mixed_content_type=cdp.security.MixedContentType.NONE,
                is_same_site=True,
            ),
            timestamp=cdp.network.MonotonicTime(84601.741052),
            wall_time=cdp.network.TimeSinceEpoch(1705002947.131719),
            initiator=cdp.network.Initiator(type_="script"),
            redirect_has_extra_info=False,
            redirect_response=None,
            type_=cdp.network.ResourceType.FETCH,
            frame_id=cdp.page.FrameId("B3DCCB96E4F9C2FA162B31B3F219CE94"),
            has_user_gesture=False,
        ),
        cdp.network.RequestWillBeSentExtraInfo(
            request_id=cdp.network.RequestId("9060.176"),
            associated_cookies=[],
            headers=cdp.network.Headers({
                ":authority": "www.youtube.com",
                ":method": "POST",
                ":path": "/youtubei/v1/att/get?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false"
            }),
            connect_timing=cdp.network.ConnectTiming(84601.743207),
            client_security_state=cdp.network.ClientSecurityState(
                initiator_is_secure_context=True,
                initiator_ip_address_space=cdp.network.IPAddressSpace.UNKNOWN,
                private_network_request_policy=cdp.network.PrivateNetworkRequestPolicy.ALLOW,
            ),
            site_has_cookie_in_other_partition=False,
        ),
    ],
)

# The values for events_youtube.json were calculated manually
@pytest.mark.parametrize(
    "events_file, comm_count, first_comm, last_comm", 
    [
        (
            "tests/events_youtube.json",
            33,
            YOUTUBE_FIRST_COMMUNICATION,
            YOUTUBE_LAST_COMMUNICATION,
        ),
    ],
)
@pytest.mark.asyncio
async def test_collect_communications(
        events_file, comm_count, first_comm, last_comm):
    """Tests the collect_communication function. Mocks the event listener and
    the CDP session with events read from file. Expects an amount of generated
    communications objects. Thoroughly verifies only the first and last
    communication."""
    with open(events_file, encoding="utf8") as f:
        events = json.load(f)

    event_mock = EventMock(events)
    urlfilter = UrlfilterMock()

    # Event mock acts both as an event iterator and CDP session
    # Keystr is not needed, we let it be an empty string
    # Function should exit before timeout. We just make sure it's big enough.
    communications = await collect_communications(event_mock, event_mock, urlfilter, "", timeout=10)

    assert len(communications) == comm_count
    assert communications[0] == first_comm
    assert communications[-1] == last_comm


@pytest.mark.parametrize(
    "events_file, actions_file", 
    [
        (
            "tests/events_youtube.json",
            "tests/actions_youtube.json",
        ),
    ],
)
@pytest.mark.asyncio
async def test_parse_communications_into_actions(events_file, actions_file):
    with open(events_file, encoding="utf8") as f:
        events = json.load(f)
    with open(actions_file, encoding="utf8") as f:
        expected_actions = json_actions_loads(f.read())

    event_mock = EventMock(events)
    urlfilter = UrlfilterMock()
    communications = await collect_communications(event_mock, 
        event_mock, urlfilter, "", timeout=10, collect_all=True)

    actions = parse_communications_into_actions(communications)

    for action in actions:
        replace_action_body_with_length(action)
    # actions = json.dumps(actions, cls=ActionsJSONEncoder, sort_keys=True, indent=4)

    assert actions == expected_actions

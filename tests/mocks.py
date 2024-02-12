from pycdp import cdp

class UrlfilterMock:
    def should_block(self, *args, **kwargs):
        return False


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

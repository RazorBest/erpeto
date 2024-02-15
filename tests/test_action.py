from cdprecorder.action import HttpAction
from cdprecorder.http_types import Cookie


class TestHttpAction:
    class DummyContainer():
        pass
        
    def test_update_info(self):
        action = HttpAction(
            body=b"dsa9d8sa",
            method="GET",
            cookies=[Cookie("old", "value")],
            status=301,
        )

        data = self.DummyContainer() 
        data.headers = {
            ":method": "GET",
            "CookiE": "test=a; B=c",
            "Val": "VAL2"
        }
        action.update_info(data)
        assert action.headers == {"val": "VAL2"}
        assert action.cookies == [Cookie("old", "value"), Cookie("test", "a"), Cookie("B", "c")]

        data = self.DummyContainer() 
        data.cookies = [Cookie("new", "2")]
        action.update_info(data)
        assert action.cookies == [Cookie("old", "value"), Cookie("test", "a"), Cookie("B", "c"), Cookie("new", "2")]

        data = self.DummyContainer() 
        data.url = "other"
        data.method = "POST"
        data.status = 404
        action.update_info(data)
        assert action.url == "other"
        assert action.method == "POST"
        assert action.status == 404

        data = self.DummyContainer() 
        data.method = "POST"
        data.status_code = 200
        action.update_info(data)
        assert action.status == 200

    def test_shallow_copy_from_action(self):
        action = HttpAction(
            body=b"dsa9d8sa",
            method="GET",
            cookies=[Cookie("old", "value")],
            headers={"a": "b"},
            status=301,
        )

        action2 = HttpAction()
        action2.shallow_copy_from_action(action)

        assert action2.method == action.method
        assert action2.headers == action.headers
        assert action2.url == action.url
        assert action2.body == action.body
        assert action2.cookies == action.cookies
        assert action2.status == action.status

        action2.headers["new"] = "c"
        action2.cookies.append(Cookie("other", ""))
        assert action2.headers == action.headers
        assert action2.cookies == action.cookies

    def test_cookies_to_dict(self):
        action = HttpAction(
            cookies=[Cookie("val1", "a"), Cookie("val2", "b")],
        )

        value = action.cookies_to_dict()
        assert value == {"val1": "a", "val2": "b"}

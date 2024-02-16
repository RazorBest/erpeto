from cdprecorder.util import DynamicRepr

class TestDynamicRepr:
    class InitDynamicRepr(DynamicRepr):
        def __init__(self, a, b, c, *, d, test=2, key="test", **kwargs):
            self.a = a
            self.b = b
            self.c = c
            self.d = d
            self.test = test
            self.key = key
            self.keyword = kwargs["keyword"]

    def test_repr(self):
        source = self.InitDynamicRepr(1, True, "dhsajk", d=8.3269, test=set(), keyword="new")
        value = repr(source)
        assert value == "InitDynamicRepr(a=1, b=True, c='dhsajk', d=8.3269, test=set(), key='test')"

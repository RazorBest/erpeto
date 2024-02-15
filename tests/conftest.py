class DummyDataSource:
    def __init__(self, value):
        self.value = value

    def get_value(self, prev_actions):
        return self.value

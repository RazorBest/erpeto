import requests

from adblockparser import AdblockRules

EASYLIST_URL = "https://easylist.to/easylist/easylist.txt"

class URLFilter(AdblockRules):
    def __init__(self) -> None:
        res = requests.get(EASYLIST_URL)
        res.raise_for_status()
        raw_rules = res.text.split("\n")
        super().__init__(raw_rules)

        with open("urlfilter", "wb") as f:
            import pickle
            pickle.dump(self, f)

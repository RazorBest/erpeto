"""
This module contains the URLFilter class, that supports adblock filters.
"""

import requests
from adblockparser import AdblockRules

EASYLIST_URL = "https://easylist.to/easylist/easylist.txt"


class URLFilter(AdblockRules):
    """Downloads a URL list, by default, the easylist.txt used by all
    adblockers."""

    def __init__(self) -> None:
        res = requests.get(EASYLIST_URL, timeout=10)
        res.raise_for_status()
        raw_rules = res.text.split("\n")
        super().__init__(raw_rules)

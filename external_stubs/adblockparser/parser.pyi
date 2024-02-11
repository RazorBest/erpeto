from _typeshed import Incomplete
from adblockparser.utils import split_data as split_data

class AdblockParsingError(ValueError): ...

class AdblockRule:
    BINARY_OPTIONS: Incomplete
    OPTIONS_SPLIT_PAT: Incomplete
    OPTIONS_SPLIT_RE: Incomplete
    raw_rule_text: Incomplete
    regex_re: Incomplete
    is_comment: Incomplete
    is_html_rule: bool
    is_exception: Incomplete
    raw_options: Incomplete
    options: Incomplete
    rule_text: Incomplete
    regex: str
    def __init__(self, rule_text) -> None: ...
    def match_url(self, url, options: Incomplete | None = None): ...
    def matching_supported(self, options: Incomplete | None = None): ...
    @classmethod
    def rule_to_regex(cls, rule): ...

class AdblockRules:
    supported_options: Incomplete
    uses_re2: Incomplete
    re2_max_mem: Incomplete
    rule_cls: Incomplete
    skip_unsupported_rules: Incomplete
    rules: Incomplete
    blacklist_re: Incomplete
    whitelist_re: Incomplete
    def __init__(self, rules, supported_options: Incomplete | None = None, skip_unsupported_rules: bool = True, use_re2: str = 'auto', max_mem=..., rule_cls=...) -> None: ...
    def should_block(self, url, options: Incomplete | None = None): ...

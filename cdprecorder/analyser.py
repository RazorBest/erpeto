import json
import re
import urllib.parse
from dataclasses import dataclass, field
from typing import Optional, Union, TypeVar, TYPE_CHECKING

import bs4
from bs4 import BeautifulSoup

from cdprecorder.action import (
    BrowserAction,
    HttpAction,
    InputAction,
    RequestAction,
    ResponseAction,
)
from cdprecorder.datasource import (
    BodySource,
    CookieSource,
    DataSource,
    InputSource,
    JSONFieldTarget,
    JSONContainer,
    QueryStringContainer,
    RegexSource,
    SubstrSource,
)
from cdprecorder.datatarget import (
    BodyTarget,
    CookieTarget,
    HeaderTarget,
    SingleSourcedTarget,
)
from cdprecorder.json_analyser import JSONSchema
from cdprecorder.http_types import (
    Cookie,
    parse_cookie,
)
from cdprecorder.str_evaluator import is_random

if TYPE_CHECKING:
    import bs4

    from cdprecorder.type_checking import HttpTarget


CONST_HEADERS = [
    "user-agent",
    "origin",
    "referer",
    "content-length",
    "sec-ch-ua-platform",
    "sec-ch-ua-mobile",
    "sec-ch-ua",
    "content-type",
    "accept",
    "x-requested-with",
]


def search_str_in_soup(soup: BeautifulSoup, text: str) -> Union[bs4.element.Tag, bs4.element.NavigableString, None]:
    def tag_contains_str(tag: bs4.Tag) -> bool:
        for key, val in tag.attrs.items():
            # Multi-valued attrs: https://beautiful-soup-4.readthedocs.io/en/latest/#multi-valued-attributes
            if isinstance(val, list):
                for elem in val:
                    if text in elem:
                        return True

            if text in val:
                return True

        if tag.string is not None and text in tag.string:
            return True

        return False

    return soup.find(tag_contains_str)


def find_context_html(data: str, text: str):
    soup = BeautifulSoup(data)
    tag = search_str_in_soup(soup, text)
    raise NotImplementedError


def find_context_bytes(data: bytes, text_to_find: bytes) -> Optional[bytes]:
    start = data.find(text_to_find)
    if start == -1:
        return None

    end = start + len(text_to_find)
    if len(data) < 50 or start < 6:
        if end - start == len(data):
            return b".*"

        return b"(?:.{" + str(start).encode() + b"}).{" + str(end - start).encode() + b"}"

    offset = 6
    while start >= offset:
        prefix = re.escape(data[start - offset : start])
        suffix = re.escape(data[end : end + offset])
        pattern = b"(?:" + prefix + b").{" + str(end - start).encode() + b"}(?:" + suffix + b")"
        matches = re.findall(pattern, data, flags=re.DOTALL | re.IGNORECASE)
        if len(matches) == 0:
            raise Exception
        if len(matches) == 1:
            break

        offset += 6

    return pattern


def find_context_str(data: str, text: str) -> Optional[str]:
    start = data.find(text)
    if start == -1:
        return None

    end = start + len(text)
    if len(data) < 50 or start < 6:
        if end - start == len(data):
            return ".*"

        return "(?:.{" + str(start) + "}).{" + str(end - start) + "}"

    prefix = re.escape(data[start - 6 : start])
    suffix = re.escape(data[end : end + 6])
    return "(?:" + prefix + ").{" + str(end - start) + "}(?:" + suffix + ")"


T = TypeVar("T", str, bytes)


def find_context(data: T, text: T, data_type: str = "str") -> Optional[T]:
    if data_type == "str":
        if not isinstance(data, str):
            raise Exception
        return find_context_str(data, text)
    if data_type == "bytes":
        if not isinstance(data, bytes):
            raise Exception
        return find_context_bytes(data, text)
    if data_type == "html":
        if not isinstance(data, str):
            raise Exception
        return find_context_html(data, text)

    return None


def greedy_check_if_attr_value(body: str, pos: int) -> bool:
    """Given an HTML body and a position check if the body ends in an HTML syntax that
    indicates that an attribute value follows (until pos), by looking backwards at the characters.
    """
    needs_equals = True
    needs_open_bracket = True
    is_attr_value_prefix = False
    for i in range(pos, -1, -1):
        if needs_equals:
            if body[i].isspace():
                continue
            elif body[i] == "=":
                needs_equals = False
            else:
                return False
        elif needs_open_bracket:
            if body[i] == "<":
                needs_open_bracket = False
                is_attr_value_prefix = True

    return is_attr_value_prefix


def greedy_html_match(body: str, text: str) -> tuple[str, str]:
    """
    Checks to see what HTML part does the given text come from. Doesn't parse the HTML. Only looks
    at the surrounding characters, and assumes an HTML syntax.

    Returns:
        - a tuple of the match_type and separator

    match_type can be:
        - "attribute" - the text is the value of an attribute
        - empty string - the text didn't match
    """
    idx = body.find(text)
    if idx == -1:
        return "", ""

    str_separator = ""
    if body[idx - 1] == '"' and body[idx + len(text)] == '"':
        str_separator = '"'
    if body[idx - 1] == "'" and body[idx + len(text)] == "'":
        str_separator = "'"

    if greedy_check_if_attr_value(body, idx - len(str_separator) - 1):
        return "attribute", str_separator

    return "", ""


def build_regex_based_on_selected_attributes(
    tag_name: str,
    prev_attrs: list,
    after_attrs: list,
    attr_name: str,
    value_pattern: str,
) -> str:
    prev_attr_pattern = ""
    for name, _, is_used in prev_attrs:
        if not is_used:
            continue
        prev_attr_pattern += rf"{re.escape(name)}[^>]+"

    after_attr_pattern = ""
    for name, _, is_used in after_attrs:
        if not is_used:
            continue
        after_attr_pattern += rf"[^>]+{re.escape(name)}"

    tag_pattern = rf"<{re.escape(tag_name)}"
    spaced_equal = r"[\s]*=[\s]*"
    if len(after_attr_pattern) > 0:
        attr_pattern = rf"{tag_pattern}[^>]+{prev_attr_pattern}{re.escape(attr_name)}{spaced_equal}{value_pattern}{after_attr_pattern}"
    else:
        attr_pattern = rf"{tag_pattern}[^>]+{prev_attr_pattern}{re.escape(attr_name)}{spaced_equal}{value_pattern}"

    return attr_pattern


class HTMLNodeFixedMatcher:
    def __init__(self, name: str, attrs: list[str]):
        self.name = name
        self.attrs = attrs

    def tag_matches_args(self, tag: bs4.Tag) -> bool:
        if len(self.attrs) != len(tag.attrs):
            return False
        idx = 0
        for attr1, attr2 in zip(self.attrs, tag.attrs):
            if attr1 != attr2:
                return False

        return True

    def tag_matches(self, tag: bs4.Tag) -> bool:
        return tag.name == self.name and self.tag_matches_args(tag)


class HTMLNodeMatcher:
    def __init__(self, name: str, attrs: list[str]):
        self.name = name
        self.attrs = attrs

    def tag_matches_args(self, tag: bs4.Tag) -> bool:
        idx = 0
        # Check if the attributes are in order
        for name in tag.attrs:
            if idx >= len(self.attrs):
                break
            if name == self.attrs[idx]:
                idx += 1

        # Not all attributes were found in the desired order
        return idx >= len(self.attrs)

    def tag_matches(self, tag: bs4.Tag) -> bool:
        return tag.name == self.name and self.tag_matches_args(tag)

    def build_regex(self) -> str:
        attr_pattern = r""
        for name in self.attrs:
            attr_pattern += rf"{re.escape(name)}[^>]*"

        return rf"<{re.escape(self.name)}[^>]*{attr_pattern}>"


@dataclass
class AttrMatcher:
    name: str
    active: bool = True


@dataclass
class HTMLAttrValuePattern:
    tag_name: str
    attr_name: str
    pre_attrs: list[AttrMatcher] = field(default_factory=list)
    post_attrs: list[AttrMatcher] = field(default_factory=list)
    pre_nodes: list[HTMLNodeMatcher] = field(default_factory=list)
    post_nodes: list[HTMLNodeMatcher] = field(default_factory=list)

    def set_active_attr(self, name: str, active: bool) -> None:
        found = False

        for matcher in self.pre_attrs + self.post_attrs:
            if matcher.name == name:
                matcher.active = active
                found = True

        if not found:
            raise ValueError(f"No attribute with name {name}")

    def activate_attr(self, name: str) -> None:
        self.set_active_attr(name, True)

    def deactivate_attr(self, name: str) -> None:
        self.set_active_attr(name, False)

    def activate_all_attr(self) -> None:
        for matcher in self.pre_attrs + self.post_attrs:
            self.activate_attr(matcher.name)

    def deactivate_all_attr(self) -> None:
        for matcher in self.pre_attrs + self.post_attrs:
            self.deactivate_attr(matcher.name)

    def match_soup(self, soup: BeautifulSoup) -> list[bs4.Tag]:
        matched_nodes = []

        all_attrs = self.pre_attrs + [AttrMatcher(self.attr_name, True)] + self.post_attrs
        all_attr_names = [attr.name for attr in all_attrs]
        attr_finder = {name: True for name in all_attr_names}
        nodes = soup.find_all(self.tag_name, attrs=attr_finder)
        own_tag = HTMLNodeMatcher(self.tag_name, all_attr_names)
        for node in nodes:
            if not own_tag.tag_matches(node):
                continue

            success = True

            for prev_node in self.pre_nodes:
                for candidate in node.previous_elements:
                    if not isinstance(candidate, bs4.Tag):
                        continue
                    if not prev_node.tag_matches(candidate):
                        success = False

            if not success:
                continue

            for next_node in self.post_nodes:
                for candidate in node.next_elements:
                    if not isinstance(candidate, bs4.Tag):
                        continue
                    if not next_node.tag_matches(candidate):
                        success = False

            if not success:
                continue

            matched_nodes.append(node)

        return matched_nodes

    def build_regex(self, value_pattern: str) -> str:
        prev_attr_pattern = ""
        for attr in self.pre_attrs:
            if not attr.active:
                continue
            prev_attr_pattern += rf"{re.escape(attr.name)}[^>]+"

        after_attr_pattern = ""
        for attr in self.post_attrs:
            if not attr.active:
                continue
            after_attr_pattern += rf"[^>]+{re.escape(attr.name)}"

        previous_tags_pattern = r""
        for node in self.pre_nodes:
            previous_tags_pattern += node.build_regex() + ".*?"

        next_tags_pattern = r""
        for node in self.post_nodes:
            next_tags_pattern += ".*?" + node.build_regex()

        tag_pattern = rf"<{re.escape(self.tag_name)}"
        spaced_equal = r"[\s]*=[\s]*"
        attr_pattern = rf"{tag_pattern}[^>]+{prev_attr_pattern}{re.escape(self.attr_name)}{spaced_equal}{value_pattern}{after_attr_pattern}"

        pattern = rf"{previous_tags_pattern}{attr_pattern}{next_tags_pattern}"

        return pattern


def html_attr_value_pattern_from_tag(tag: bs4.Tag, attr_name: str) -> HTMLAttrValuePattern:
    attrs = list(tag.attrs.items())
    pos_of_attr_name = -1
    for idx, (k, v) in enumerate(attrs):
        if k == attr_name:
            pos_of_attr_name = idx
            break

    if pos_of_attr_name == -1:
        raise ValueError("Attribute name not found")

    # Assume tag.attrs keeps the order in the HTML
    # Get the attributes that are defined before `attr_name`
    pre_attr_matchers = [AttrMatcher(k, True) for k, _ in attrs[:pos_of_attr_name]]
    # Get the attributes that are defined after `attr_name`
    post_attr_matchers = [AttrMatcher(k, True) for k, _ in attrs[pos_of_attr_name + 1 :]]

    return HTMLAttrValuePattern(
        tag_name=tag.name,
        attr_name=attr_name,
        pre_attrs=pre_attr_matchers,
        post_attrs=post_attr_matchers,
    )


'''
def activate_necessary_attributes(template: HTMLAttrValuePattern, matched_nodes: list[bs4.BeautifulSoup]) -> None:
    """Activates the necessary attributes in the HTML pattern in order to match only one node from the given list.
    Uses shortest uncommon subsenquence."""
    if len(matched_nodes) == 0:
        return

    match_mask = [1 if attr.active else 0 for attr in template.pre_attrs]
    match_mask += [1] # Mask for the attribute represented by template.attr_name, which is always active
    match_mask += [1 if attr.active else 0 for attr in template.post_attrs]
    others_mask = [0] * (len(template.pre_attrs) + 1 len(template.post_attrs))
    all_attr = template.pre_attrs + [AttrMatcher(template.attr_name, True)] + template.post_attrs
    active_attr = [attr for attr in all_attr if attr.active]
    for node in matched_nodes:
        idx = 0

        for name in node.attrs:
            if name == all_attr[idx].name:
                idx += 1
                if idx >= len(all_attr):
                    break

        for attr in template.pre_attrs:
            if node.
'''


def get_soup_root(element: bs4.Tag) -> bs4.BeautifulSoup:
    while element.parent is not None:
        element = element.parent

    if not isinstance(element, BeautifulSoup):
        raise ValueError("Soup is not in propper form. Root must be of type BeautifulSoup.")

    return element


def build_unique_regex_attr_val(html: str, tag: bs4.Tag, attr_name: str, separator: str) -> Optional[str]:
    """Builds a regex that selects the attribute value in the HTML from wich the tag comes from."""
    attr_value = tag.attrs[attr_name]
    # lines = html.split("\n")

    if separator != "":
        value_pattern = rf"{separator}([^{separator}]*?){separator}"
    else:
        value_pattern = r"([^\s>]*?)"

    template = html_attr_value_pattern_from_tag(tag, attr_name)
    template.deactivate_all_attr()

    attr_pattern = template.build_regex(value_pattern)
    found = re.findall(attr_pattern, html, flags=re.DOTALL | re.IGNORECASE)
    if len(found) == 1:
        return attr_pattern

    attr_names = [attr.name for attr in template.pre_attrs + template.post_attrs]

    found_unique_regex = False

    active_attrs = []
    # Starting using the previous attributes, starting from the one with the longest name
    for new_name in attr_names:
        # TODO: What if there are multiple attributes with the same name?
        template.activate_attr(new_name)

        active_attrs.append(new_name)

        attr_pattern = template.build_regex(value_pattern)

        found = re.findall(attr_pattern, html, flags=re.DOTALL | re.IGNORECASE)
        if len(found) == 1:
            found_unique_regex = True
            break

        if len(found) == 0:
            import pdb

            pdb.set_trace()

    if not found_unique_regex:
        for pre_node, post_node in zip(tag.previous_elements, tag.next_elements):
            if not isinstance(pre_node, bs4.element.Tag):
                continue

            node_attr_names = list(pre_node.attrs)
            matcher = HTMLNodeMatcher(pre_node.name, node_attr_names)
            template.pre_nodes.insert(0, matcher)
            attr_pattern = template.build_regex(value_pattern)

            found = re.findall(attr_pattern, html, flags=re.DOTALL | re.IGNORECASE)
            if len(found) == 1 and found[0] == attr_value:
                found_unique_regex = True
                break

            if len(found) == 0:
                import pdb

                pdb.set_trace()

            if not isinstance(post_node, bs4.element.Tag):
                continue

            node_attr_names = list(post_node.attrs)
            matcher = HTMLNodeMatcher(post_node.name, node_attr_names)
            template.post_nodes.append(matcher)
            attr_pattern = template.build_regex(value_pattern)

            print(f"Checking {attr_pattern!r}")
            found = re.findall(attr_pattern, html, flags=re.DOTALL | re.IGNORECASE)
            if len(found) == 1 and found[0] == attr_value:
                found_unique_regex = True
                break

            if len(found) == 0:
                import pdb

                pdb.set_trace()

        # TODO: look at the next_elements of the tag

        if not found_unique_regex:
            return None

    for name in active_attrs:
        template.deactivate_attr(name)
        attr_pattern = template.build_regex(value_pattern)
        found = re.findall(attr_pattern, html, flags=re.DOTALL | re.IGNORECASE)
        if len(found) != 1 or found[0] != attr_value:
            template.activate_attr(name)

    attr_pattern = template.build_regex(value_pattern)

    return attr_pattern


def find_source_of_str_in_body(body: str, text: str) -> Optional[str]:
    """Receives a text that is a substring of the HTML body. Finds a relevant regex that selects that
    substring."""
    match_type, separator = greedy_html_match(body, text)

    def has_attr_val(tag: bs4.Tag) -> bool:
        return text in tag.attrs.values()

    if match_type == "attribute":
        soup = BeautifulSoup(body, features="html.parser")
        found_tag = soup.find(has_attr_val)
        if found_tag is not None and isinstance(found_tag, bs4.Tag):
            attr_name = None
            for k, v in found_tag.attrs.items():
                if v == text:
                    attr_name = k
                    break

            if attr_name is not None:
                pattern = build_unique_regex_attr_val(body, found_tag, attr_name, separator)
                return pattern

    return None


def look_for_str_in_response(
    text: str,
    action: ResponseAction,
) -> Optional[DataSource]:
    text_bin = text.encode()

    if action.body and action.body.find(text_bin) != -1:
        pattern = find_source_of_str_in_body(action.body.decode("utf8"), text)
        if pattern is not None:
            return RegexSource(BodySource(action.ID), pattern, default=text)

    for key, value in action.headers.items():
        escaped_value = value
        if key.lower() == "set-cookie":
            escaped_value = urllib.parse.unquote(value)

        source = None

        if text in escaped_value:
            if key.lower() == "set-cookie":
                values = value.split("\n")
                cookies = [parse_cookie(val) for val in values]
                for cookie in cookies:
                    if text in cookie.value:
                        start = cookie.value.find(text)
                        end = start + len(text)
                        if end - start == len(cookie.value):
                            strcontext = ".*"
                        else:
                            strcontext = "(?:.{" + str(start) + "}).{" + str(end - start) + "}"

                        # match = re.match(strcontext, cookie.value)

                        source = CookieSource(action.ID, cookie.name, strcontext)
                        break

                return source
            else:
                pass
                """
                start = escaped_value.find(text)
                end = start + len(text)
                if end - start == len(escaped_value):
                    strcontext = ".*"
                else:
                    strcontext = "(?:.{" + str(start) + "}).{" + str(end - start) + "}"
                source = HeaderSource(index, key.lower(), strcontext)

                return source
                """
    return None


def look_for_str_in_input_action(text: str, action: InputAction) -> Optional[DataSource]:
    if action.text in text:
        start = text.find(action.text)
        end = start + len(action.text)

        src1 = InputSource(action.text)
        src2 = SubstrSource(src1, start, end)

        return src2

    return None


def look_for_str_in_actions(
    text: str,
    actions: list[HttpAction],
) -> Optional[DataSource]:
    """Takes a string and looks for it through the actions present in the actions."""
    for action in actions[::-1]:
        source = None
        if isinstance(action, ResponseAction):
            source = look_for_str_in_response(text, action)
        elif isinstance(action, InputAction):
            source = look_for_str_in_input_action(text, action)

        if source is not None:
            return source

    return None


def look_for_str_in_last_source_actions(text: str, actions: list[HttpAction], limit: int = 10) -> Optional[DataSource]:
    """Receives a string and looks for it through the last actions present in the actions, up to the
    given limit."""
    actions_checked = 0
    for action in actions[::-1]:
        source = None
        if isinstance(action, ResponseAction):
            source = look_for_str_in_response(text, action)
            actions_checked += 1
        elif isinstance(action, InputAction):
            source = look_for_str_in_input_action(text, action)
            actions_checked += 1

        if source is not None:
            return source

        if actions_checked >= limit:
            break

    return None


def search_for_header(actions: list, key: str, value: str) -> list[SingleSourcedTarget]:
    """Looks for actions that might generate the given header key and value. In the case of
    success, returns the header generator."""
    if key.lower() in CONST_HEADERS:
        return []

    if is_random(value):
        source = look_for_str_in_actions(value, actions)
        if source:
            target: HttpTarget = HeaderTarget(source, key, value)
            print(f"Found {source.__class__.__name__} for {target.__class__.__name__}")

            return [target]

    return []


def search_for_cookie(actions: list, cookie: Cookie) -> list[SingleSourcedTarget]:
    """Looks for actions that might generate the given cookie. In the case of
    success, returns the cookie generator."""
    if not cookie.value:
        return []
    if is_random(cookie.value):
        if source := look_for_str_in_actions(cookie.value, actions):
            target = CookieTarget(cookie.name, source)
            print(f"Found {source.__class__.__name__} for {target.__class__.__name__}")
            return [target]

    return []


def search_for_json(actions: list, schema: JSONSchema) -> list[SingleSourcedTarget]:
    has_sources = False
    json_targets = []
    for field in schema.fields:
        source = look_for_str_in_actions(field.value, actions)
        if source:
            json_targets.append(JSONFieldTarget(source, field.path))
            has_sources = True

    targets: list[SingleSourcedTarget] = []
    if has_sources:
        container = JSONContainer(schema, json_targets)
        targets.append(BodyTarget(container))
        print(f"Found {container.__class__.__name__} for BodyTarget")

    return targets


def search_for_query_string(actions: list, query_list: list[tuple[str, str]]) -> list[SingleSourcedTarget]:
    new_qlist: list[tuple[Union[str, DataSource], Union[str, DataSource]]] = []
    has_sources = False
    print(f"Queriy list: {query_list}")
    for name, value in query_list:
        found_name: Union[str, DataSource] = name
        found_value: Union[str, DataSource] = value

        if is_random(value):
            print(f"Searching qs param: {value} with name {name}")
            source = look_for_str_in_actions(value, actions)
            if source:
                has_sources = True
                found_value = source
        # look only at the previous response
        elif len(value) > 3:
            print(f"Searching qs param in last source: {value}")
            source = look_for_str_in_last_source_actions(value, actions)
            if source:
                has_sources = True
                found_value = source

        if is_random(name):
            print(f"Searching qs param name: {name}")
            source = look_for_str_in_actions(name, actions)
            if source:
                has_sources = True
                found_name = source
        elif len(name) > 3:
            print(f"Searching qs param name in last source: {name}")
            source = look_for_str_in_last_source_actions(name, actions)
            if source:
                has_sources = True
                found_name = source

        new_qlist.append((found_name, found_value))

    if has_sources:
        return [BodyTarget(QueryStringContainer(new_qlist))]

    return []


def analyse_actions(actions: list[BrowserAction]) -> None:
    for action_idx, action in enumerate(actions):
        if isinstance(action, RequestAction):
            for key, value in action.headers.items():
                targets = search_for_header(actions[:action_idx], key, value)
                action.targets.extend(targets)

            for cookie in action.cookies:
                targets = search_for_cookie(actions[:action_idx], cookie)
                action.targets.extend(targets)

            if action.body:
                body_bytes = action.body
                body = body_bytes.decode("utf8")
                try:
                    json.loads(body)
                    schema = JSONSchema(body)
                    targets = search_for_json(actions[:action_idx], schema)
                    action.targets.extend(targets)
                except json.JSONDecodeError:
                    pass

                # try:
                query_list = urllib.parse.parse_qsl(body, strict_parsing=True, keep_blank_values=True)
                targets = search_for_query_string(actions[:action_idx], query_list)
                action.targets.extend(targets)
                # except ValueError:
                #    pass

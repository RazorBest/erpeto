from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable, Optional, Union

from .datasource import DataSource
from .str_evaluator import randomness_score


@dataclass(frozen=True, eq=False)
class JSONField:
    value: str
    path: list[Union[str, int]]
    source: Optional[DataSource] = None


class JSONSchema:
    def __init__(self, data: str, token_classifier: Optional[Callable[[str], bool]] = None):
        self.data = json.loads(data)

        if token_classifier is not None:
            self.classifier = token_classifier
        else:
            self.classifier = lambda token: randomness_score(token) >= 50

        self.fields: list[JSONField] = []
        self.classify_tokens()

    def _classify(self, data: object, path: list[Union[str, int]]) -> list[JSONField]:
        fields = []
        if isinstance(data, dict):
            for key, val in data.items():
                fields += self._classify(val, path + [key])
        elif isinstance(data, list):
            for index, val in enumerate(data):
                fields += self._classify(val, path + [index])
        elif isinstance(data, str):
            if self.classifier(data):
                field = JSONField(data, path)
                fields.append(field)
        # TODO: decide for int, bool, bytes etc

        return fields

    def classify_tokens(self) -> None:
        self.fields = self._classify(self.data, [])

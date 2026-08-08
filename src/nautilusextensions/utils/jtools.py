from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Union, cast

import yaml


class JsonNode:
    def __init__(self, data: Any):
        self._data = data

    def __getattr__(self, name: str) -> Any:
        if isinstance(self._data, dict) and name in self._data:
            return self._wrap(self._data[name])
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

    def __getitem__(self, key: Any) -> Any:
        if isinstance(self._data, dict):
            return self._wrap(self._data[key])
        if isinstance(self._data, list):
            return self._wrap(self._data[key])
        raise TypeError(f"'{type(self).__name__}' object is not subscriptable")

    def __contains__(self, key: Any) -> bool:
        return isinstance(self._data, dict) and key in self._data

    def __iter__(self):
        if isinstance(self._data, list):
            return (self._wrap(x) for x in self._data)
        if isinstance(self._data, dict):
            return iter(self._data)
        raise TypeError(f"'{type(self).__name__}' object is not iterable")

    def __len__(self) -> int:
        if isinstance(self._data, (dict, list)):
            return len(self._data)
        return 0

    def __repr__(self) -> str:
        return f"JsonNode({self._data!r})"

    def get(self, key: str, default: Any = None) -> Any:
        if isinstance(self._data, dict):
            return self._wrap(self._data.get(key, default))
        return default

    def keys(self):
        if isinstance(self._data, dict):
            return self._data.keys()
        return ()

    def values(self):
        if isinstance(self._data, dict):
            return (self._wrap(v) for v in self._data.values())
        return ()

    def items(self):
        if isinstance(self._data, dict):
            return ((k, self._wrap(v)) for k, v in self._data.items())
        return ()

    def to_dict(self) -> Any:
        return self._unwrap(self._data)

    @classmethod
    def _wrap(cls, value: Any) -> Any:
        if isinstance(value, (dict, list)):
            return cls(value)
        return value

    @classmethod
    def _unwrap(cls, value: Any) -> Any:
        if isinstance(value, JsonNode):
            value = value._data

        if isinstance(value, dict):
            return {k: cls._unwrap(v) for k, v in value.items()}

        if isinstance(value, list):
            return [cls._unwrap(v) for v in value]

        return value


class JsonRegistry:
    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)
        self._tables: Dict[str, JsonNode] = {}
        self._paths: Dict[str, Path] = {}

    def load(self, file_name: str, alias: Optional[str] = None) -> JsonNode:
        path = self.base_dir / file_name
        if not path.exists():
            raise FileNotFoundError(f"JSON file not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        node = JsonNode(data)
        table_name = alias or path.stem

        self._tables[table_name] = node
        self._paths[table_name] = path
        setattr(self, table_name, node)

        return node

    def load_many(
        self, files: Union[Mapping[str, str], Iterable[tuple[str, Optional[str]]]]
    ) -> Dict[str, JsonNode]:
        loaded: Dict[str, JsonNode] = {}

        if isinstance(files, Mapping):
            files = cast(Mapping[str, str], files)

            for alias, file_name in files.items():
                loaded[alias] = self.load(file_name, alias=alias)
            return loaded

        for item in files:
            file_name, alias = item
            node = self.load(file_name, alias=alias)
            table_name = alias or Path(file_name).stem
            loaded[table_name] = node

        return loaded

    def reload(self, alias: str) -> JsonNode:
        if alias not in self._paths:
            raise KeyError(f"Table '{alias}' is not loaded")

        path = self._paths[alias]
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        node = JsonNode(data)
        self._tables[alias] = node
        setattr(self, alias, node)
        return node

    def unload(self, alias: str) -> None:
        if alias in self._tables:
            self._tables.pop(alias, None)
            self._paths.pop(alias, None)
            if hasattr(self, alias):
                delattr(self, alias)

    def clear(self) -> None:
        for alias in list(self._tables.keys()):
            self.unload(alias)

    def get(self, alias: str, default: Any = None) -> Any:
        return self._tables.get(alias, default)

    def has(self, alias: str) -> bool:
        return alias in self._tables

    def list_tables(self) -> list[str]:
        return list(self._tables.keys())

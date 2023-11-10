import json
import os


class Cache:
    def __init__(self, path):
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump({}, f)

        self.path = path
        self.data = self.load()

    def load(self) -> dict[str, list[str]]:
        with open(self.path) as f:
            return json.load(f)

    def write(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def add(self, key: str, value: str) -> None:
        self.data[key] = self.data.get(key, [])
        self.data[key].append(value)

    def is_cached(self, value: str) -> bool:
        return any(value in values for values in self.data.values())

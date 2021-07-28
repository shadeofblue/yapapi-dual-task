from typing import Optional


class Singleton:
    _instance: Optional["Singleton"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance:
            return cls._instance
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        if self._instance:
            return

        type(self)._instance = self

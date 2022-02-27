import typing
from collections.abc import Callable
from interface import implements, Interface

class CommandInterface(Interface):
    @property
    def method(self) -> Callable:
        pass

    def execute(self, instance: typing.Any) -> typing.Any:
        pass

class Command(implements(CommandInterface)):
    @property
    def method(self) -> Callable:
        return self._method

    def __init__(self, method):
        self._method = method

    def execute(self, instance: typing.Any) -> typing.Any:
        return self.method(instance)

import typing
from interface import Interface, implements

class CreatorInterface(Interface):
    def create(self, init_data: typing.Any=None):
        pass

class FactoryInterface(Interface):
    @property
    def creators(self) -> typing.Dict[str, CreatorInterface]:
        pass

    def register_creator(self, identifier: str, creator_class: CreatorInterface) -> bool:
        pass

    def get_creators(self) -> typing.List[str]:
        pass

    def create(self, identifier: str, init_data: typing.Any=None) -> typing.Any:
        pass

class Factory(implements(FactoryInterface)):
    @property
    def creators(self) -> typing.Dict[str, CreatorInterface]:
        return self._creators

    def __init__(self):
        self._creators = {}

    def register_creator(self, identifier: str, creator_class: CreatorInterface) -> bool:
        if identifier in self.creators:
            return False

        self.creators[identifier] = creator_class();
        return True

    def get_creators(self) -> typing.List[str]:
        return self.creators.keys()

    def create(self, identifier: str, init_data: typing.Any=None) -> typing.Any:
        return self.creators[identifier].create(init_data)

class Creator(implements(CreatorInterface)):
    def create(self, init_data: typing.Any=None):
        raise("Error. 'create()' method must be implemented.")
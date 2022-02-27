import typing
from interface import Interface, implements
from utils.visitor import VisitorReceiverInterface, VisitorInterface

class ChainOfResponsabilitiesInterface(Interface):
    @property
    def instances(self) -> typing.List[VisitorReceiverInterface]:
        pass

    @property
    def visitor(self) -> VisitorInterface:
        pass

    def append(self, instance: VisitorReceiverInterface):
        pass

    def handle(self) -> typing.Any:
        pass

class ChainOfResponsabilities(implements(ChainOfResponsabilitiesInterface)):
    @property
    def instances(self) -> typing.List[VisitorReceiverInterface]:
        return self._instances

    @property
    def visitor(self) -> VisitorInterface:
        return self._visitor

    def __init__(self, visitor: VisitorInterface):
        self._instances = []
        self._visitor = visitor

    def append(self, instance: VisitorReceiverInterface):
        self.instances.append(instance)

    def handle(self) -> typing.Any:
        return self.traverse()

    def traverse(self) -> typing.Any:
        i = 0
        while True:
            result = self.visitor.visit(self.instances[i])
            if result != False:
                return result
            else:
                if i < len(self.instances)-1:
                    i += 1
                else:
                    return False

from interface import Interface, implements

class IteratorInterface(Interface):
    def append(self, instance):
        pass

    def is_next(self):
        pass

    def next(self):
        pass

    def traverse(self, visitor):
        pass

class Iterator(implements(IteratorInterface)):
    def __init__(self):
        self.index = -1
        self.instances = []

    def append(self, instance):
        self.instances.append(instance)

    def is_next(self):
        if self.index < len(self.instances)-1:
            return True
        else:
            return False

    def next(self):
        if self.is_next():
            self.index = self.index + 1
            return self.instances[self.index]
        else:
            return False

    def traverse(self, visitor):
        results = []
        for instance in self.instances:
            results.append(visitor.visit(instance))

        return results

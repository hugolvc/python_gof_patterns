"""
This module implements a general porpouse *Composite* pattern.
"""

import typing
import copy
from interface import implements, Interface
from utils.visitor import VisitorInterface, VisitorReceiverInterface
from utils.iterator import Iterator, IteratorInterface

class CompositeInterface(Interface):
    """
    Defines the interface for composite nodes
    """

    @property
    def definer(self) -> VisitorReceiverInterface:
        pass

    @property
    def name(self) -> str:
        return self._name

    @property
    def children(self) -> typing.List['CompositeInterface']:
        pass

    @property
    def parent(self) -> 'CompositeInterface':
        pass

    def add_child(self, definer: typing.Any) -> 'CompositeInterface':
        pass

    def get_child(self, name: str) -> 'CompositeInterface':
        pass

    def get_breadcrumbs_to(self) -> str:
        pass

    def get_all_breadcrumbs_from(self) -> typing.List[str]:
        pass

    def get_leaves(self) -> typing.List['CompositeInterface']:
        pass

    def get_root(self) -> 'CompositeInterface':
        pass

    def get_path_to(self) -> IteratorInterface:
        pass

    def get_nodes_to(self) -> typing.List['CompositeInterface']:
        pass

    def traverse_from(self, visitor: VisitorInterface) -> typing.Any:
        pass

    def branch(self) -> 'CompositeInterface':
        pass

    def get_node_from_breadcrumbs(self, breadcrumbs: str) -> 'CompositeInterface':
        pass

class CompositeNode(implements(CompositeInterface, VisitorReceiverInterface)):
    """
    Implements the *Composite*
    """

    @property
    def definer(self) -> VisitorReceiverInterface:
        return self._definer

    @property
    def name(self) -> str:
        return self._name

    @property
    def children(self) -> typing.List[CompositeInterface]:
        return self._children

    @property
    def parent(self) -> CompositeInterface:
        return self._parent

    @parent.setter
    def parent(self, value: CompositeInterface):
        self._parent = value

    def __init__(self, definer):
        self._definer = definer

        if self._definer.__class__.__name__ == 'dict':
            if 'name' in self._definer:
                self._name = str(definer['name'])
            else:
                self._name = str(list(self._definer.values())[0])
        else:
            self._name = str(self._definer)
        
        self._children = []
        self._parent = None

    def __str__(self):
        if self.definer.__class__.__name__ == 'dict':
            if 'name' in self.definer:
                return self.definer['name']
            else:
                return list(self.definer.values())[0]
        else:
            return str(self.definer)

    def add_child(self, definer: typing.Any) -> CompositeInterface:
        new_node = CompositeNode(definer)
        new_node.parent = self
        self.children.append(new_node)

        return new_node

    def get_child(self, name: str) -> CompositeInterface:
        child_to_return = next(child for child in self.children if child.name == name)

        return child_to_return

    def get_breadcrumbs_to(self) -> str:
        if self.parent:
            parent_breadcrumbs = self.parent.get_breadcrumbs_to()
            return parent_breadcrumbs + '/' + self.name
        else:
            return self.name

    def get_all_breadcrumbs_from(self) -> typing.List[str]:
        if self.children:
            breadcrumbs = []
            for child in self.children:
                child_breadcrumbs = child.get_all_breadcrumbs_from()
                for child_breadcrumb in child_breadcrumbs:
                    breadcrumbs.append(self.name + '/' + child_breadcrumb)

            return breadcrumbs
        else:
            return [self.name,]

    def get_leaves(self) -> typing.List[CompositeInterface]:
        if self.children:
            leaves = []
            for child in self.children:
                child_leaves = child.get_leaves()
                leaves = leaves + child_leaves

            return leaves
        else:
            return [self,]

    def get_root(self) -> CompositeInterface:
        if self.parent:
            return self.parent.get_root()
        else:
            return self

    def get_path_to(self) -> IteratorInterface:
        iterator = Iterator()
        nodes = self.get_nodes_to()

        for node in nodes:
            iterator.append(node)

        return iterator

    def get_nodes_to(self) -> typing.List[CompositeInterface]:
        if self.parent:
            nodes = self.parent.get_nodes_to()
            nodes.append(self)

            return nodes
        else:
            return [self,]

    def accept_visit(self, visitor: 'VisitorInterface') -> typing.Any:
        return visitor.execute(self)

    def traverse_from(self, visitor: VisitorInterface) -> typing.Any:
        return self._traverse(visitor)

    def _traverse(self, visitor: VisitorInterface) -> typing.Any:
        result = []
        result.append(visitor.visit(self))

        for child in self.children:
            result.append(child._traverse(visitor))

        return result

    def branch(self) -> CompositeInterface:
        new_root = copy.deepcopy(self)
        new_root.parent = None

        return new_root

    def get_node_from_breadcrumbs(self, breadcrumbs: str) -> CompositeInterface:
        names = breadcrumbs.split('/')
        if names[0] == self.name:
            names.pop(0)

        return self._get_node_from_breadcrumbs(names)

    def _get_node_from_breadcrumbs(self, names: typing.List[str]) -> CompositeInterface:
        name = names.pop(0)
        next_node = next((child for child in self.children if child.name == name), None)

        if not next_node:
            return None

        if names:
            return next_node._get_node_from_breadcrumbs(names)
        else:
            return next_node

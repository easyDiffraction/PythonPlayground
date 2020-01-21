from typing import Union, Any, NoReturn, List
from collections import UserDict

from PySide2.QtWidgets import QUndoStack, QUndoCommand


class _EmptyCommand(QUndoCommand):
    """
    The _EmptyCommand class is the custom base class of all undoable commands
    stored on a QUndoStack.
    """

    def __init__(self, dictionary: 'UndoableDict', key: Union[str, list], value: Any):
        QUndoCommand.__init__(self)
        self._dictionary = dictionary
        self._key = key
        self._new_value = value
        self._old_value = dictionary.getItem(key)


class _AddItemCommand(_EmptyCommand):
    """
    The _AddItemCommand class implements a command to add a key-value pair to
    the UndoableDict-based dictionary.
    """

    def __init__(self, dictionary: 'UndoableDict', key: Union[str, list], value: Any):
        super().__init__(dictionary, key, value)
        self.setText("Adding: {} = {}".format(self._key, self._new_value))

    def undo(self) -> NoReturn:
        self._dictionary._realDelItem(self._key)

    def redo(self) -> NoReturn:
        self._dictionary._realAddItem(self._key, self._new_value)


class _SetItemCommand(_EmptyCommand):
    """
    The _SetItemCommand class implements a command to modify the value of
    the existing key in the UndoableDict-based dictionary.
    """

    def __init__(self, dictionary: 'UndoableDict', key: Union[str, list], value: Any):
        super().__init__(dictionary, key, value)
        self.setText("Setting: {} = {}".format(self._key, self._new_value))

    def undo(self) -> NoReturn:
        self._dictionary._realSetItem(self._key, self._old_value)

    def redo(self) -> NoReturn:
        self._dictionary._realSetItem(self._key, self._new_value)


class PathDict(UserDict):
    """
    The PathDict class extends a python dictionary with methods to access its nested
    elements by list-based path of keys.
    """

    # Private UndoableDict dictionary-based methods to be called via the QUndoCommand-based classes.

    def __setitem__(self, key: str, val: Any) -> NoReturn:
        """Overrides default dictionary assignment to self[key] implementation.
        Calls the undoable command and pushes this command on the stack."""
        if key in self:
            self._realSetItem(key, val)
        else:
            self._realAddItem(key, val)

    def setItem(self, key: Union[str, list], value: Any) -> NoReturn:
        """Calls the undoable command to set a value in a nested object
        by key sequence and pushes this command on the stack."""
        if isinstance(key, list):
            self.setItemByPath(key, value)
        else:
            self[key] = value

    def setItemByPath(self, keys: list, value: Any) -> NoReturn:
        """Calls the undoable command to set a value in a nested object
        by key sequence and pushes this command on the stack."""
        self._realSetItem(keys, value)

    def _realSetItem(self, key: Union[str, List], value: Any) -> NoReturn:
        """Actually changes the value for the existing key in dictionary."""
        if isinstance(key, list):
            self.getItemByPath(key[:-1])[key[-1]] = value
        else:
            super().__setitem__(key, value)

    def _realAddItem(self, key: str, value: Any) -> NoReturn:
        """Actually adds a key-value pair to dictionary."""
        super().__setitem__(key, value)

    def _realDelItem(self, key: str) -> NoReturn:
        """Actually deletes a key-value pair from dictionary."""
        del self[key]

    def _realSetItemByPath(self, keys: list, value: Any) -> NoReturn:
        """Actually sets the value in a nested object by the key sequence."""
        self.getItemByPath(keys[:-1])[keys[-1]] = value

    # Public dictionary-based methods

    def getItemByPath(self, keys: list, default=None) -> Any:
        """Returns a value in a nested object by key sequence."""
        item = self
        for key in keys:
            if key in item.keys():
                item = item[key]
            else:
                return default
        return item

    def getItem(self, key: Union[str, list], default=None):
        """Returns a value in a nested object. Key can be either a sequence
        or a simple string."""
        if isinstance(key, list):
            return self.getItemByPath(key, default)
        else:
            return self.get(key, default)


class UndoableDict(PathDict):
    """
    The UndoableDict class implements a PathDict-based class with undo/redo
    functionality based on QUndoStack.
    """

    def __init__(self, *args, **kwargs):
        self.stack = QUndoStack()
        super().__init__(*args, **kwargs)

    # Public dictionary-based methods

    def __setitem__(self, key: str, val: Any) -> NoReturn:
        """Overrides default dictionary assignment to self[key] implementation.
        Calls the undoable command and pushes this command on the stack."""
        if key in self:
            self.stack.push(_SetItemCommand(self, key, val))
        else:
            self.stack.push(_AddItemCommand(self, key, val))

    def setItemByPath(self, keys: list, value: Any) -> NoReturn:
        """Calls the undoable command to set a value in a nested object
        by key sequence and pushes this command on the stack."""
        self.stack.push(_SetItemCommand(self, keys, value))

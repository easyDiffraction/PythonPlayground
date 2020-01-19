from typing import Union, Any, NoReturn, List

from PySide2.QtWidgets import QUndoStack, QUndoCommand


class URDict(dict):
    class __SingleStackCommand__(QUndoCommand):
        def __init__(self, dictionary: dict, key: str, value: Any):
            QUndoCommand.__init__(self)
            self._dictionary = dictionary
            self._key = key
            self._old_value = None

            thisKey = key
            if isinstance(thisKey, list):
                thisKey = thisKey[0]
            if thisKey in dictionary:
                self._old_value = dictionary[key]

            self._new_value = value

        def undo(self) -> NoReturn:
            # self.setText("     undo command {} - {}:{} = ".format(self._dictionary, self._key, self._value))
            if self._old_value is None:
                self.setText("     undo command {} - {}:{} = ".format(self._dictionary, self._key, self._new_value))
                del self._dictionary[self._key]
            else:
                self._dictionary.__realsetitem__(self._key, self._old_value)

        def redo(self) -> NoReturn:
            # self.setText("  do/redo command {} + {}:{} = ".format(self._dictionary, self._key, self._value))
            self._dictionary.__realsetitem__(self._key, self._new_value)

    class __MultiStackCommand__(QUndoCommand):
        def __init__(self, dictionary, key: str):
            QUndoCommand.__init__(self)
            self._key = key
            self._dict = dictionary

        def undo(self) -> NoReturn:
            self._dict[self._key].undo()

        def redo(self) -> NoReturn:
            self._dict[self._key].redo()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__stack__ = QUndoStack()
        self._macroRunning = False

    def __setitem__(self, key: str, val: Any) -> NoReturn:
        self.__stack__.push(self.__SingleStackCommand__(self, key, val))

    def __getitem__(self, key: Union[str, List]) -> Any:
        if isinstance(key, list):
            return self.getByPath(key)
        return super().__getitem__(key)

    def __realsetitem__(self, key: Union[str, List], val: Any) -> NoReturn:
        if isinstance(key, list):
            self.setByPath(key, val)
        else:
            super().__setitem__(key, val)

    def undoText(self) -> NoReturn:
        return self.__stack__.undoText()

    def redoText(self) -> NoReturn:
        return self.__stack__.redoText()

    def undo(self) -> NoReturn:
        self.__stack__.undo()

    def redo(self) -> NoReturn:
        self.__stack__.redo()

    def getByPath(self, keys: List) -> Any:
        """Access a nested object in root by key sequence.
        We can't use reduce and operator"""
        item = self
        for key in keys:
            if key in item.keys():
                item = item[key]
            else:
                raise KeyError
        return item

    def setByPath(self, keys: List, value: Any) -> NoReturn:
        """Get a value in a nested object in root by key sequence."""
        self.getByPath(keys[:-1])[keys[-1]] = value


    def startBulkUpdate(self) -> NoReturn:
        self.__stack__.beginMacro('Bulk update')
        self._macroRunning = True

    def endBulkUpdate(self) -> NoReturn:
        self.__stack__.endMacro()
        self._macroRunning = False

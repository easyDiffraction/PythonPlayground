from PySide2.QtWidgets import QUndoStack, QUndoCommand


class URDict(dict):
    class _StackCommand(QUndoCommand):
        def __init__(self, dictionary, key, value):
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

        def undo(self):
            # self.setText("     undo command {} - {}:{} = ".format(self._dictionary, self._key, self._value))
            if self._old_value is None:
                self.setText("     undo command {} - {}:{} = ".format(self._dictionary, self._key, self._new_value))
                del self._dictionary[self._key]
            else:
                self._dictionary.__realsetitem__(self._key, self._old_value)

        def redo(self):
            # self.setText("  do/redo command {} + {}:{} = ".format(self._dictionary, self._key, self._value))
            self._dictionary.__realsetitem__(self._key, self._new_value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__stack__ = QUndoStack()

    def __setitem__(self, key, val):
        self.__stack__.push(self._StackCommand(self, key, val))

    def __getitem__(self, key):
        if isinstance(key, list):
            return self.getByPath(key)
        return super().__getitem__(key)

    def __realsetitem__(self, key, val):
        if isinstance(key, list):
            self.setByPath(key, val)
        else:
            super().__setitem__(key, val)

    def undoText(self):
        return self.__stack__.undoText()

    def redoText(self):
        return self.__stack__.redoText()

    def undo(self):
        self.__stack__.undo()

    def redo(self):
        self.__stack__.redo()

    def getByPath(self, keys):
        """Access a nested object in root by key sequence.
        We can't use reduce and operator"""
        item = self
        for key in keys:
            if key in item.keys():
                item = item[key]
            else:
                raise KeyError
        return item

    def setByPath(self, keys, value):
        """Get a value in a nested object in root by key sequence."""
        self.getByPath(keys[:-1])[keys[-1]] = value
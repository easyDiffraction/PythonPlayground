from typing import Union, Any, NoReturn
from collections import UserList
from PySide2.QtWidgets import QUndoStack, QUndoCommand


class URList(UserList):
    class __SingleStackCommand__(QUndoCommand):
        def __init__(self, myList: 'URList', key: Union[int, slice], value: Any):
            QUndoCommand.__init__(self)
            self._list = myList
            self._key = key
            try:
                self._old_value = self._list[key]
            except IndexError:
                self._old_value = None
            self._new_value = value

        def undo(self) -> NoReturn:
            if self._old_value is None:
                del self._list[self._key]
            else:
                self._list.__realsetitem__(self._key, self._old_value)

        def redo(self) -> NoReturn:
            self._list.__realsetitem__(self._key, self._new_value)

    class __MultiStackCommand__(QUndoCommand):
        def __init__(self, myList: 'URList', key: Union[int, slice]):
            QUndoCommand.__init__(self)
            self._key = key
            self._list = myList

        def undo(self) -> NoReturn:
            self._list[self._key].undo()

        def redo(self) -> NoReturn:
            self._list[self._key].redo()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__stack__ = QUndoStack()
        self._macroRunning = False

    def __setitem__(self, key: Union[int, slice], value: Any) -> NoReturn:
        self.__stack__.push(self.__SingleStackCommand__(self, key, value))

    def __getitem__(self, key):
        if isinstance(key, slice):
            myList = []
            if key.step is None:
                myRange = range(key.start, key.stop + 1)
            else:
                myRange = range(key.start, key.stop + 1, key.step)
            for cKey in myRange:
                myList.append(super().__getitem__(cKey))
            return myList
        return super().__getitem__(key)

    def __realsetitem__(self, key: Union[int, slice], value: Any) -> NoReturn:

        def keyUpdate(base, key, value):
            if key > (len(base.data) - 1):
                super().append(value)
            super().__setitem__(key, value)

        if isinstance(key, slice):
            if key.step is None:
                myRange = range(key.start, key.stop + 1)
            else:
                myRange = range(key.start, key.stop + 1, key.step)
            for cKey in myRange:
                keyUpdate(self, cKey, value[cKey])
                super().__setitem__(cKey, value[cKey])
            return
        keyUpdate(self, key, value)

    def undo(self) -> NoReturn:
        self.__stack__.undo()

    def redo(self) -> NoReturn:
        self.__stack__.redo()

    def startBulkUpdate(self) -> NoReturn:
        self.__stack__.beginMacro('Bulk update')
        self._macroRunning = True

    def endBulkUpdate(self) -> NoReturn:
        self.__stack__.endMacro()
        self._macroRunning = False

    def append(self, item) -> None:
        self.__setitem__(len(self.data), item)

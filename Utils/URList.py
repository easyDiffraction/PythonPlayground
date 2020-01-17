from abc import ABC
from typing import Union, Any, NoReturn, List
from collections import UserList
from PySide2.QtWidgets import QUndoStack, QUndoCommand

class URList(UserList):
    def __init__(self, myList: list):
        super().__init__(myList)
        self.__stack__ = QUndoStack()


# class URList(list):
#     class __SingleStackCommand__(QUndoCommand):
#         def __init__(self, myList: list, key: int, value: Any):
#             QUndoCommand.__init__(self)
#             self._list = myList
#             self._key = key
#             self._old_value = None
#
#             if key in range(len(myList)):
#                 self._old_value = myList[key]
#
#             self._new_value = value
#
#         def undo(self) -> NoReturn:
#             if self._old_value is None:
#                 del self._list[self._key]
#             else:
#                 self._list.insert(self._key, self._old_value)
#
#         def redo(self) -> NoReturn:
#             if self._key > len(self._list):
#                 self._list.append(self._new_value)
#             else:
#                 self._list.insert(self._key, self._new_value)
#
#     class __MultiStackCommand__(QUndoCommand):
#         def __init__(self, myList: list, key: int):
#             QUndoCommand.__init__(self)
#             self._key = key
#             self._list = myList
#
#         def undo(self) -> NoReturn:
#             self._list[self._key].undo()
#
#         def redo(self) -> NoReturn:
#             self._list[self._key].redo()
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.__stack__ = QUndoStack()
#
#     def __setitem__(self, key: int, val: Any) -> NoReturn:
#         self.__stack__.push(self.__SingleStackCommand__(self, key, val))
#
#     def __getitem__(self, key: int) -> Any:
#         return super().__getitem__(key)
#
#     def undo(self) -> NoReturn:
#         self.__stack__.undo()
#
#     def redo(self) -> NoReturn:
#         self.__stack__.redo()
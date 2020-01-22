from typing import Union, Any, NoReturn, List, Iterable, Tuple
from collections import UserDict
from copy import deepcopy

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
        #print(f"dict: {id(self._dictionary)}, key: {id(self._key)}, new val: {id(self._old_value)}, old val: {id(self._old_value)}")


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

    # Private methods

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

    # Public methods

    def __setitem__(self, key: str, val: Any) -> NoReturn:
        """Overrides default dictionary assignment to self[key] implementation."""
        if key in self:
            self._realSetItem(key, val)
        else:
            self._realAddItem(key, val)

    def setItemByPath(self, keys: list, value: Any) -> NoReturn:
        """Set a value in a nested object by key sequence."""
        self._realSetItem(keys, value)

    def setItem(self, key: Union[str, list], value: Any) -> NoReturn:
        """Set a value in a nested object by key sequence or by simple key."""
        if isinstance(key, list):
            self.setItemByPath(key, value)
        else:
            self[key] = value

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

    def toDict(self) -> dict:
        baseD = deepcopy(self.data)
        for key in baseD.keys():
            item = baseD[key]
            if hasattr(item, 'toBase'):
                baseD[key] = item.toBase()
        return baseD

    def dictComparison(self, new_dict: Union['PathDict', dict]) -> Tuple[list, list]:
        """
        Compare self to a dictionary or PathDict and return the update path and value
        :param new_dict: dict or PathDict to compare self to
        :return: path and value updates for self to become newDict
        """
        def dictIterator(old_dict_in: dict, new_dict_in: dict) -> Tuple[list, list]:
            """
            Iterate through a dict and find all comparisons
            :param old_dict_in: Base dictionary
            :param new_dict_in: dictionary to compare to base dictionary
            :return: list of update locations and list of update values
            """
            keyList = []
            itemList = []
            for key, item in new_dict_in.items():
                if key not in old_dict_in.keys():
                    # The field does not exist in the old dict
                    keyList.append(key)
                    itemList.append(item)
                else:
                    # The key exists in both dicts
                    tempItem = old_dict_in[key]
                    if isinstance(item, dict):
                        # Its a dictionary, so we have to call `dictComparison` again
                        nestedKeyList, nestedItemList = dictIterator(tempItem, item)
                        if len(nestedKeyList) > 0:
                            keyList.append([key, nestedKeyList])
                            itemList.append(nestedItemList)
                    else:
                        # We know that we're left with objects and numbers strings etc
                        if item is not tempItem:
                            # They are not the same. Boo
                            keyList.append(key)
                            itemList.append(item)
            return keyList, itemList

        def prettyKey(keylist: list) -> list:
            """
            Makes the key list into a UndoableDict path
            """
            for i, key in enumerate(keylist):
                if isinstance(key, list):
                    if len(key) == 1:
                        keylist[i] = key[0]
                    else:
                        keylist[i] = prettyKey(key)
            return keylist

        def flatten(items: list) -> list:
            """
            Yield items from any nested iterable
            """
            for item in items:
                if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
                    for sub_x in flatten(item):
                        yield sub_x
                else:
                    yield item
        if isinstance(new_dict, PathDict):
            new_dict = new_dict.toDict()
        keyList, itemList = dictIterator(self.toDict(), new_dict)
        return prettyKey(keyList), list(flatten(itemList))


class UndoableDict(PathDict):
    """
    The UndoableDict class implements a PathDict-based class with undo/redo
    functionality based on QUndoStack.
    """

    def __init__(self, *args, **kwargs):
        self.__stack = QUndoStack()
        self._macroRunning = False
        super().__init__(*args, **kwargs)

    # Public methods

    def __setitem__(self, key: str, val: Any) -> NoReturn:
        """
        Calls the undoable command to override PathDict assignment to self[key]
        implementation and pushes this command on the stack.
        """
        if key in self:
            self.__stack.push(_SetItemCommand(self, key, val))
        else:
            self.__stack.push(_AddItemCommand(self, key, val))

    def setItemByPath(self, keys: list, value: Any) -> NoReturn:
        """
        Calls the undoable command to set a value in a nested object
        by key sequence and pushes this command on the stack.
        """
        self.__stack.push(_SetItemCommand(self, keys, value))

    def undo(self) -> NoReturn:
        """
        Undoes the current command on stack.
        """
        self.__stack.undo()

    def redo(self) -> NoReturn:
        """
        Redoes the current command on stack.
        """
        self.__stack.redo()

    def undoText(self) -> str:
        """
        :return the current command on stack.
        """
        return self.__stack.undoText()

    def redoText(self) -> str:
        """
        :return the current command on stack.
        """
        return self.__stack.redoText()

    def startBulkUpdate(self, text='Bulk update') -> NoReturn:
        """
        Begins composition of a macro command with the given text description.
        """
        if self._macroRunning:
            print('Macro already running')
            return
        self.__stack.beginMacro(text)
        self._macroRunning = True

    def endBulkUpdate(self) -> NoReturn:
        """
        Ends composition of a macro command.
        """
        if not self._macroRunning:
            print('Macro not running')
            return
        self.__stack.endMacro()
        self._macroRunning = False

    def bulkUpdate(self, key_list: list, item_list: list) -> NoReturn:
        """
        Performs a bulk update based on a list of keys and a list of values
        :param key_list: list of keys or path keys to be updated
        :param item_list: the value to be updated
        :return: None
        """
        self.startBulkUpdate()
        for key, value in zip(key_list, item_list):
            self.setItemByPath(key, value)
        self.endBulkUpdate()

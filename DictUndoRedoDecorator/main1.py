import os, sys, random
from PySide2.QtCore import QUrl, QObject, Signal, Slot
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWidgets import QUndoStack, QUndoCommand

class AppendCommand(QUndoCommand):
    def __init__(self, dictionary, key, value):
        QUndoCommand.__init__(self)
        print(dictionary)
        self._dictionary = dictionary
        print(self._dictionary)
        self._key = key
        self._value = value

    def undo(self):
        self.setText("     undo command {} - {}:{} = ".format(self._dictionary, self._key, self._value))
        print(self._dictionary)
        del self._dictionary[self._key]

    def redo(self):
        self.setText("  do/redo command {} + {}:{} = ".format(self._dictionary, self._key, self._value))
        print(self._dictionary)
        self._dictionary._realSet(self._key, self._value)


class ModifyCommand(QUndoCommand):
    def __init__(self, dictionary, key, value):
        QUndoCommand.__init__(self)
        self._dictionary = dictionary
        self._key = key
        self._old_value = dictionary[key]
        self._new_value = value
        self.setText("   modify command")

    def undo(self):
        # self.setText("     undo command {} - {}:{} = ".format(self._dictionary, self._key, self._value))
        self._dictionary._realSet(self._key, self._old_value)

    def redo(self):
        # self.setText("  do/redo command {} + {}:{} = ".format(self._dictionary, self._key, self._value))
        self._dictionary._realSet(self._key, self._new_value)

class stackable:
    def __init__(self):
        self.stack = QUndoStack()

    def _myWrapper(self, func):
        def inner(thisDict, key, val):
            if key in thisDict.keys():
                print('Overwriting Key: {}'.format(key))
                self.stack.push(ModifyCommand(thisDict, key, val))
            else:
                self.stack.push(AppendCommand(thisDict, key, val))
        return inner

class MyDict(dict):

    stack = stackable()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _realSet(self, key, val):
        super().__setitem__(key, val)

    @stack._myWrapper
    def __setitem__(self, key, val):
        pass

    def undoText(self):
        return self.stack.stack.undoText()

    def redoText(self):
        return self.stack.stack.redoText()

    def undo(self):
        self.stack.stack.undo()

    def redo(self):
        self.stack.stack.redo()

if __name__ == '__main__':
    dictionary = {"a": "AAA", "b": "BBB"}
    test = MyDict(dictionary)

    print(test)
    test['c'] = 'CCC'
    print(test.undoText(), test)
    test['d']= 'DDD'
    print(test.undoText(), test)

    test.undo()
    print(test.redoText(), test)
    test.undo()
    print(test.redoText(), test)
    test.redo()
    print(test.redoText(), test)
    test['a'] = '---'
    print(test.redoText(), test)
    test.undo()
    print(test.redoText(), test)
    test.redo()
    print(test.redoText(), test)
    test['b'] = '---'
    print(test.redoText(), test)
    test.undo()
    print(test.redoText(), test)
    test.redo()
    print(test.redoText(), test)

    # undo_stack = QUndoStack()
    #
    # dictionary = {"a": "AAA", "b": "BBB"}
    # print('* initial dict', dictionary)
    #
    # undo_stack.push(AppendCommand(dictionary, "c", "CCC"))
    # print(undo_stack.undoText(), dictionary)
    #
    # undo_stack.push(AppendCommand(dictionary, "d", "DDD"))
    # print(undo_stack.undoText(), dictionary)
    #
    # undo_stack.undo()
    # print(undo_stack.redoText(), dictionary)
    #
    # undo_stack.undo()
    # print(undo_stack.redoText(), dictionary)
    #
    # undo_stack.redo()
    # print(undo_stack.undoText(), dictionary)
    #
    # undo_stack.push(ModifyCommand(dictionary, "a", "---"))
    # print(undo_stack.undoText(), dictionary)
    #
    # undo_stack.undo()
    # print(undo_stack.redoText(), dictionary)
    #
    # undo_stack.redo()
    # print(undo_stack.undoText(), dictionary)
    #
    # undo_stack.push(ModifyCommand2(dictionary, "b", "---"))
    # print(undo_stack.undoText(), dictionary)
    #
    # undo_stack.undo(dictionary)
    # print(undo_stack.redoText(), dictionary)
    #
    # undo_stack.redo(dictionary)
    # print(undo_stack.undoText(), dictionary)

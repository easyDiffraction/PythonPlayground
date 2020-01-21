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
        self._dictionary[self._key] = self._value

class ModifyCommand(QUndoCommand):
    def __init__(self, dictionary, key, value):
        QUndoCommand.__init__(self)
        self._dictionary = dictionary
        self._key = key
        self._old_value = dictionary[key]
        self._new_value = value
        self.setText("   modify command")

    def undo(self):
        #self.setText("     undo command {} - {}:{} = ".format(self._dictionary, self._key, self._value))
        self._dictionary[self._key] = self._old_value

    def redo(self):
        #self.setText("  do/redo command {} + {}:{} = ".format(self._dictionary, self._key, self._value))
        self._dictionary[self._key] = self._new_value

#
class ModifyCommand2(QUndoCommand):
    def __init__(self, dictionary, key, value):
        QUndoCommand.__init__(self)
        self._key = key
        self._old_value = dictionary[key]
        self._new_value = value
        self.setText("   modify command")

    def undo(self, dictionary):
        #self.setText("     undo command {} - {}:{} = ".format(self._dictionary, self._key, self._value))
        dictionary[self._key] = self._old_value

    def redo(self, dictionary):
        #self.setText("  do/redo command {} + {}:{} = ".format(self._dictionary, self._key, self._value))
        dictionary[self._key] = self._new_value


class MiscClass:
    def __init__(self, dict=None):
        if dict is not None:
            self.dict = dict
        else:
            self.dict = {}
        self.stack = QUndoStack()

    def get(self, item):
        if item in self.dict.keys():
            return self.dict[item]
        else:
            raise KeyError

    def set(self, item, value):
        if item in self.dict.keys():
            print('Overwriting Key: {}'.format(item))
            self.stack.push(ModifyCommand(self.dict, item, value))
        else:
            self.stack.push(AppendCommand(self.dict, item, value))

    def undo(self):
        self.stack.undo()

    def redo(self):
        self.stack.redo()

    def __str__(self):
        return self.dict.__str__()

if __name__ == '__main__':

    dictionary = {"a": "AAA", "b": "BBB"}
    test = MiscClass(dictionary)

    print(test)
    test.set('c', 'CCC')
    print(test.stack.undoText(), test)
    test.set('d', 'DDD')
    print(test.stack.undoText(), test)

    test.undo()
    print(test.stack.redoText(), test)
    test.undo()
    print(test.stack.redoText(), test)
    test.redo()
    print(test.stack.redoText(), test)
    test.set('a', '---')
    print(test.stack.redoText(), test)
    test.undo()
    print(test.stack.redoText(), test)
    test.redo()
    print(test.stack.redoText(), test)
    test.set('b', '---')
    print(test.stack.redoText(), test)
    test.undo()
    print(test.stack.redoText(), test)
    test.redo()
    print(test.stack.redoText(), test)

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

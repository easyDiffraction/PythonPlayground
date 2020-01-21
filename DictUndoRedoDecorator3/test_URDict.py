from URDict import URDict


def test_non_nested_dict():

    d = URDict()

    # Add item

    assert d == {}
    assert d.stack.undoText() == ""
    assert d.stack.redoText() == ""

    d['a'] = 'AAA'
    assert d == {'a': 'AAA'}
    assert d.stack.undoText() == "Adding: a = AAA"
    assert d.stack.redoText() == ""

    d['b'] = 'BBB'
    assert d == {'a': 'AAA', 'b': 'BBB'}
    assert d.stack.undoText() == "Adding: b = BBB"
    assert d.stack.redoText() == ""

    d['c'] = 'CCC'
    assert d == {'a': 'AAA', 'b': 'BBB', 'c': 'CCC'}
    assert d.stack.undoText() == "Adding: c = CCC"
    assert d.stack.redoText() == ""

    d.stack.undo()
    assert d == {'a': 'AAA', 'b': 'BBB'}
    assert d.stack.undoText() == "Adding: b = BBB"
    assert d.stack.redoText() == "Adding: c = CCC"

    d.stack.redo()
    assert d == {'a': 'AAA', 'b': 'BBB', 'c': 'CCC'}
    assert d.stack.undoText() == "Adding: c = CCC"
    assert d.stack.redoText() == ""

    # Set item

    d['a'] = '---'
    assert d == {'a': '---', 'b': 'BBB', 'c': 'CCC'}
    assert d.stack.undoText() == "Setting: a = ---"
    assert d.stack.redoText() == ""

    d['b'] = '+++'
    assert d == {'a': '---', 'b': '+++', 'c': 'CCC'}
    assert d.stack.undoText() == "Setting: b = +++"
    assert d.stack.redoText() == ""

    d.stack.undo()
    assert d == {'a': '---', 'b': 'BBB', 'c': 'CCC'}
    assert d.stack.undoText() == "Setting: a = ---"
    assert d.stack.redoText() == "Setting: b = +++"

    d.stack.undo()
    assert d == {'a': 'AAA', 'b': 'BBB', 'c': 'CCC'}
    assert d.stack.undoText() == "Adding: c = CCC"
    assert d.stack.redoText() == "Setting: a = ---"

    d.stack.undo()
    assert d == {'a': 'AAA', 'b': 'BBB'}
    assert d.stack.undoText() == "Adding: b = BBB"
    assert d.stack.redoText() == "Adding: c = CCC"

    d.stack.redo()
    assert d == {'a': 'AAA', 'b': 'BBB', 'c': 'CCC'}
    assert d.stack.undoText() == "Adding: c = CCC"
    assert d.stack.redoText() == "Setting: a = ---"

    d.stack.redo()
    assert d == {'a': '---', 'b': 'BBB', 'c': 'CCC'}
    assert d.stack.undoText() == "Setting: a = ---"
    assert d.stack.redoText() == "Setting: b = +++"

    # Add item again

    d['e'] = 999
    assert d == {'a': '---', 'b': 'BBB', 'c': 'CCC', 'e': 999}
    assert d.stack.undoText() == "Adding: e = 999"
    assert d.stack.redoText() == ""


def test_nested_dict():

    # Add item

    d = URDict(dict(a=1, b=2, c=dict(d=3, e=dict(f=4, g=5))))
    d.stack.clear()
    assert d.stack.undoText() == ""
    assert d.stack.redoText() == ""

    d['a'] = "---"
    assert d == {'a': '---', 'b': 2, 'c': {'d': 3, 'e': {'f': 4, 'g': 5}}}
    assert d.stack.undoText() == "Setting: a = ---"
    assert d.stack.redoText() == ""

    d.stack.undo()
    assert d == {'a': 1, 'b': 2, 'c': {'d': 3, 'e': {'f': 4, 'g': 5}}}
    assert d.stack.undoText() == ""
    assert d.stack.redoText() == "Setting: a = ---"

    d.stack.redo()
    assert d == {'a': '---', 'b': 2, 'c': {'d': 3, 'e': {'f': 4, 'g': 5}}}
    assert d.stack.undoText() == "Setting: a = ---"
    assert d.stack.redoText() == ""

    d.setItemByPath(['c', 'e', 'g'], '***')
    assert d == {'a': '---', 'b': 2, 'c': {'d': 3, 'e': {'f': 4, 'g': '***'}}}
    assert d.stack.undoText() == "Setting: ['c', 'e', 'g'] = ***"
    assert d.stack.redoText() == ""

    d.stack.undo()
    assert d == {'a': '---', 'b': 2, 'c': {'d': 3, 'e': {'f': 4, 'g': 5}}}
    assert d.stack.undoText() == "Setting: a = ---"
    assert d.stack.redoText() == "Setting: ['c', 'e', 'g'] = ***"

    d.stack.redo()
    assert d == {'a': '---', 'b': 2, 'c': {'d': 3, 'e': {'f': 4, 'g': '***'}}}
    assert d.stack.undoText() == "Setting: ['c', 'e', 'g'] = ***"
    assert d.stack.redoText() == ""


def test_bulk_update():

    # Add item

    d = URDict(dict(a=1, b=2, c=dict(d=3, e=dict(f=4, g=5))))
    d.stack.clear()
    assert d.stack.undoText() == ""
    assert d.stack.redoText() == ""

    d['b'] = 999
    assert d == {'a': 1, 'b': 999, 'c': {'d': 3, 'e': {'f': 4, 'g': 5}}}
    assert d.stack.undoText() == "Setting: b = 999"
    assert d.stack.redoText() == ""

    d['b'] = 2
    assert d == {'a': 1, 'b': 2, 'c': {'d': 3, 'e': {'f': 4, 'g': 5}}}
    assert d.stack.undoText() == "Setting: b = 2"
    assert d.stack.redoText() == ""

    d['b'] = 777
    assert d == {'a': 1, 'b': 777, 'c': {'d': 3, 'e': {'f': 4, 'g': 5}}}
    assert d.stack.undoText() == "Setting: b = 777"
    assert d.stack.redoText() == ""

    d.stack.undo()
    assert d == {'a': 1, 'b': 2, 'c': {'d': 3, 'e': {'f': 4, 'g': 5}}}
    assert d.stack.undoText() == "Setting: b = 2"
    assert d.stack.redoText() == "Setting: b = 777"

    assert d.stack.canUndo() is True
    assert d.stack.canRedo() is True

    d.stack.beginMacro("Bulk update")

    assert d.stack.canUndo() is False
    assert d.stack.canRedo() is False

    d['a'] = "---"
    assert d == {'a': '---', 'b': 2, 'c': {'d': 3, 'e': {'f': 4, 'g': 5}}}
    assert d.stack.undoText() == ""
    assert d.stack.redoText() == ""

    d.setItemByPath(['c', 'e', 'g'], '***')
    assert d == {'a': '---', 'b': 2, 'c': {'d': 3, 'e': {'f': 4, 'g': '***'}}}
    assert d.stack.undoText() == ""
    assert d.stack.redoText() == ""

    d.stack.endMacro()

    d.stack.undo()
    assert d == {'a': 1, 'b': 2, 'c': {'d': 3, 'e': {'f': 4, 'g': 5}}}
    assert d.stack.undoText() == "Setting: b = 2"
    assert d.stack.redoText() == "Bulk update"

    d.stack.redo()
    assert d == {'a': '---', 'b': 2, 'c': {'d': 3, 'e': {'f': 4, 'g': '***'}}}
    assert d.stack.undoText() == "Bulk update"
    assert d.stack.redoText() == ""

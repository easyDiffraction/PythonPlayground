from URDict import URDict


def test_simple():

    d = URDict()

    # Add

    assert d == {}
    assert d.undoText() == ""
    assert d.redoText() == ""

    d['a'] = 'AAA'
    assert d == {'a': 'AAA'}
    assert d.undoText() == "Adding: a = AAA"
    assert d.redoText() == ""

    d['b'] = 'BBB'
    assert d == {'a': 'AAA', 'b': 'BBB'}
    assert d.undoText() == "Adding: b = BBB"
    assert d.redoText() == ""

    d['c'] = 'CCC'
    assert d == {'a': 'AAA', 'b': 'BBB', 'c': 'CCC'}
    assert d.undoText() == "Adding: c = CCC"
    assert d.redoText() == ""

    d.undo()
    assert d == {'a': 'AAA', 'b': 'BBB'}
    assert d.undoText() == "Adding: b = BBB"
    assert d.redoText() == "Adding: c = CCC"

    d.redo()
    assert d == {'a': 'AAA', 'b': 'BBB', 'c': 'CCC'}
    #assert d.undoText() == "Adding: c = CCC"
    #assert d.redoText() == ""

    # Set

    d['a'] = '---'
    assert d == {'a': '---', 'b': 'BBB', 'c': 'CCC'}
    #assert d.undoText() == "Setting: a = ---"
    #assert d.redoText() == ""

    d['b'] = '+++'
    assert d == {'a': '---', 'b': '+++', 'c': 'CCC'}
    #assert d.undoText() == "Setting: b = +++"
    #assert d.redoText() == ""

    d.undo()
    assert d == {'a': '---', 'b': 'BBB', 'c': 'CCC'}
    #assert d.undoText() == "Setting: a = ---"
    #assert d.redoText() == "Setting: b = BBB" #???

    d.undo()
    assert d == {'a': 'AAA', 'b': 'BBB', 'c': 'CCC'}

    d.undo()
    assert d == {'a': 'AAA', 'b': 'BBB'}

    d.redo()
    assert d == {'a': 'AAA', 'b': 'BBB', 'c': 'CCC'}

    d.redo()
    assert d == {'a': '---', 'b': 'BBB', 'c': 'CCC'}

    # Add again

    d['e'] = 999
    assert d == {'a': '---', 'b': 'BBB', 'c': 'CCC', 'e': 999}




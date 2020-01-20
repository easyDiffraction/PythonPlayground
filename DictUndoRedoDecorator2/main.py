from URDict import URDict


if __name__ == '__main__':

    print("\n****Test phase 1****")

    test = URDict(a="AAA", b="BBB")
    print("\n-1 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test['c'] = 'CCC'
    print("\n-2 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test['d'] = 'DDD'
    print("\n-3 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test.undo()
    print("\n-4 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test.undo()
    print("\n-5 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test.redo()
    print("\n-6 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test['a'] = '---'
    print("\n-7 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test.undo()
    print("\n-8 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test.redo()
    print("\n-9 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test['b'] = '---'
    print("\n-10 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test.undo()
    print("\n-11 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test.redo()
    print("\n-12 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    print("\n****Test phase 2****")

    test = URDict(dict(a=1, b=2, c=dict(d=3, e=dict(f=4, g=5))))
    print("\n-1 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test['a'] = "---"
    print("\n-2 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test.undo()
    print("\n-3 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test.redo()
    print("\n-4 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    #test['c']['e']['g'] = "999"
    #print("\n-5 ", test)
    #print("Undo", test.undoText())
    #print("Redo", test.redoText())

    #test.undo()
    #print("\n-6 ", test)
    #print("Undo", test.undoText())
    #print("Redo", test.redoText())

    #test.redo()
    #print("\n-7 ", test)
    #print("Undo", test.undoText())
    #print("Redo", test.redoText())

    test.setItemByPath(['c', 'e', 'g'], '***')
    print("\n-8 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test.undo()
    print("\n-9 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test.redo()
    print("\n-10 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    print("\n****Test phase 3****")

    test = URDict(dict(a=1, b=2, c=dict(d=3, e=dict(f=4, g=5))))
    print("\n-1 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test.startBulkUpdate()

    test['a'] = "---"
    print("\n-2 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test.setItemByPath(['c', 'e', 'g'], '***')
    print("\n-2 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

    test.endBulkUpdate()

    test.undo()
    print("\n-3 ", test)
    print("Undo", test.undoText())
    print("Redo", test.redoText())

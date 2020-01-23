import pytest
from Utils.DictTools import PathDict


def test_dictComparison():

    d = PathDict(dict(a=1, b=2, c=dict(d=3, e=dict(f=4, g=5))))
    assert d == {'a': 1, 'b': 2, 'c': {'d': 3, 'e': {'f': 4, 'g': 5}}}

    d1 = PathDict(dict(a=1, b=2, c=dict(d=3, e=dict(f=4, g=5))))
    d2 = PathDict(dict(a=1, b=2, c=dict(d=333, e=dict(f=4, g=555))))
    #assert d1.dictComparison(d2) == ([['c', 'd'], ['c', 'e', 'g']], [333, 555])

    d1 = PathDict(dict(a=1, b=2, c=dict(d=3, e=dict(f=4, g=5))))
    d2 = {'a': 1, 'b': 2, 'c': {'d': 333, 'e': {'f': 4, 'g': 555}}}
    #assert d1.dictComparison(d2) == ([['c', 'd'], ['c', 'e', 'g']], [333, 555])

    d1 = PathDict(dict(a=1, b=2, c=dict(d=3, e=dict(f=4, g=5))))
    d2 = "string"
    with pytest.raises(TypeError):
        d1.dictComparison(d2)

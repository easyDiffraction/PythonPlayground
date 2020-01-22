from typing import Tuple
from copy import deepcopy
from typing import Iterable

from PythonPlayground.Utils.DictTools import UndoableDict

def dictComparison(oldDict: dict, newDict: dict) -> Tuple[list, list]:

    def dictItterator(oldDictIn: dict, newDictIn: dict) -> Tuple[list, list]:
        keyList = []
        itemList = []
        for key, item in newDictIn.items():
            if key not in oldDictIn.keys():
                # The field does not exist in the old dict
                keyList.append(key)
                itemList.append(item)
            else:
                # The key exists in both dicts
                tempItem = oldDictIn[key]
                if isinstance(item, dict):
                    # Its a dictionary, so we have to call `dictComparison again
                    nestedKeyList, nestedItemList = dictItterator(tempItem, item)
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

    keyList, itemList = dictItterator(oldDict, newDict)
    return prettyKey(keyList), list(flatten(itemList))

def bulkUpdate(inDict: UndoableDict, keyList: list, itemList: list) -> UndoableDict:
    inDict.startBulkUpdate()
    for key, value in zip(keyList, itemList):
        inDict.setItemByPath(key, value)
    inDict.endBulkUpdate()
    return inDict

if __name__ == '__main__':

    dict1 = {"a": "AAA", "b": "BBB", "c": "CCC"}
    dict2 = {"a": "AAA", "b": "BBB", "c": "CDC"}
    dict2['d'] = "DDD"
    dict2['e'] = dict(f='FFF', g='GGG')
    dict1 = deepcopy(dict2)
    dict2['e']['g'] = "GHG"
    dict2['a'] = "ABA"

    key, item = dictComparison(dict1, dict2)
    print('{} - {}'.format(key, item))


    dictUR1 = UndoableDict(**dict1)
    dictUR2 = UndoableDict(**dict2)

    dictUR1 = bulkUpdate(dictUR1, key, item)
    key, item = dictComparison(dictUR1.toDict(), dictUR2.toDict())
    print('{} - {}'.format(key, item))

    dictUR1.undo()
    key, item = dictComparison(dictUR1.toDict(), dictUR2.toDict())
    print('{} - {}'.format(key, item))






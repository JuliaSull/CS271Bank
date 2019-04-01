#------------------------------------------------------------------
# Author: Julian Sullivan
# Purpose: Suite of tests to understand when python copies data
#------------------------------------------------------------------

import copy
import inspect

def Test1():
    print(inspect.stack()[0][3] + ": ")
    def CreateList():
        return []

    list1 = CreateList()
    list1.append(1)
    list2 = CreateList()
    list2.append(2)
    if list1 != list2:
        print("A list created from a local function will produce unique lists")
    else:
        print("A list created from a local function will produce shallow lists")

def GlobalCreateList():
    return []

def Test2():
    print(inspect.stack()[0][3] + ": ")
    list1 = GlobalCreateList()
    list1.append(1)
    list2 = GlobalCreateList()
    list2.append(2)
    if list1 != list2:
        print("A list created from a global function will produce unique lists")
    else:
        print("A list created from a global function will produce shallow lists")

def Test3():
    print(inspect.stack()[0][3] + ": ")
    list1 = []
    list1.append(1)
    list2 = []
    list2.append(2)
    if list1 != list2:
        print("A list created from a local [] initialization will produce unique lists")
    else:
        print("A list created from a local [] initialization will produce shallow lists")

def Test4():
    print(inspect.stack()[0][3] + ": ")
    for i in range(5):
        list = []
        list.append(i)

    if len(list) == 1:
        print("A list created in a for loop using [] will produce unique lists")
    else:
        print("A list created in a for loop using [] will produce shallow lists")

def Test5():
    print(inspect.stack()[0][3] + ": ")
    list1 = []
    list2 = list1
    list1.append(1)

    if list1 != list2:
        print("A list created via assignment of another list will produce unique lists")
    else:
        print("A list created via assignment of another list will produce shallow lists")

class TestObjectNoInit:
    List = []

def Test6():
    print(inspect.stack()[0][3] + ": ")
    obj1 = TestObjectNoInit()
    obj2 = TestObjectNoInit()
    obj1.List.append(1)
    if obj1.List != obj2.List:
        print("A list created via creation of an object with 0 __init__ functions will produce unique lists")
    else:
        print("A list created via creation of an object with 0 __init__ functions will produce shallow lists")

class TestObjectWithInit:
    List = []
    def __init__(self):
        self.List = []

def Test7():
    print(inspect.stack()[0][3] + ": ")
    obj1 = TestObjectWithInit()
    obj2 = TestObjectWithInit()
    obj1.List.append(1)
    if obj1.List != obj2.List:
        print("A list created via creation of an object with 1 __init__ functions will produce unique lists")
    else:
        print("A list created via creation of an object with 1 __init__ functions will produce shallow lists")

def Test8():
    print(inspect.stack()[0][3] + ": ")
    listList = []
    for i in range(3):
        listList.append([i])

    listList[0][0] += 10

    if listList == [[10], [1], [2]]:
        print("A list created in a for loop and added to another list will produce unique lists")
    else:
        print("A list created in a for loop and added to another list will produce shallow lists")

def Test9():
    print(inspect.stack()[0][3] + ": ")
    listList = []
    for i in range(3):
        listList.append([0])

    listList[0][0] += 1

    if listList == [[1], [0], [0]]:
        print("A list created in a for loop with non-unique values will produce unique lists")
    else:
        print("A list created in a for loop with non-unique values will produce shallow lists")

def ModifyList(List, val):
        List[0] = 10
        List.append(val)
        del List[1]

def Test10():
    print(inspect.stack()[0][3] + ": ")
    list1 = []
    list1.append(0)
    list1.append(5)
    ModifyList(list1, 1)

    if list1 == [10, 1]:
        print("A list passed to a function will operate as a shallow copy in all situations")
    else:
        if list1[0] == 10:
            print("A list passed to a function will allow for modification via assignment (list[0] = 10)")
        elif 5 not in list1:
            print("A list passed to a function will allow for deletion via del (del list[1])")
        elif 1 in list1:
            print("A list passed to a function will allow for addition via append (list.append(1))")

def Test11():
    print(inspect.stack()[0][3] + ": ")
    def Optional(list = []):
        list.append(1)
        return list

    list1 = Optional() + Optional()
    if len(list1) == 2 and len(list1[0]) == 1 and len(list1[1]) == 1:
        print("A list created as an optional parameter will produce unique lists")
    else:
        print("A list created as an optional parameter will produce shallow lists")

def Test12():
    print(inspect.stack()[0][3] + ": ")
    list1 = [0]
    list2 = list(list1)

    list1.append(1)
    list1[0] = 10

    if list2 == [0]:
        print("A list created using list(otherList) will produce unique lists")
    else:
        print("A list created using list(otherList) will produce shallow lists")

def Test13():
    print(inspect.stack()[0][3] + ": ")
    list1 = [0, [1]]
    list2 = copy.copy(list1)

    list1[0] = 10
    if list2[0] != 10:
        print("A list created using copy.copy(otherList) will produce unique lists")
    else:
        print("A list created using copy.copy(otherList) will produce shallow lists")

    list1[1][0] = 10
    
    if list2[1][0] != 10:
        print("A list created using copy.copy(otherList) will deep copy all elements of the list")
    else:
        print("A list created using copy.copy(otherList) will shallow copy all elements of the list")

def Test14():
    print(inspect.stack()[0][3] + ": ")
    list1 = [0, [1]]
    list2 = copy.deepcopy(list1)

    list1[0] = 10
    if list2[0] != 10:
        print("A list created using copy.deepcopy(otherList) will produce unique lists")
    else:
        print("A list created using copy.deepcopy(otherList) will produce shallow lists")

    list1[1][0] = 10
    
    if list2[1][0] != 10:
        print("A list created using copy.deepcopy(otherList) will deep copy all elements of the list")
    else:
        print("A list created using copy.deepcopy(otherList) will shallow copy all elements of the list")

Test1()   ;print("")
Test2()   ;print("")
Test3()   ;print("")
Test4()   ;print("")
Test5()   ;print("")
Test6()   ;print("")
Test7()   ;print("")
Test8()   ;print("")
Test9()   ;print("")
Test10()  ;print("")
Test11()  ;print("")
Test12()  ;print("")
Test13()  ;print("")
Test14()  ;print("")

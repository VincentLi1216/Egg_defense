class Test:
    def __init__(self, index):
        self.index = index

lst = []
lst.append(Test(3))
lst.append(Test(12))
lst.append(Test(0))
lst.append(Test(4))
lst.append(Test(3))

sorted_list = sorted(lst, key=lambda obj: obj.index, reverse=True)

for i in sorted_list:
    print(i.index)
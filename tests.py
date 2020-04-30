import jsoner

db=jsoner.db('test.json',{},2)
print(db)
db['test'] = 34

if len(db) > 20:
    print(a)
else:
    print(len(db)>=3)

'''
    def __contains__(self, item):
        # item in self  --> bool
        pass

    def __eq__(self, other):
        # self == other --> bool
        pass

    def __gt__(self, other):
        # self > other --> bool
        pass

    def __ge__(self, other):
        # self >= other --> bool
        pass

    def __lt__(self,other):
        # self < other --> bool
        pass

    def __le__(self, other):
        # self <= other --> bool
        pass
    '''
import jsoner

db = jsoner.db('test.json', {})
db['lolo'] = {}
db['lolo']['haha'] = {}
db['lolo']['haha']['ss'] = {}
db['lolo']['haha']['ss']['gg'] = {}
db['lolo']['haha']['ss']['gg']['aha'] = {}
db['lolo']['haha']['ss']['gg']['aha']['lol'] = 1
db['lolo']['haha']['ss']['gg']['aha']['lol'] = 'string'
print(db)
print(db['lolo']['haha'])
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
# -*- coding: utf-8 -*-

import json
from .classtypes import *
from .errors import *
import os


class db:
    """
            CLASS db

            :param file:  -  name of database (like 'xxx.json')

            :param data:  -  data adding into the db in start

            ! if you set data - all data in file will be cleared and reloaded !
            !         don't set data if you would load json file              !

            to start using:
                import jsoner
                db = jsoner.db('testname.json',{},2) # creates db file with {}
                db['test'] = 1                       # creates 'test' in db
                print(db)                            # shows {'test':1}

                more examples in README
        """

    def __init__(self, file, data=None):
        self.file = file

        if data is None:
            self.data = self.load()

        elif type(data) == DICT:
            types = [type(key) for key in data.values()]
            if (DICT in types) or (LIST in types):
                for key, value in data.items():
                    if type(value) in [DICT, LIST]:
                        data[key] = db(file=self.file, data=value)
            self.data = data

        elif type(data) == LIST:
            types = [type(key) for key in data]
            if (DICT in types) or (LIST in types):
                for key in range(len(data)):
                    if type(data[key]) in [DICT, LIST]:
                        data[key] = db(file=self.file, data=data[key])
            self.data = data

        self.datatype = type(self.data)

    def __repr__(self):
        data = str(self.data)
        return data

    def __str__(self):
        data = str(self.data)
        return data

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        if type(value) in (DICT, LIST):
            value = db('lol', data=value)

        if self.datatype == DICT:
            self.update({key: value})
        elif self.datatype == LIST and isinstance(key, int):
            if abs(key) >= len(self):
                raise IndexError('list out of range')
            else:
                self.data[key] = value
        self.save()

    def __len__(self):
        return len(self.data)

    def load(self):
        if not os.path.exists(self.file):
            raise FileNotFoundError(f'File with name "{self.file}" not found. [ {os.getcwd()} ]')
        fb = open(self.file, 'r')
        try:
            data = json.load(fb)
        except json.decoder.JSONDecodeError as err:
            line = err.lineno
            col = err.colno
            raise UnreadableJSON(f'File {self.file} not readable in [line: {line}|col: {col}]')
        return data

    def save(self):
        with open(file=self.filename, mode='w') as fb:
            try:
                json.dump(self.data, fb, cls=dbEncoder)
            except:
                with open('$tempBD.py', 'w') as fb:
                    fb.write('db=' + str(self.data) + '\n \
                               # if that file maked (saved export), bugs in code, in dumping data')

    def update(self, value, **kwargs):
        self.data.update(value, **kwargs)
        self.save()

    def append(self, *args):
        if self.datatype == DICT:
            if type(args[0]) == DICT:
                self.data.update(args[0])
            else:
                self.data.update({args[0]: args[1]})
        elif self.datatype == LIST:
            for num in args:
                self.data.append(num)
        self.save()

    def keys(self):
        if self.datatype == DICT:
            return list(self.data.keys())
        elif self.datatype == LIST:
            return self.data

    def values(self):
        if self.datatype == DICT:
            return list(self.data.values())
        elif self.datatype == LIST:
            return self.data

    def items(self):
        if self.datatype == DICT:
            return self.data.items()
        elif self.datatype == LIST:
            return self.data


class dbEncoder(json.JSONEncoder):
    """ used for encode class db to json"""

    def default(self, obj):
        if isinstance(obj, db):
            return obj.__dict__['data']
        return json.JSONEncoder.default(self, obj)

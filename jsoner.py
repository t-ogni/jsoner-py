# -*- coding: utf-8 -*-

import json
from classtypes import *
from errors import *
import logging
import os
import threading
import time

logging.basicConfig(level = logging.WARNING, filename='jsoner.log',
    format = '%(filename)s [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s' )
logger = logging.getLogger(__file__)

"""
Logging Levels:
CRITICAL  50
ERROR     40
WARNING   30
INFO      20
DEBUG     10
NOTSET    0
"""

class db:
    """
            CLASS db 

            :param file:  -  name of database (like 'xxx.json')

            :param data:  -  data adding into the db in start

            ! if you set data - all data in file will be cleared and reloaded !
            !         don't set data if you would load json file              !
            :param savetype:  -  set 1 or 2:
                1 {faster} - 
                    data update all the time in external thread
                    with a speed of 1 update in 1 second

                    [it's better when you have many updates in a short period of time like a loops]
                    [but be careful: database can be cleared if updating data will incoreect      ]

                2  {qualitative} - 
                    all data will be updated when data changes

                    [it's better when you have big list of data]

            to start using:
                import jsoner
                db = jsoner.db('testname.json',{},2) # creates db file with {}
                db['test'] = 1                       # creates 'test' in db
                print(db)                            # shows {'test':1}
                



        """

    def __init__(self, file='database.json', data=None, savetype=1):
        '''
        INIT MODULE
        creating new db object
        '''
        self.savetype = int(savetype)
        self.commitLOOP = False
        self.filename = file
        if data == None:
            self.data = self.load_from(file)

        elif type(data) == DICT:
            self.datatype = DICT
            types = [type(key) for key in data.values()]
            if ((DICT in types) or (LIST in types)):
                for key, value in data.items():
                    if type(value) in [DICT, LIST]:
                        data[key] = db(file=self.filename, data=value)
            self.data = data

        elif type(data) == LIST:
            self.datatype = LIST
            types = [type(key) for key in data]
            if ((DICT in types) or (LIST in types)):
                for key in range(len(data)):
                    if type(data[key]) in [DICT, LIST]:
                        data[key] = db(file=self.filename, data=data[key])

            self.data = data

        else:
            raise IllegalTypeError

        self.commit()

    def __repr__(self):
        data = str(self.data)
        return data

    def __str__(self):
        data = str(self.data)
        return data

    # def __call__(self):
    #     return self.data

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        if type(value) == DICT:
            value = db(self.filename, data=value)
        if self.datatype == DICT:
            self.update({key: value})
        elif self.datatype == LIST and isinstance(key, int):
            if abs(key) >= len(self):
                raise IndexError('list out of range')
            else:
                self.data[key] = value
        else:
            raise IndexError('list out of range')

    def __delitem__(self, key):
        del self.storage[key]

    def __getattr__(self, name):
        print(f'uniknown requested name: {name}')

    def __add__(self, other):
        data = self.data
        if self.datatype == DICT:
            data.update(other)
        elif self.datatype == LIST:
            data.append(other)
        return data

    def __radd__(self, other):
        if self.datatype == DICT:
            data.update(other)
        elif self.datatype == LIST:
            data.instert(0,other)
        return data
    
    def __len__(self):
        return(len(self.data))

    def load_from(self, file):
        if isinstance(file, str):
            if not os.path.exists(file):
                logger.error(f'File with name "{file}" not found. [ {os.getcwd()} ]')
                raise FileNotFoundError(f'File with name "{file}" not found. [ {os.getcwd()} ]')
            fb = open(file, 'r')
            try:
                data = json.load(fb)
            except json.decoder.JSONDecodeError as err:
                line = (err.lineno)
                col = (err.colno)
                logger.critical(f'File {self.filename} not readable in [line: {line}|col: {col}]')
                raise UnreadableJSON(f'File {self.filename} not readable in [line: {line}|col: {col}]')
            else:
                logger.info(f'File {self.filename} was readed')
        else:
            logger.critical(f'Filename has illegal format {self.filename}')
            raise IllegalTypeError(f'Filename must be string')

        self.datatype = type(data)
        return data

    def load(self):
        with open(self.filename, 'r') as fb:
            try:
                data = json.load(fb)
            except json.decoder.JSONDecodeError as err:
                line = (err.lineno)
                col = (err.colno)
                logger.critical(f'File {self.filename} not readable in [line: {line}|col: {col}]')
                raise UnreadableJSON(f'File {self.filename} not readable in [line: {line}|col: {col}]')
            else:
                logger.info(f'File {self.filename} was readed')
        return data

    def append(self, *args):
        if self.datatype == DICT:
            if type(args[0]) == DICT:
                self.data.update(args[0])
            else:
                self.data.update({args[0]: args[1]})
        elif self.datatype == LIST:
            for num in args:
                self.data.append(num)
        # self.commit()

    def update(self, value, **kwargs):
        self.data.update(value, **kwargs)

    def remove(self, *args):
        for arg in args:
            if self.datatype == DICT:
                self.data.pop(arg)
            elif self.datatype == LIST:
                self.data.remove(arg)
        # self.commit()

    def commit(self):
        """
        tests:
            [mas from -1000 to 1000]
                commit mode 2: 14 sec
                commit mode 1: 1 sec

        """
        if ((self.savetype == 1) and not(self.commitLOOP)): #thread saving
            c = threading.Thread(target=self.commitTH)
            c.start()
        elif (self.savetype == 2): # saving changes
            self.commitCH()

    def commitTH(self):
        self.sleeptime = 1
        self.commitLOOP = True
        while self.commitLOOP:
            time.sleep(self.sleeptime)
            with open(file=self.filename, mode='w') as fb:
                try:
                    json.dump(self.data, fb, cls=dbEncoder)
                except:
                    with open('$tempBD.py', 'w') as fb:
                        fb.write('db='+str(self.data)+'\n \
                        # if that file maked (saved export), bugs in code, in dumping data')

    def commitCH(self):
        with open(file=self.filename, mode='w') as fb:
                try:
                    json.dump(self.data, fb, cls=dbEncoder)
                except:
                    with open('$tempBD.py', 'w') as fb:
                        fb.write('db='+str(self.data)+'\n \
                        # if that file maked (saved export), bugs in code, in dumping data')

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
            return list(self.data.items())
        elif self.datatype == LIST:
            return self.data

    def close(self):
        self.commitLOOP = False

class dbEncoder(json.JSONEncoder):
    """ used for encode class db to json"""

    def default(self, obj):
        if isinstance(obj, db):
            return obj.__dict__['data']
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':

    a = db('data.json')
    a.append({'45': 89})
    print(a)
    print(len(a))
    a.close()
# -*- coding: utf-8 -*-

DICT = type(dict())
LIST = type(list())
TUPLE = type(tuple())
STR = type(str())
INT = type(int())
FLOAT = type(float())
BYTES = type(bytes())
NIL = type(None)
BOOL = type(bool())


def cltype(obj):
    return obj.__class__

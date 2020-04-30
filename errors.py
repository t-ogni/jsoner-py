# -*- coding: utf-8 -*-

"""
jsoner.errors
 - Error
 - UnsupportedTypeError
 - IllegalTypeError
 - UnreadableJSON
 - UnsupportedOperation
~~~~~~~~~~~~

"""


class Error(Exception):
    pass


class UnsupportedTypeError(Error):
    pass


class IllegalTypeError(Error):
    pass


class UnreadableJSON(Error):
    pass


class UnsupportedOperation(Error):
    pass

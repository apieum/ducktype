# -*- coding: utf8 -*-
import inspect
__all__ = ["isducktype"]

def isducktype(given, obj_or_tuple):
    if type(obj_or_tuple) is not tuple:
        obj_or_tuple = (obj_or_tuple, )
    for obj in obj_or_tuple:
        if __check(given, obj):
            return True
    return False

__public = lambda member_name: member_name[0] != '_'

def __is_duck(given, expected):
    expected_members = filter(__public, dir(expected))
    for member in expected_members:
        if __cmp_member(member, given, expected) is False:
            return False
    return True

def __cmp_routine(given, expected):
    result = True
    if inspect.ismethod(given):
        given = given.__func__
    if inspect.ismethod(expected):
        expected = expected.__func__

    given = inspect.getargspec(given)
    if (given.varargs, given.keywords) == (None, None):
        expected = inspect.getargspec(expected)
        defaults_len = 0 if expected.defaults is None else len(expected.defaults)
        result = len(given.args) >= len(expected.args) - defaults_len
    return result

def __cmp_member(name, given, expected):
    if hasattr(given, name) is False: return False
    given = getattr(given, name)
    if inspect.isroutine(given):
        return __cmp_routine(given, getattr(expected, name))
    return True


def __check(given, expected):
    if hasattr(expected, '__ducktypecheck__'):
        return expected.__ducktypecheck__(given)
    if inspect.isroutine(expected):
        return __cmp_routine(given, expected)
    return __is_duck(given, expected)


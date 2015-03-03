#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

class cached_property(object):
  """A property that is only computed once per instance and then replaces
  itself with an ordinary attribute. Deleting the attribute resets the
  property.
  Credit to Marcel Hellkamp, author of bottle.py.
  """

  def __init__(self, func):
    self.__doc__ = getattr(func, '__doc__')
    self.func = func

  def __get__(self, obj, cls):
    if obj is None:
        return self
    value = obj.__dict__[self.func.__name__] = self.func(obj)
    return value

def memoize(obj):
  cache = obj.cache = {}

  @functools.wraps(obj)
  def memoizer(*args, **kwargs):
    key = tuple(list(args) + sorted(kwargs.items()))
    if key not in cache:
      cache[key] = obj(*args, **kwargs)
    return cache[key]
  return memoizer

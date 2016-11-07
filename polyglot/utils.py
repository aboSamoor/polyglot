#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Collection of general utilities."""

from __future__ import print_function
from os import path
import os
import tarfile

import six
from six import text_type as unicode
from six import string_types


def _open(file_, mode='r'):
  """Open file object given filenames, open files or even archives."""
  if isinstance(file_, string_types):
    _, ext = path.splitext(file_)
    if ext in {'.bz2', '.gz'}:
      s = tarfile.open(file_)
      return s.extractfile(s.next())
    else:
      return open(file_, mode)
  return file_


def _print(text):
  """Handle the differences between Pytho2,3 print functions.
  Args:
    text (string): Should be in unicode.
  """
  if six.PY3:
    print(text)
  else:
    print(text.encode("utf8"))

def _pickle_method(method):
  """Pickle methods properly, including class methods."""
  func_name = method.im_func.__name__
  obj = method.im_self
  cls = method.im_class
  if isinstance(cls, type):
      # handle classmethods differently
      cls = obj
      obj = None
  if func_name.startswith('__') and not func_name.endswith('__'):
      #deal with mangled names
      cls_name = cls.__name__.lstrip('_')
      func_name = '_%s%s' % (cls_name, func_name)
  return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
  """Unpickle methods properly, including class methods."""

  if obj is None:
    return cls.__dict__[func_name].__get__(obj, cls)
  for cls in cls.__mro__:
    try:
      func = cls.__dict__[func_name]
    except KeyError:
      pass
    else:
      break
  return func.__get__(obj, cls)

def pretty_list(items, cols=3):
  text = []
  width = 24
  col_width = u"{" + u":<" + str(width) + u"} "
  for i, lang in enumerate(items):
    if not six.PY3:
      lang = lang.decode(u"utf-8")
    if len(lang) > width:
      lang = lang[:width-3] + "..."
    text.append(u"{:>3}. ".format(i+1))
    text.append(col_width.format(lang))
    if (i+1) % cols  == 0:
      text.append(u"\n")
  return u"".join(text)

def _decode(s, encoding="utf-8"):
  if six.PY3 and type(s) == str:
    return s.encode("utf-8").decode(encoding)
  else:
    return s.decode(encoding)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Collection of general utilities."""

from __future__ import print_function
from os import path
import os

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

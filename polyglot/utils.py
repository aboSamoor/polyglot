#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Collection of general utilities."""

from os import path
import os

from six import text_type as unicode
from six import string_types


def _open(file_, mode='r'):

  if isinstance(file_, string_types):
    _, ext = path.splitext(file_)
    if ext in {'.bz2', '.gz'}:
      s = tarfile.open(file_)
      return s.extractfile(s.next())
    else:
      return open(file_, mode)
  return file_

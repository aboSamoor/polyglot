#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic data types."""


from six.moves import zip
from six import text_type as unicode


class Sequence(object):
  """ Text with indices indicates boundaries."""

  def __init__(self, text):

    if not text:
      raise ValueError("This Sequence is Empty")
    if not isinstance(text, unicode):
      raise ValueError("This is not unicode text instead {}".format(type(text)))

    self.__text = text
    self.idx = [0, len(self.text)]

  @property
  def text(self):
    return self.__text
    
  def __iter__(self):
    for start, end in zip(self.idx[:-1], self.idx[1:]):
      yield self.text[start: end]

  def __str__(self):
    return u'\n'.join([x.strip() for x in self if x.strip()])

  def __len__(self):
    return len(self.idx) - 1

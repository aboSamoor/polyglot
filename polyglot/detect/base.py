#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Detecting languages"""

from icu import Locale
import pycld2 as cld2

class Detector(object):
  """ Detect the language used in a snippet of text.
  """
  def __init__(self, text):
    """ Detector of the language used in `text`.

    Args:
      text (string): unicode string.
    """
    self.detect(text)

  @property
  def name(self):
    return self.locale.getDisplayLanguage()

  @property
  def code(self):
    return self.locale.getName()

  def detect(self, text):
    flag, index, top_3_choices = cld2.detect(text.encode("utf-8"))
    top_choice, second_choice, third_choice = top_3_choices
    basic_name, code, confidence, bytesize = top_choice
    self.locale = Locale(code)
    self.confidence = float(confidence)
    self.read_bytes = int(bytesize)
    return self

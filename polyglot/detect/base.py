#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Detecting languages"""

from icu import Locale
import pycld2 as cld2

class Detector(object):
  def __init__(self):
    pass

  @property
  def name(self):
    return self.locale.getDisplayLanguage()

  @property
  def code(self):
    return self.locale.getName()

  def detect(self, text):
    flag, index, top_3_choices = cld2.detect(text)
    top_choice, second_choice, third_choice = top_3_choices
    basic_name, code, confidence, bytesize = top_choice
    self.locale = Locale(code)
    self.confidence = float(confidence)
    return self

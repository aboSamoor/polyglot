#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Detecting languages"""

from icu import Locale
import pycld2 as cld2

class Language(object):
  def __init__(self, choice):
    self.basic_name, code, confidence, bytesize = choice
    self.locale = Locale(code)
    self.confidence = float(confidence)
    self.read_bytes = int(bytesize)

  @property
  def name(self):
    return self.locale.getDisplayLanguage()

  @property
  def code(self):
    return self.locale.getName()

  def __str__(self):
    return ("name: {:<12}code: {:<5}confidence: {:>5.1f} "
            "read bytes:{:>6}".format(self.name, self.code,
                                    self.confidence, self.read_bytes))


class Detector(object):
  """ Detect the language used in a snippet of text.
  """
  def __init__(self, text):
    """ Detector of the language used in `text`.

    Args:
      text (string): unicode string.
    """
    self.__text = text
    self.detect(text)

  def detect(self, text):
    flag, index, top_3_choices = cld2.detect(text.encode("utf-8"))
    self.languages = [Language(x) for x in top_3_choices]
    self.language = self.languages[0]
    return self.language

  def __str__(self):
    return u"\n".join(["Language {}: {}".format(i+1, str(l))
                        for i,l in enumerate(self.languages)])

#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Detecting languages"""


import logging


from icu import Locale
import pycld2 as cld2

logger = logging.getLogger(__name__)


class Error(Exception):
  """Base exception class for this class."""


class UnknownLanguage(Error):
  """Raised if we can not detect the language of a text snippet."""


class Language(object):
  def __init__(self, choice):
    basic_name, code, confidence, bytesize = choice
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
    return ("name: {:<12}code: {:<9}confidence: {:>5.1f} "
            "read bytes:{:>6}".format(self.name, self.code,
                                    self.confidence, self.read_bytes))

  @staticmethod
  def from_code(code):
    return Language(("", code, 100, 0))


class Detector(object):
  """ Detect the language used in a snippet of text.
  """

  def __init__(self, text, quiet=False):
    """ Detector of the language used in `text`.

    Args:
      text (string): unicode string.
    """
    self.__text = text
    self.reliable = True
    """False if the detector used Best Effort strategy in detection."""
    self.quiet = quiet
    """If true, exceptions will be silenced."""
    self.detect(text)

  @staticmethod
  def supported_languages():
    """Returns a list of the languages that can be detected by pycld2."""
    return [name.capitalize() for name,code in cld2.LANGUAGES if not name.startswith("X_")]

  def detect(self, text):
    """Decide which language is used to write the text.

    The method tries first to detect the language with high reliability. If
    that is not possible, the method switches to best effort strategy.


    Args:
      text (string): A snippet of text, the longer it is the more reliable we
                     can detect the language used to write the text.
    """
    t = text.encode("utf-8")
    reliable, index, top_3_choices = cld2.detect(t, bestEffort=False)

    if not reliable:
      self.reliable = False
      reliable, index, top_3_choices = cld2.detect(t, bestEffort=True)

      if not reliable and not self.quiet:
        raise UnknownLanguage("Try passing a longer snippet of text")
      else:
        logger.warning("Detector is not able to detect the language reliably.")

    self.languages = [Language(x) for x in top_3_choices]
    self.language = self.languages[0]
    return self.language

  def __str__(self):
    text = "Prediction is reliable: {}\n".format(self.reliable)
    text += u"\n".join(["Language {}: {}".format(i+1, str(l))
                        for i,l in enumerate(self.languages)])
    return text

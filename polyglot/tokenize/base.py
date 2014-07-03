#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Basic text segmenters."""

from icu import Locale, BreakIterator
from polyglot.base import Sequence


class Breaker(object):
  """ Base class to segment text."""

  def __init__(self, locale):
    self.locale = Locale('locale')
    self.breaker = None

  def transform(self, sequence):
    seq = Sequence(sequence.text)
    seq.idx = [0]
    for segment in sequence:
      offset = seq.idx[-1]
      self.breaker.setText(segment)
      seq.idx.extend([offset+x for x in self.breaker])
    return seq

 
class SentenceTokenizer(Breaker):
  """ Segment text to sentences. """

  def __init__(self, locale='en'):
    super(SentenceTokenizer, self).__init__(locale)
    self.breaker = BreakIterator.createSentenceInstance(self.locale)


class WordTokenizer(Breaker):
  """ Segment text to words or tokens."""

  def __init__(self, locale='en'):
    super(WordTokenizer, self).__init__(locale)
    self.breaker = BreakIterator.createWordInstance(self.locale)

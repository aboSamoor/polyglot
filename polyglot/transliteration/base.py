#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Transliteration.

Transliteration across pair of languages.

"""

from math import log

from ..load import load_transliteration_table
from ..decorators import cached_property


class Transliterator(object):
  """Transliterator between pair of languages. """

  def __init__(self, source_lang="en", target_lang="en"):
    """
    Args:
      source_lang (string): language code of the input langauge.
      target_lang (string): language code of the generated output langauge.
    """
    self.source_lang = source_lang
    self.target_lang = target_lang

    self.decoder = self._decoder()
    """Transliterate a string from English to the target language."""
    self.encoder = self._encoder()
    """Transliterate a string from the input language to English."""

  def _decoder(self):
    """Transliterate a string from English to the target language."""
    if self.target_lang == 'en':
      return Transliterator._dummy_coder
    else:
      weights = load_transliteration_table(self.target_lang)
      decoder_weights = weights["decoder"]
      return Transliterator._transliterate_string(decoder_weights)

  def _encoder(self):
    """Transliterate a string from the input language to English."""
    if self.source_lang == 'en':
      return Transliterator._dummy_coder
    else:
      weights = load_transliteration_table(self.source_lang)
      encoder_weights = weights["encoder"]
      return Transliterator._transliterate_string(encoder_weights)

  @staticmethod
  def _dummy_coder(word):
    """Returns the string as it is, no transliteration is done."""
    return  word

  def transliterate(self, word):
    """Transliterate the word from its source language to the target one.

    The method works by encoding the word into English then decoding the new
    Enlgish word to the target language.
    """
    encoded_word = self.encoder(word)
    decoded_word = self.decoder(word)
    return decoded_word

  @staticmethod
  def _transliterate_string(weight, ngram1=6, ngram2=6):
    def translate_string(word):
      unlimited5 = 99999
      # Convert input to lower case
      word = word.lower().strip()
      # Initialize bestk results
      best_source_string = []
      best_target_string = []
      best_string_cost = []
      for i in range(len(word)+1):
        best_source_string.append('')
        best_target_string.append('')
        best_string_cost.append(unlimited5)
      # Only 1 initial state
      best_string_cost[0] = 0
      # Start DP to generate bestk results
      for i in range(1, len(word)+1):
        for j in range(1, ngram1+1):
          if i >= j:
            piece = word[i-j:i]
            for item in weight:
              if item[0].strip() == piece:
                vfinal = -log(weight[item])
                if best_string_cost[i - j] < unlimited5:
                  tmp_string_cost = best_string_cost[i - j]
                  # Final cost value.
                  # Things need to be considered:
                  # 1) Individual cost of tranliterating from piece to tar
                  # 2) Length of piece and tar
                  # 3) Prefix of piece
                  # 4) Prefix of tar
                  tmp_string_cost += vfinal
                  if tmp_string_cost < best_string_cost[i]:
                    tmp_source_string = best_source_string[i - j] + piece
                    tmp_target_string = best_target_string[i - j] + item[1].strip()
                    best_source_string[i] = tmp_source_string
                    best_target_string[i] = tmp_target_string
                    best_string_cost[i] = tmp_string_cost
      return best_target_string[len(word)]
    return translate_string

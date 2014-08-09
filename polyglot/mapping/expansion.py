#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import OrderedVocabulary
from collections import defaultdict
from six import iteritems
import re
import logging

logger = logging.getLogger(__name__)

class VocabExpander(OrderedVocabulary):
  def __init__(self, vocabulary, formatters, strategy):
    super(VocabExpander, self).__init__(vocabulary.words)
    self.strategy = strategy
    self._vocab = vocabulary
    self.aux_word_id = defaultdict(lambda: [])
    self.formatters = formatters
    self.expand(formatters)
    self.aux_id_word = {id_:w for w, id_ in iteritems(self.aux_word_id)}

  def __getitem__(self, key):
    try:
      return self._vocab[key]
    except KeyError as e:
      try:
        return self.aux_word_id[key]
      except KeyError as e:
        return self.approximate_ids(key)

  def __contains__(self, key):
    return ((key in self._vocab) or
            (key in self.aux_word_id) or
            self.approximate(key))

  def __len__(self):
    return len(self._vocab) + len(self.aux_word_id)
  
  def __delitem__(self):
    raise NotImplementedError("It is quite complex, let us do it in the future")

  def format(self, w):
    return [f(w) for f in self.formatters]
  
  def approximate(self, w):
    f = lambda key: (key in self._vocab) or (key in self.aux_word_id)
    return {w_:self[w_] for w_ in self.format(w) if f(w_)}
  
  def approximate_ids(self, key):
    ids = [id_ for w, id_ in self.approximate(key).items()]
    if not ids:
      raise KeyError("{} not found".format(key))
    else:
      if self.strategy == 'most_frequent':
        return min(ids)
      else:
        return tuple(sorted(ids))  

  def _expand(self, formatter):
    for w in self.word_id:
      w_ = formatter(w)
      if w_ not in self._vocab:
        id_ = self.word_id[w]
        self.aux_word_id[w_].append(id_)

  def expand(self, formatters):
    for formatter in formatters:
      self._expand(formatter)
    if self.strategy == 'average':
      self.aux_word_id = {w: tuple(sorted(ids)) for w, ids in iteritems(self.aux_word_id)}
    elif self.strategy == 'most_frequent':
      self.aux_word_id = {w: min(ids) for w, ids in iteritems(self.aux_word_id)}
    else:
      raise ValueError("A strategy is needed")

    words_added = self.aux_word_id.keys()
    old_no = len(self._vocab)
    new_no = len(self.aux_word_id)
    logger.info("We have {} original words.".format(old_no))
    logger.info("Added {} new words.".format(new_no))
    logger.info("The new total number of words is {}".format(len(self)))
    logger.debug(u"Words added\n{}\n".format(u" ".join(words_added)))


class CaseExpander(VocabExpander):
  def __init__(self, vocabulary, strategy='most_frequent'):
    formatters = [lambda x: x.lower(),
                  lambda x: x.title(),
                  lambda x: x.upper()]
    super(CaseExpander, self).__init__(vocabulary=vocabulary, formatters=formatters, strategy=strategy)

    
class DigitExpander(VocabExpander):
  def __init__(self, vocabulary, strategy='most_frequent'):
    pattern = re.compile("[0-9]", flags=re.UNICODE)
    formatters = [lambda x: pattern.sub("#", x)]
    super(DigitExpander, self).__init__(vocabulary=vocabulary, formatters=formatters, strategy=strategy)

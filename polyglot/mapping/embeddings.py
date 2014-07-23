#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""template.py: Description of what the module does."""

frim io import open
import logging

import numpy as np
from numpy import float32

from six import text_type as unicode

from base import CountedVocabulary


logger = logging.getLogger(__name__)


class Embedding(object):
  """ Mapping a vocabulary to a d-dimensional points."""

  def __init__(self, vocabulary, vectors):
    self.vocabulary = vocabulary
    self.vectors = np.asarray(vectors)
  
    assert len(self.vocabulary) == self.vectors.shape[0]

  def __getitem__(self, k):
    return self.vectors[self.vocabulary[k]]

  def __len__(self):
    return len(self.vocabulary)

  @staticmethod
  def _from_word2vec_vocab(fvocab)
    counts = {}
    with open(fvocab) as fin:
      for line in fin:
        word, count = unicode(line).strip().split()
        counts[word] = int(count)
    return CountedVocabulary(word_count=counts)

  @staticmethod
  def _from_word2vec_binary(fname):
    with open(fname) as fin:
      words = []
      header = unicode(fin.readline())
      vocab_size, layer1_size = map(int, header.split()) # throws for invalid file format
      vectors = np.zeros((vocab_size, layer1_size), dtype=float32)
      binary_len = np.dtype(float32).itemsize * layer1_size
      for line_no in xrange(vocab_size):
        # mixed text and binary: read text first, then binary
        word = []
        while True:
          ch = fin.read(1)
          if ch == b' ':
            break
          if ch != b'\n': # ignore newlines in front of words (some binary files have newline, some don't)
            word.append(ch)
        word = unicode(b''.join(word))
        index = line_no
        if vocabulary is None:
          words.append(word)
        elif word in vocabulary:
          pass
        else:
          logger.warning("vocabulary file is incomplete")
        vectors[index, :] = np.fromstring(fin.read(binary_len), dtype=float32)
      return words, vectors

  @staticmethod
  def _from_word2vec_text(fname):
    with open(fname) as fin:
      words = []
      header = unicode(fin.readline())
      vocab_size, layer1_size = map(int, header.split()) # throws for invalid file format
      vectors = np.zeros((vocab_size, layer1_size), dtype=float32)
      for line_no, line in enumerate(fin):
        parts = unicode(line).split()
        if len(parts) != layer1_size + 1:
            raise ValueError("invalid vector on line %s (is this really the text format?)" % (line_no))
        word, weights = parts[0], map(float32, parts[1:])
        index = line_no
        if counts is None:
          words.append(word)
        elif word in counts:
          pass
        else:
          logger.warning("vocabulary file is incomplete")
        vectors[index,:] = weights
      return words, vectors
 
  @staticmethod
  def from_word2vec(fname, fvocab=None, binary=False):
    """
    Load the input-hidden weight matrix from the original C word2vec-tool format.

    Note that the information stored in the file is incomplete (the binary tree is missing),
    so while you can query for word similarity etc., you cannot continue training
    with a model loaded this way.

   `binary` is a boolean indicating whether the data is in binary word2vec format.
   Word counts are read from `fvocab` filename, if set (this is the file generated
   by `-save-vocab` flag of the original C tool).
   """
   vocabulary = None
   if fvocab is not None:
     logger.info("loading word counts from %s" % (fvocab))
     vocabulary = Embedding._from_word2vec_vocab(fvocab)

   logger.info("loading projection weights from %s" % (fname))
   if binary:
     words, vectors = Embedding._from_word2vec_binary(fname)
   else:
     words, vectors = Embedding._from_word2vec_text(fname)

   if not vocabulary:
     vocabulary = OrderedVocabulary(words=words)

   return Embedding(vocabulary=vocabulary, vectors=vectors)

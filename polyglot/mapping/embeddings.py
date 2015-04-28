#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Defines classes related to mapping vocabulary to n-dimensional points."""

from io import open
import logging
from os import path
import tarfile

import numpy as np
from numpy import float32

from six import PY2
from six import text_type as unicode
from six import iteritems
from six.moves import map
from six import string_types
from six.moves import cPickle as pickle

from .base import CountedVocabulary, OrderedVocabulary
from ..utils import _open


logger = logging.getLogger(__name__)


class Embedding(object):
  """ Mapping a vocabulary to a d-dimensional points."""

  def __init__(self, vocabulary, vectors):
    self.vocabulary = vocabulary
    self.vectors = np.asarray(vectors)

    if len(self.vocabulary) != self.vectors.shape[0]:
      raise ValueError("Vocabulary has {} items but we have {} "
                       "vectors".format(len(vocabulary), self.vectors.shape[0]))

  def __getitem__(self, k):
    return self.vectors[self.vocabulary[k]]

  def __contains__(self, k):
    return k in self.vocabulary

  def __delitem__(self, k):
    """Remove the word and its vector from the embedding.

    Note:
     This operation costs \\theta(n). Be careful putting it in a loop.
    """
    index = self.vocabulary[k]
    del self.vocabulary[k]
    self.vectors = np.delete(self.vectors, index, 0)

  def __len__(self):
    return len(self.vocabulary)

  def __iter__(self):
    for w in self.vocabulary:
      yield w, self[w]

  @property
  def words(self):
    return self.vocabulary.words

  @property
  def shape(self):
    return self.vectors.shape

  def apply_expansion(self, expansion):
    """Apply a vocabulary expansion to the current emebddings."""
    self.vocabulary = expansion(self.vocabulary)

  def get(self, k, default=None):
    try:
      return self[k]
    except KeyError as e:
      return default

  def most_frequent(self, k, inplace=False):
    """Only most frequent k words to be included in the embeddings."""
    vocabulary = self.vocabulary.most_frequent(k)
    vectors = np.asarray([self[w] for w in vocabulary])
    if inplace:
      self.vocabulary = vocabulary
      self.vectors = vectors
      return self
    return Embedding(vectors=vectors, vocabulary=vocabulary)

  def normalize_words(self, ord=2, inplace=False):
    """Normalize embeddings matrix row-wise.

    Args:
      ord: normalization order. Possible values {1, 2, 'inf', '-inf'}
    """
    if ord == 2:
      ord = None # numpy uses this flag to indicate l2.
    vectors = self.vectors.T / np.linalg.norm(self.vectors, ord, axis=1)
    if inplace:
      self.vectors = vectors.T
      return self
    return Embedding(vectors=vectors.T, vocabulary=self.vocabulary)

  def nearest_neighbors(self, word, top_k=10):
    """Return the nearest k words to the given `word`.

    Args:
      word (string): single word.
      top_k (integer): decides how many neighbors to report.

    Returns:
      A list of words sorted by the distances. The closest is the first.

    Note:
      L2 metric is used to calculate distances.
    """
    #TODO(rmyeid): Use scikit ball tree, if scikit is available
    point = self[word]
    diff = self.vectors - point
    distances = np.linalg.norm(diff, axis=1)
    top_ids = distances.argsort()[1:top_k+1]
    return [self.vocabulary.id_word[i] for i in top_ids]

  def distances(self, word, words):
    """Calculate eucledean pairwise distances between `word` and `words`.

    Args:
      word (string): single word.
      words (list): list of strings.

    Returns:
      numpy array of the distances.

    Note:
      L2 metric is used to calculate distances.
    """

    point = self[word]
    vectors = np.asarray([self[w] for w in words])
    diff = vectors - point
    distances = np.linalg.norm(diff, axis=1)
    return distances

  @staticmethod
  def from_gensim(model):
    word_count = {}
    vectors = []
    for word, vocab in sorted(iteritems(model.vocab), key=lambda item: -item[1].count):
      vectors.append(model.syn0[vocab.index])
      word_count[word] = vocab.count
    vocab = CountedVocabulary(word_count=word_count)
    vectors = np.asarray(vectors)
    return Embedding(vocabulary=vocab, vectors=vectors)

  @staticmethod
  def from_word2vec_vocab(fvocab):
    counts = {}
    with _open(fvocab) as fin:
      for line in fin:
        word, count = unicode(line).strip().split()
        counts[word] = int(count)
    return CountedVocabulary(word_count=counts)

  @staticmethod
  def _from_word2vec_binary(fname):
    with _open(fname, 'rb') as fin:
      words = []
      header = unicode(fin.readline())
      vocab_size, layer1_size = list(map(int, header.split())) # throws for invalid file format
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
        word = b''.join(word)
        index = line_no
        words.append(word)
        vectors[index, :] = np.fromstring(fin.read(binary_len), dtype=float32)
      return words, vectors

  @staticmethod
  def _from_word2vec_text(fname):
    with _open(fname, 'rb') as fin:
      words = []
      header = unicode(fin.readline())
      vocab_size, layer1_size = list(map(int, header.split())) # throws for invalid file format
      vectors = []
      for line_no, line in enumerate(fin):
        try:
          parts = unicode(line, encoding="utf-8").strip().split()
        except TypeError as e:
          parts = line.strip().split()
        except Exception as e:
          logger.warning("We ignored line number {} because of erros in parsing"
                          "\n{}".format(line_no, e))
          continue
        # We differ from Gensim implementation.
        # Our assumption that a difference of one happens because of having a
        # space in the word.
        if len(parts) == layer1_size + 1:
          word, weights = parts[0], list(map(float32, parts[1:]))
        elif len(parts) == layer1_size + 2:
          word, weights = parts[:2], list(map(float32, parts[2:]))
          word = u" ".join(word)
        else:
          logger.warning("We ignored line number {} because of unrecognized "
                          "number of columns {}".format(line_no, parts[:-layer1_size]))
          continue
        index = line_no
        words.append(word)
        vectors.append(weights)
      vectors = np.asarray(vectors, dtype=np.float32)
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
      vocabulary = Embedding.from_word2vec_vocab(fvocab)

    logger.info("loading projection weights from %s" % (fname))
    if binary:
      words, vectors = Embedding._from_word2vec_binary(fname)
    else:
      words, vectors = Embedding._from_word2vec_text(fname)

    if not vocabulary:
      vocabulary = OrderedVocabulary(words=words)

    return Embedding(vocabulary=vocabulary, vectors=vectors)

  @staticmethod
  def load(fname):
    """Load an embedding dump generated by `save`"""

    content = _open(fname).read()
    if PY2:
      state = pickle.loads(content)
    else:
      state = pickle.loads(content, encoding='latin1')
    voc, vec = state
    if len(voc) == 2:
      words, counts = voc
      word_count = dict(zip(words, counts))
      vocab = CountedVocabulary(word_count=word_count)
    else:
      vocab = OrderedVocabulary(voc)
    return Embedding(vocabulary=vocab, vectors=vec)

  def save(self, fname):
    """Save a pickled version of the embedding into `fname`."""

    vec = self.vectors
    voc = self.vocabulary.getstate()
    state = (voc, vec)
    with open(fname, 'wb') as f:
      pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)

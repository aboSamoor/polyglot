#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Named entity chunker.

Detect three types of entities: {Person, Location, Organization.}

"""

import numpy as np
from six.moves import range

from ..load import load_embeddings, load_ner_model


ID_TAG = {0: 'O', 1: 'I-PER', 2:'I-LOC', 3: 'I-ORG'} 


class NEChunker(object):
  """ Named entity chunker. """
  PAD = '<PAD>'
  START = '<S>'
  END = '</S>'
  UNK = '<UNK>'

  def __init__(self, lang='en'):
    """
    Args:
      lang: language code to decide which chunker to use.
    """
    self.lang = lang
    self.embeddings = load_embeddings(self.lang, type='cw')
    self.embeddings.normalize_words(inplace=True)
    self.model = load_ner_model(lang=self.lang, version=2)
    self.predictor = self._load_network()

  def _load_network(self):
    """ Building the predictor out of the model."""
    first_layer, second_layer = self.model
    def predict_proba(input_):
      hidden = np.tanh(np.dot(first_layer, input_))
      hidden = np.hstack((hidden, np.ones((hidden.shape[0], 1))))
      output =  (second_layer *  hidden).sum(axis=1)
      output_ = 1.0/(1.0 + np.exp(-output))
      probs = output_/output_.sum()
      return probs
    return predict_proba

  @staticmethod
  def ngrams(sequence, n):
    ngrams_ = []
    seq = (n-1) * [NEChunker.PAD] + [NEChunker.START] + sequence + [NEChunker.END] + (n-1) * [NEChunker.PAD]
    for i in range(n, n+len(sequence)):
      yield seq[i-n: i+n+1]

  def annotate(self, sent):
    """Annotate a squence of words with entity tags.

    Args:
      sent: sequence of strings/words.
    """
    preds = []
    words = []
    for word, fv in self.sent2examples(sent):
      probs = self.predictor(fv)
      tags = probs.argsort()
      tag = ID_TAG[tags[-1]]

      words.append(word)
      preds.append(tag)

    # fix_chunks(preds)
    annotations = zip(words, preds)
    return annotations

  def sent2examples(self, sent):
    """ Convert ngrams into feature vectors."""

    # TODO(rmyeid): use expanders.
    words = [w if w in self.embeddings else NEChunker.UNK for w in sent]
    ngrams = NEChunker.ngrams(words, 2)
    fvs = []
    for word, ngram in zip(sent, ngrams):
      fv_ = np.array([self.embeddings[w] for w in ngram])
      fv = np.hstack((fv_.flatten(), np.array(1)))
      yield word, fv

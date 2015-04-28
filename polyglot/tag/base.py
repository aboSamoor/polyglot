#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""POS and NER Taggers.

Part of speech taggers (POS) classifies words into 17 syntactic category.
Named entity Recognition extractors (NER) Detect three types of entities: {Person, Location, Organization.}

"""

import numpy as np
from six.moves import range

from ..decorators import memoize
from ..load import load_embeddings, load_ner_model, load_pos_model


NER_ID_TAG = {0: u'O', 1: u'I-PER', 2: u'I-LOC', 3: u'I-ORG'}

POS_TAG_ID = {u'ADJ': 0, u'ADP': 1, u'ADV': 2, u'AUX': 3, u'CONJ': 4,
              u'DET': 5, u'INTJ': 6, u'NOUN': 7, u'NUM': 8, u'PART': 9,
              u'PRON': 10, u'PROPN': 11, u'PUNCT': 12, u'SCONJ': 13,
              u'SYM': 14, u'VERB': 15, u'X': 16}

POS_ID_TAG = {v:k for k,v in POS_TAG_ID.items()}

class TaggerBase(object):
  """Tagger base class that defines the interface. """
  PAD = u'<PAD>'
  START = u'<S>'
  END = u'</S>'
  UNK = u'<UNK>'

  def __init__(self, lang='en'):
    """
    Args:
      lang: language code to decide which chunker to use.
    """
    self.lang = lang
    self.predictor = self._load_network()
    self.ID_TAG = {}
    self.add_bias = True
    self.context = 2

  @staticmethod
  def ngrams(sequence, n):
    ngrams_ = []
    seq = ((n-1) * [TaggerBase.PAD] + [TaggerBase.START] +
           sequence +
           [TaggerBase.END] + (n-1) * [TaggerBase.PAD])
    for i in range(n, n+len(sequence)):
      yield seq[i-n: i+n+1]

  def _load_network(self):
    raise NotImplementedError()

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
      tag = self.ID_TAG[tags[-1]]

      words.append(word)
      preds.append(tag)

    # fix_chunks(preds)
    annotations = zip(words, preds)
    return annotations

  def sent2examples(self, sent):
    """ Convert ngrams into feature vectors."""

    # TODO(rmyeid): use expanders.
    words = [w if w in self.embeddings else TaggerBase.UNK for w in sent]
    ngrams = TaggerBase.ngrams(words, self.context)
    fvs = []
    for word, ngram in zip(sent, ngrams):
      fv = np.array([self.embeddings[w] for w in ngram]).flatten()
      if self.add_bias:
        fv = np.hstack((fv, np.array(1)))
      yield word, fv


class NEChunker(TaggerBase):
  """Named entity extractor."""

  def __init__(self, lang='en'):
    """
    Args:
      lang: language code to decide which chunker to use.
    """
    super(NEChunker, self).__init__(lang=lang)
    self.ID_TAG = NER_ID_TAG

  def _load_network(self):
    """ Building the predictor out of the model."""
    self.embeddings = load_embeddings(self.lang, type='cw')
    self.embeddings.normalize_words(inplace=True)
    self.model = load_ner_model(lang=self.lang, version=2)
    first_layer, second_layer = self.model
    def predict_proba(input_):
      hidden = np.tanh(np.dot(first_layer, input_))
      hidden = np.hstack((hidden, np.ones((hidden.shape[0], 1))))
      output =  (second_layer *  hidden).sum(axis=1)
      output_ = 1.0/(1.0 + np.exp(-output))
      probs = output_/output_.sum()
      return probs
    return predict_proba


class POSTagger(TaggerBase):
  """Universal Part of Speech Tagger."""

  def __init__(self, lang='en'):
    """
    Args:
      lang: language code to decide which chunker to use.
    """
    super(POSTagger, self).__init__(lang=lang)
    self.ID_TAG = POS_ID_TAG
    self.add_bias = False

  def _load_network(self):
    """ Building the predictor out of the model."""
    self.embeddings = load_embeddings(self.lang, type='cw')
    #self.embeddings.normalize_words(inplace=True)
    self.model = load_pos_model(lang=self.lang, version=2)

    def predict_proba(input_):
      hidden = np.tanh(np.dot(input_, self.model["W1"]) + self.model["b1"])
      output =  np.dot(hidden, self.model["W2"]) + self.model["b2"]
      scores = np.exp(output)
      probs = scores/scores.sum()
      return probs
    return predict_proba

@memoize
def get_pos_tagger(lang='en'):
  """Return a POS tagger from the models cache."""
  return POSTagger(lang=lang)

@memoize
def get_ner_tagger(lang='en'):
  """Return a NER tagger from the models cache."""
  return NEChunker(lang=lang)

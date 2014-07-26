#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test basic embedding utilities."""

import unittest
from ..embeddings import Embedding

from io import StringIO

word2vec_dump = u"""
9 5
</s> 0.001329 -0.000965 -0.001856 -0.000425 -0.000381 
the -0.144928 0.074345 -0.069327 -0.017698 0.090774
, -0.022361 -0.033252 -0.000350 -0.027688 -0.025736
. 0.006878 0.064503 0.074926 -0.048397 -0.041165
of 0.182565 0.125933 0.065001 -0.004585 0.164688
and 0.013473 0.012923 0.027855 0.046051 -0.043293
in -0.003114 -0.126757 0.099654 0.059442 0.003293
to 0.223011 -0.080497 -0.083754 -0.182311 0.057853
a -0.136669 0.161203 0.192028 0.068527 0.292363
""".strip()


class EmbeddingTest(unittest.TestCase):
  def setUp(self):
    self.fname = StringIO(word2vec_dump)
    self.model = Embedding.from_word2vec(self.fname, binary=0, fvocab=None)
    self.words = ["</s>", "the", ",", ".", "of", "and", "in", "to", "a"]

  def tearDown(self):
    pass

  def test_model_words(self):
    self.assertEqual(self.model.words, self.words)
    self.assertAlmostEqual(self.model[self.words[-1]][-1], 0.292363)

  def test_most_frequent(self):
    model = self.model.most_frequent(3)
    self.assertEqual(model.words, self.words[:3])
    self.assertEqual(model.shape, (3, 5))

  def test_model_shape(self):
    self.assertEqual(self.model.shape, (9, 5))

  def test_deletion(self):
    del self.model[self.words[5]]
    self.assertEqual(self.model.shape, (8, 5))
    self.assertEqual(self.model.words, self.words[:5]+self.words[6:])
    self.assertFalse(self.words[5] in self.model)

  def test_word_with_space(self):
    new_dump = word2vec_dump.replace("9", "10") + u"\na b 1.0 2.0 3.0 4.0 5.0"
    fname = StringIO(new_dump)
    model = Embedding.from_word2vec(fname, binary=0, fvocab=None)
    self.assertEqual(model.words[-1], u"a b")

  def test_norm(self):
    model = self.model.normalize_words()
    norms = (model.vectors ** 2).sum(axis=1)
    _ = [self.assertAlmostEqual(x,y, places=6) for x,y in zip(norms, [1.]*model.shape[0])]
    

if __name__ == "__main__":
  unittest.main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import os

from six import PY2
from six.moves import cPickle as pickle
from .utils import _open
from . import data_path
from .mapping import Embedding, CountedVocabulary

from . import data_path

if "~" in data_path:
  data_path = path.expanduser(data_path)

polyglot_path = path.join(path.abspath(data_path), "polyglot_data")


resource_dir = {
  "cw_embeddings":"embeddings2",
  "visualization": "tsne2",
  "wiki_vocab": "counts2",
  "ner2": "ner2",
  "sentiment": "sentiment2"
}


def locate_resource(name, lang, filter=None):
  """Return filename that contains specific language resource name.

  Args:
    name (string): Name of the resource.
    lang (string): language code to be loaded.
  """
  task_dir = resource_dir[name]
  p = path.join(polyglot_path, task_dir, lang)
  if not path.isdir(p):
    raise ValueError("This resource is not available "
                     "try to run\n\n$polyglot download {}.{}".format(task_dir, lang))
  return path.join(p, os.listdir(p)[0])


def load_embeddings(lang="en", task="embeddings", type="cw"):
  """Return a word embeddings object for `lang` and of type `type`

  Args:
    lang (string): language code.
    task (string): parameters that define task.
    type (string): skipgram, cw, cbow ...
  """
  src_dir = "_".join((type, task)) if type else task
  p = locate_resource(src_dir, lang)
  return Embedding.load(p)


def load_vocabulary(lang="en", type="wiki"):
  """Return a CountedVocabulary object.

  Args:
    lang (string): language code.
    type (string): wiki,...
  """
  src_dir = "{}_vocab".format(type)
  p = locate_resource(src_dir, lang)
  return CountedVocabulary.from_vocabfile(p)


def load_ner_model(lang="en", version="2"):
  """Return a word embeddings object for `lang` and of type `type`

  Args:
    lang (string): language code.
  """
  src_dir = "ner{}".format(version)
  p = locate_resource(src_dir, lang)
  fh = _open(p)
  try:
    return pickle.load(fh)
  except UnicodeDecodeError:
    fh.seek(0)
    return pickle.load(fh, encoding='latin1')

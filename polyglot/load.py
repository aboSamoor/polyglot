#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import os
from tempfile import NamedTemporaryFile

import numpy as np
import morfessor

from six import PY2
from six.moves import cPickle as pickle

from . import data_path
from .decorators import memoize
from .downloader import downloader
from .mapping import Embedding, CountedVocabulary, CaseExpander, DigitExpander

from .utils import _open

if "~" in data_path:
  data_path = path.expanduser(data_path)

polyglot_path = path.join(path.abspath(data_path), "polyglot_data")


resource_dir = {
  "cw_embeddings":"embeddings2",
  "sgns_embeddings":"sgns2",
  "visualization": "tsne2",
  "wiki_vocab": "counts2",
  "sentiment": "sentiment2",
}


def locate_resource(name, lang, filter=None):
  """Return filename that contains specific language resource name.

  Args:
    name (string): Name of the resource.
    lang (string): language code to be loaded.
  """
  task_dir = resource_dir.get(name, name)
  package_id = u"{}.{}".format(task_dir, lang)
  p = path.join(polyglot_path, task_dir, lang)
  if not path.isdir(p):
    if downloader.status(package_id) != downloader.INSTALLED:
      raise ValueError("This resource is available in the index "
                       "but not downloaded, yet. Try to run\n\n"
                       "polyglot download {}".format(package_id))
  return path.join(p, os.listdir(p)[0])


@memoize
def load_embeddings(lang="en", task="embeddings", type="cw"):
  """Return a word embeddings object for `lang` and of type `type`

  Args:
    lang (string): language code.
    task (string): parameters that define task.
    type (string): skipgram, cw, cbow ...
  """
  src_dir = "_".join((type, task)) if type else task
  p = locate_resource(src_dir, lang)
  e = Embedding.load(p)
  if type == "cw":
    e.apply_expansion(CaseExpander)
    e.apply_expansion(DigitExpander)
  if type == "sgns":
    e.apply_expansion(CaseExpander)
  return e


@memoize
def load_vocabulary(lang="en", type="wiki"):
  """Return a CountedVocabulary object.

  Args:
    lang (string): language code.
    type (string): wiki,...
  """
  src_dir = "{}_vocab".format(type)
  p = locate_resource(src_dir, lang)
  return CountedVocabulary.from_vocabfile(p)


@memoize
def load_ner_model(lang="en", version="2"):
  """Return a named entity extractor parameters for `lang` and of version `version`

  Args:
    lang (string): language code.
    version (string): version of the parameters to be used.
  """
  src_dir = "ner{}".format(version)
  p = locate_resource(src_dir, lang)
  fh = _open(p)
  try:
    return pickle.load(fh)
  except UnicodeDecodeError:
    fh.seek(0)
    return pickle.load(fh, encoding='latin1')


@memoize
def load_pos_model(lang="en", version="2"):
  """Return a part of speech tagger parameters for `lang` and of version `version`

  Args:
    lang (string): language code.
    version (string): version of the parameters to be used.
  """
  src_dir = "pos{}".format(version)
  p = locate_resource(src_dir, lang)
  fh = _open(p)
  return dict(np.load(fh))


@memoize
def load_morfessor_model(lang="en", version="2"):
  """Return a morfessor model for `lang` and of version `version`

  Args:
    lang (string): language code.
    version (string): version of the parameters to be used.
  """
  src_dir = "morph{}".format(version)
  p = locate_resource(src_dir, lang)
  file_handler = _open(p)
  tmp_file_ = NamedTemporaryFile(delete=False)
  tmp_file_.write(file_handler.read())
  tmp_file_.close()
  io = morfessor.MorfessorIO()
  model = io.read_any_model(tmp_file_.name)
  os.remove(tmp_file_.name)
  return model


@memoize
def load_transliteration_table(lang="en", version="2"):
  """Return a morfessor model for `lang` and of version `version`

  Args:
    lang (string): language code.
    version (string): version of the parameters to be used.
  """
  src_dir = "transliteration{}".format(version)
  p = locate_resource(src_dir, lang)
  file_handler = _open(p)
  return pickle.load(file_handler)

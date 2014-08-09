#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

from . import data_path
from .mapping import Embedding

from . import data_path

if "~" in data_path:
  data_path = path.expanduser(data_path)

polyglot_path = path.join(path.abspath(data_path), "polyglot_data")


resource_dir = {
  "cw_embeddings":"embeddings2",
  "visualization": "tsne2",
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
      "try to run\n\n$polyglot download {}.{}".format(name, lang))

  return path.join(p, os.listdir(p)[0])


def load_embeddings(lang="en", type="cw"):
  """Return a word embeddings object for `lang` and of type `type`

  Args:
    lang (string): language code.
    type (string): skipgram, cw, cbow ...
  """
  src_dir = "{}_embeddings".format(type)
  p = locate_resource(src_dir, lang)
  return Embedding.load(p)

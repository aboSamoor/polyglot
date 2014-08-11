#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic data types."""

from io import open, StringIO
from collections import Counter
import os
from concurrent.futures import ProcessPoolExecutor
from itertools import islice

import six
from six.moves import zip
from six import text_type as unicode
from six import iteritems
from six import string_types


class Sequence(object):
  """ Text with indices indicates boundaries."""

  def __init__(self, text):

    if not text:
      raise ValueError("This Sequence is Empty")
    if not isinstance(text, unicode):
      raise ValueError("This is not unicode text instead {}".format(type(text)))

    self.__text = text
    self.idx = [0, len(self.text)]

  @property
  def text(self):
    return self.__text

  def __iter__(self):
    for start, end in zip(self.idx[:-1], self.idx[1:]):
      yield self.text[start: end]

  def tokens(self):
    """ Returns segmented text after stripping whitespace."""

    return [x.strip() for x in self if x.strip()]

  def __str__(self):
    if six.PY3:
      return self.__unicode__()
    return self.__unicode__().encode("utf-8")

  def __unicode__(self):
    return u'\n'.join(self.tokens())

  def split(self, sequence):
    """ Split into subsequences according to `sequence`."""

    major_idx = sequence.idx
    idx2 = 0
    for start, end in zip(major_idx[:-1], major_idx[1:]):
      idx1 = self.idx.index(start, idx2)
      idx2 = self.idx.index(end, idx2)
      seq = Sequence(self.text[start:end])
      seq.idx = [x-start for x in self.idx[idx1:idx2]]
      yield seq

  def __len__(self):
    return len(self.idx) - 1

  def empty(self):
    return not self.text.strip()


class TokenSequence(list):
  """A list of tokens.

  Args:
   tokens (list): list of symbols.
  """

  def sliding_window(self, width=2, padding=None):
    seq = self
    if padding:
      pad = [padding for x in range(width/2)]
      seq = pad + self + pad
    args = [islice(seq, i, None)  for i in range(width)]
    for x in zip(*args):
      yield x


class TextFile(object):
  """ Wrapper around text files.

      It uses io.open to guarantee reading text files with unicode encoding.
      It has an iterator that supports arbitrary delimiter instead of only
      new lines.

  Attributes:
    delimiter (string): A string that defines the limit of each chunk.
    file (string): A path to a file.
    buf (StringIO): a buffer to store the results of peeking into the file.
  """

  def __init__(self, file, delimiter=u'\n'):
    self.name = file
    self.delimiter = delimiter
    self.open_file = open(file, 'r')
    self.buf = StringIO()

  def iter_delimiter(self, byte_size=8192):
    """ Generalization of the default iter file delimited by '\n'.
    Note:
      The newline string can be arbitrarily long; it need not be restricted to a
      single character. You can also set the read size and control whether or not
      the newline string is left on the end of the iterated lines.  Setting
      newline to '\0' is particularly good for use with an input file created with
      something like "os.popen('find -print0')".

    Args:
      byte_size (integer): Number of bytes to be read at each time.
    """
    partial = u''
    while True:
      read_chars = self.read(byte_size)
      if not read_chars: break
      partial += read_chars
      lines = partial.split(self.delimiter)
      partial = lines.pop()

      for line in lines:
        yield line + self.delimiter

    if partial:
      yield partial

  def __iter__(self):
    for l in self.iter_delimiter():
      yield l

  def iter_chunks(self, chunksize):
    chunk = []
    for i, l in enumerate(self):
      chunk.append(l)
      if i % chunksize == chunksize -1:
        yield chunk
        chunk = []
    if chunk:
      yield chunk

  def _append_to_buf(self, contents):
    oldpos = self.buf.tell()
    self.buf.seek(0, os.SEEK_END)
    self.buf.write(contents)
    self.buf.seek(oldpos)

  def peek(self, size):
    contents = self.open_file.read(size)
    self._append_to_buf(contents)
    return contents

  def read(self, size=None):
    """ Read `size` of bytes."""
    if size is None:
      return self.buf.read() + self.open_file.read()
    contents = self.buf.read(size)
    if len(contents) < size:
      contents += self.open_file.read(size - len(contents))
    return contents

  def readline(self):
    line = self.buf.readline()
    if not line.endswith('\n'):
      line += self.open_file.readline()
    return line

  def apply(self, func, workers=1, job_size=10000):
    """Apply `func` to lines of text in parallel or sequential.

    Args:
      func : a function that takes a list of lines.
    """
    if workers == 1:
      for lines in self.iter_chunks(job_size):
        yield func(lines)
    else:
      with ProcessPoolExecutor(max_workers=workers) as executor:
        for result in executor.map(func, self.iter_chunks(job_size)):
          yield result


class TextFiles(TextFile):
  """Interface for a sequence of files."""

  def __init__(self, files, delimiter=u'\n'):
    if isinstance(files[0], string_types):
      self.files = [TextFile(f) for f in files]
    self.files = files
    self.delimiter = delimiter
    self.buf = StringIO()
    self.i = 0
    self.open_file = self.files[self.i].open_file

  def readline(self):
    raise NotImplementedError("Future work")

  def peek(self, size):
    self.open_file.seek(0)
    contents = self.open_file.read(size)
    self.open_file.seek(0)
    return contents

  def read(self, size=None):
    content = super(TextFiles, self).read(size)
    if not content and self.i < len(self.files)-1:
      self.i += 1
      self.buf = StringIO()
      self.open_file = self.files[self.i].open_file
      return self.read(size)
    return content

  @property
  def names(self):
    return [f.name for f in self.files]

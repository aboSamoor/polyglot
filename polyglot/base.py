#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic data types."""

from io import open, StringIO
from collections import Counter
import os

from six.moves import zip
from six import text_type as unicode
from six import iteritems


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
    return u'\n'.join(self.tokens()).encode('utf8')

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



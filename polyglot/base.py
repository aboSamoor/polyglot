#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic data types."""

from io import open
from collections import Counter

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
  """

  def __init__(self, file, delimiter=u'\n'):
    self.delimiter = delimiter
    self.open_file = open(file, 'r')

  def iter_delimiter(self, chunk_size=8192):
    """ Generalization of the default iter file delimited by '\n'.

       The newline string can be arbitrarily long; it need not be restricted to a
       single character. You can also set the read size and control whether or not
       the newline string is left on the end of the iterated lines.  Setting
       newline to '\0' is particularly good for use with an input file created with
       something like "os.popen('find -print0')".
    """
    partial = u''
    while True:
      read_chars = self.open_file.read(chunk_size)
      if not read_chars: break
      partial += read_chars
      lines = partial.split(self.delimiter)
      partial = lines.pop()

      for line in lines:
        yield line + self.delimiter

    if partial:
      yield partial

  def __iter__(self):
    if self.delimiter == u'\n':
      for l in self.open_file:
        yield l
    else:
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


def count(lines):
  """ Counts the word frequences in a list of sentences.

  Note:
    This is a helper function for parallel execution of `Vocabulary.from_text`
    method.
  """
  words = [w for l in lines for w in l.strip().split()]
  return Counter(words)


class Vocabulary(object):
  """ Storing the vocabulary with their ids [and counts if available].

  Attributes:
    word_id (dictionary): Mapping from words to IDs.
    id_word (dictionary): A reverse map of `word_id`.
  """

  def __init__(self, words=None, word_count=None):
    """ Build attributes word_id and id_word from input.

    Note:
      Either words or word_count should be passed.
      IDs will be given according to the lexicographic order of words,
      if words is passed. Or according to the word count if word_count is used.

    Args:
      words (list): list of words.
      word_count (dictionary): A dictionary of the type word:count or
                               list of tuples of the type (word, count).
    """

    if words is None and word_count is None:
      raise ValueError("Either words or word_count should be passed.")

    if words is not None:
      self.word_id = {w:i for i, w in enumerate(sorted(words))}

    if word_count is not None:
      if isinstance(word_count, dict):
        word_count = iteritems(word_count)
      sorted_counts = sorted(word_count, key=lambda (x,y): y, reverse=True)
      self.word_id = {w:i for i,(w,c) in enumerate(sorted_counts)}
      self.word_count = {w:c for (w,c) in sorted_counts}

    self.id_word = {i:w for w,i in iteritems(self.word_id)}

  @staticmethod
  def from_textfile(textfile, workers=1, job_size=1000):
    """ Count the set of words appeared in a text file.

    Args:
      textfile (string): The name of the text file or `TextFile` object.
      min_count (integer): Minimum number of times a word/token appeared in the document
                 to be considered part of the vocabulary.
      workers (integer): Number of parallel workers to read the file simulatenously.
      job_size (integer): Size of the batch send to each worker.
      most_frequent (integer): if no min_count is specified, consider the most frequent k words for the vocabulary.

    Returns:
      A vocabulary of the most frequent words appeared in the document.
    """

    c = Counter()
    if isinstance(textfile, unicode):
      textfile = TextFile(textfile)
    if workers == 1:
      for lines in textfile.iter_chunks(job_size):
        c.update(count(lines))
    else:
      with ProcessPoolExecutor(max_workers=workers) as executor:
        for counter_ in executor.map(count, textfile.iter_chunks(job_size)):
          c.update(counter_)

    return Vocabulary(word_count=c)

  @property
  def words(self):
    if self.word_count:
      return [w for w,c in
              sorted(iteritems(self.word_count), key=lambda (x,y): y, reverse=True)]
    else:
      return [w for w,id_ in sorted(iteritems(self.word_id), key=lambda (x,y): y)]

  def most_frequent(self, k):
    """ Returns a vocabulary with the most frequent `k` words.

    Args:
      k (integer): specifies the top k most frequent words to be returned.
    """
    if not hasattr(self, 'word_count'):
      raise ValueError("This vocabulary object does not contain word count "
                        "information.")
    wc = iteritems(self.word_count)
    word_count = list(sorted(wc, key=lambda (x,y): y, reverse=True))
    word_count = dict(word_count[:k])
    return Vocabulary(word_count=word_count)

  def min_count(self, n=1):
    """ Returns a vocabulary after eliminating the words that appear < `n`.

    Args:
      n (integer): specifies the minimum word frequency allowed.
    """
    if not hasattr(self, 'word_count'):
      raise ValueError("This vocabulary object does not contain word count "
                        "information.")

    word_count = {w:c for w,c in iteritems(self.word_count) if c >= n}
    return Vocabulary(word_count=word_count)

  def __str__(self):
    if hasattr(self, 'word_count'):
      return u"\n".join([u"{}\t{}".format(w,self.word_count[w]) for w in self.words])
    else:
      return u"\n".join(self.words)

  def __getitem__(self, key):
    return self.word_id[key]

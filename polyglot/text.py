#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import numpy as np

from polyglot.base import Sequence, TextFile, TextFiles
from polyglot.detect import Detector, Language
from polyglot.decorators import cached_property
from polyglot.downloader import Downloader
from polyglot.load import load_embeddings, load_morfessor_model
from polyglot.mapping import CountedVocabulary
from polyglot.mixins import BlobComparableMixin, StringlikeMixin
from polyglot.tag import get_pos_tagger, get_ner_tagger
from polyglot.tokenize import SentenceTokenizer, WordTokenizer
from polyglot.transliteration import Transliterator
from polyglot.utils import _print

from .mixins import basestring

import six
from six import text_type as unicode

class BaseBlob(StringlikeMixin, BlobComparableMixin):
  """An abstract base class that Sentence, Text will inherit from.
  Includes words, POS tag, NP, and word count properties. Also includes
  basic dunder and string methods for making objects like Python strings.
  :param text: A string.
  """

  def __init__(self, text):
    if not isinstance(text, basestring):
        raise TypeError('The `text` argument passed to `__init__(text)` '
                        'must be a unicode string, not {0}'.format(type(text)))
    self.raw = text
    if not isinstance(text, unicode):
      self.raw = text.decode("utf-8")

    self.string = self.raw
    self.__lang = None

  @cached_property
  def detected_languages(self):
    return Detector(self.raw, quiet=True)

  @property
  def language(self):
    if self.__lang is None:
      self.__lang = self.detected_languages.language
    return self.__lang

  @language.setter
  def language(self, value):
    self.__lang = Language.from_code(value)

  @property
  def word_tokenizer(self):
    word_tokenizer = WordTokenizer(locale=self.language.code)
    return word_tokenizer

  @property
  def words(self):
    """Return a list of word tokens. This excludes punctuation characters.
    If you want to include punctuation characters, access the ``tokens``
    property.
    :returns: A :class:`WordList <WordList>` of word tokens.
    """
    return self.tokens

  @cached_property
  def tokens(self):
    """Return a list of tokens, using this blob's tokenizer object
    (defaults to :class:`WordTokenizer <textblob.tokenizers.WordTokenizer>`).
    """
    seq = self.word_tokenizer.transform(Sequence(self.raw))
    return WordList(seq.tokens(), parent=self, language=self.language.code)

  def tokenize(self, tokenizer=None):
    """Return a list of tokens, using ``tokenizer``.
    :param tokenizer: (optional) A tokenizer object. If None, defaults to
        this blob's default tokenizer.
    """
    t = tokenizer if tokenizer is not None else self.tokenizer
    return WordList(t.tokenize(self.raw), parent=self)

  @cached_property
  def polarity(self):
    """Return the polarity score as a float within the range [-1.0, 1.0]
    """
    scores = [w.polarity for w in self.words if w.polarity != 0]
    return sum(scores) / float(len(scores))

  @cached_property
  def ne_chunker(self):
    return get_ner_tagger(lang=self.language.code)

  @cached_property
  def pos_tagger(self):
    return get_pos_tagger(lang=self.language.code)

  @cached_property
  def morpheme_analyzer(self):
    return load_morfessor_model(lang=self.language.code)

  def transliterate(self, target_language="en"):
    """Transliterate the string to the target language."""
    return WordList([w.transliterate(target_language) for w in self.words],
                     language=target_language, parent=self)

  @cached_property
  def morphemes(self):
    words, score = self.morpheme_analyzer.viterbi_segment(self.raw)
    return WordList(words, language=self.language.code, parent=self)


  @cached_property
  def entities(self):
    """Returns a list of entities for this blob."""
    start = 0
    end = 0
    prev_tag = u'O'
    chunks = []
    for i, (w, tag) in enumerate(self.ne_chunker.annotate(self.words)):
      if tag != prev_tag:
        if prev_tag == u'O':
          start = i
        else:
          chunks.append(Chunk(self.words[start: i], start, i, tag=prev_tag,
                              parent=self))
        prev_tag = tag
    if tag != u'O':
      chunks.append(Chunk(self.words[start: i+1], start, i+1, tag=tag,
                          parent=self))
    return chunks

  @cached_property
  def pos_tags(self):
    """Returns an list of tuples of the form (word, POS tag).
    Example:
    ::
        [('At', 'ADP'), ('eight', 'NUM'), ("o'clock", 'NOUN'), ('on', 'ADP'),
        ('Thursday', 'NOUN'), ('morning', 'NOUN')]
    :rtype: list of tuples
    """
    tagged_words = []
    for word,t in self.pos_tagger.annotate(self.words):
      word.pos_tag = t
      tagged_words.append((word, t))
    return tagged_words

  @cached_property
  def word_counts(self):
    """Dictionary of word frequencies in this text.
    """
    counts = defaultdict(int)
    for word in self.words:
        counts[word] += 1
    return counts

  @cached_property
  def np_counts(self):
    """Dictionary of noun phrase frequencies in this text.
    """
    counts = defaultdict(int)
    for phrase in self.noun_phrases:
        counts[phrase] += 1
    return counts

  def ngrams(self, n=3):
    """Return a list of n-grams (tuples of n successive words) for this
    blob.
    :rtype: List of :class:`WordLists <WordList>`
    """
    if n <= 0:
        return []
    grams = [WordList(self.words[i:i+n], parent=self)
                        for i in range(len(self.words) - n + 1)]
    return grams

  def detect_language(self):
    """Detect the blob's language using the Google Translate API.
    Requires an internet connection.
    Usage:
    ::
        >>> b = Text("bonjour")
        >>> b.language
        u'fr'
    """
    return self.language.code

  def correct(self):
    """Attempt to correct the spelling of a blob.
    .. versionadded:: 0.6.0
    :rtype: :class:`BaseBlob <BaseBlob>`
    """
    # regex matches: contraction or word or punctuation or whitespace
    tokens = nltk.tokenize.regexp_tokenize(self.raw, "\w*('\w*)+|\w+|[^\w\s]|\s")
    corrected = (Word(w).correct() for w in tokens)
    ret = ''.join(corrected)
    return self.__class__(ret)

  def _cmpkey(self):
    """Key used by ComparableMixin to implement all rich comparison
    operators.
    """
    return self.raw

  def _strkey(self):
    """Key used by StringlikeMixin to implement string methods."""
    return self.raw

  def __hash__(self):
    return hash(self._cmpkey())

  def __add__(self, other):
    '''Concatenates two text objects the same way Python strings are
    concatenated.
    Arguments:
    - `other`: a string or a text object
    '''
    if isinstance(other, basestring):
        return self.__class__(self.raw + other)
    elif isinstance(other, BaseBlob):
        return self.__class__(self.raw + other.raw)
    else:
        raise TypeError('Operands must be either strings or {0} objects'
            .format(self.__class__.__name__))

  def split(self, sep=None, maxsplit=sys.maxsize):
    """Behaves like the built-in str.split() except returns a
    WordList.
    :rtype: :class:`WordList <WordList>`
    """
    return WordList(self._strkey().split(sep, maxsplit), parent=self)


class Word(unicode):

  """A simple word representation. Includes methods for inflection,
  translation, and WordNet integration.
  """

  def __new__(cls, string, language=None, pos_tag=None):
    """Return a new instance of the class. It is necessary to override
    this method in order to handle the extra pos_tag argument in the
    constructor.
    """
    return super(Word, cls).__new__(cls, string)

  def __init__(self, string, language=None, pos_tag=None):
    self.string = string
    self.pos_tag = pos_tag
    self.__lang = language

  def __repr__(self):
      return repr(self.string)

  def __str__(self):
    return self.string


  @cached_property
  def morpheme_analyzer(self):
    return load_morfessor_model(lang=self.language)

  @cached_property
  def morphemes(self):
    words, score = self.morpheme_analyzer.viterbi_segment(self.string)
    return WordList(words, parent=self, language=self.language)

  @cached_property
  def detected_languages(self):
    return Detector(self.string, quiet=True)

  @property
  def language(self):
    if self.__lang is None:
      self.__lang = self.detected_languages.language.code
    return self.__lang

  @language.setter
  def language(self, value):
    self.__lang = value

  @property
  def vector(self):
    embeddings = load_embeddings(lang=self.language, type="sgns",
                                 task="embeddings")
    return embeddings[self.string]

  @property
  def neighbors(self):
    embeddings = load_embeddings(lang=self.language, type="sgns",
                                 task="embeddings")
    return embeddings.nearest_neighbors(self.string)

  @property
  def polarity(self):
    embeddings = load_embeddings(lang=self.language, type="", task="sentiment")
    return embeddings.get(self.string, [0])[0]

  def detect_language(self):
    """Detect the word's language."""
    return self.language

  def transliterate(self, target_language="en"):
    """Transliterate the string to the target language."""
    t = Transliterator(source_lang=self.language,
                       target_lang=target_language)
    return t.transliterate(self.string)


class WordList(list):
  """A list-like collection of words."""

  def __init__(self, collection, parent=None, language="en"):
    """Initialize a WordList. Takes a collection of strings as
    its only argument.
    """
    self._collection = [Word(w, language=language) for w in collection]
    self.parent = parent
    super(WordList, self).__init__(self._collection)

  def __str__(self):
    return str(self._collection)

  def __repr__(self):
    """Returns a string representation for debugging."""
    class_name = self.__class__.__name__
    return '{cls}({lst})'.format(cls=class_name, lst=repr(self._collection))

  def __getitem__(self, key):
    """Returns a string at the given index."""
    if isinstance(key, slice):
        return self.__class__(self._collection[key])
    else:
        return self._collection[key]

  def __getslice__(self, i, j):
    # This is included for Python 2.* compatibility
    return self.__class__(self._collection[i:j])

  def __iter__(self):
    return iter(self._collection)

  def count(self, strg, case_sensitive=False, *args, **kwargs):
    """Get the count of a word or phrase `s` within this WordList.
    :param strg: The string to count.
    :param case_sensitive: A boolean, whether or not the search is case-sensitive.
    """
    if not case_sensitive:
        return [word.lower() for word in self].count(strg.lower(), *args,
                **kwargs)
    return self._collection.count(strg, *args, **kwargs)

  def append(self, obj):
    """Append an object to end. If the object is a string, appends a
    :class:`Word <Word>` object.
    """
    if isinstance(obj, basestring):
        return self._collection.append(Word(obj))
    else:
        return self._collection.append(obj)

  def extend(self, iterable):
    """Extend WordList by appending elements from ``iterable``. If an element
    is a string, appends a :class:`Word <Word>` object.
    """
    [self._collection.append(Word(e) if isinstance(e, basestring) else e)
        for e in iterable]
    return self

  def upper(self):
    """Return a new WordList with each word upper-cased."""
    return self.__class__([word.upper() for word in self])

  def lower(self):
    """Return a new WordList with each word lower-cased."""
    return self.__class__([word.lower() for word in self])


class Chunk(WordList):
  """A subsequence within a WordList object. Inherits from :class:`WordList <WordList>`.
  :param subsequence: A list, the raw sentence.
  :param start_index: An int, the index where this chunk begins
                      in WordList. If not given, defaults to 0.
  :param end_index: An int, the index where this chunk ends in
                      a WordList. If not given, defaults to the
                      length of the sentence - 1.
  :param parent: Original Baseblob.
  """

  def __init__(self, subsequence, start_index=0, end_index=None, tag="",
               parent=None):
    super(Chunk, self).__init__(collection=subsequence, parent=parent)
    #: The start index within a Text
    self.start = start_index
    #: The end index within a Text
    self.end = end_index or len(sentence) - 1
    class_name = self.__class__.__name__
    self.tag = tag if tag else class_name


  def __repr__(self):
    """Returns a string representation for debugging."""
    return '{tag}({lst})'.format(tag=self.tag, lst=repr(self._collection))

  @cached_property
  def positive_sentiment(self):
    """Positive sentiment of the entity."""
    pos, neg = self._sentiment()
    return pos

  @cached_property
  def negative_sentiment(self):
    """Negative sentiment of the entity."""
    pos, neg = self._sentiment()
    return neg

  def _sentiment(self, distance=True):
    """Calculates the sentiment of an entity as it appears in text."""
    sum_pos = 0
    sum_neg = 0
    text = self.parent
    entity_positions = range(self.start, self.end)
    non_entity_positions = set(range(len(text.words))).difference(entity_positions)
    if not distance:
      non_entity_polarities = np.array([text.words[i].polarity for i in non_entity_positions])
      sum_pos = sum(non_entity_polarities == 1)
      sum_neg = sum(non_entity_polarities == -1)
    else:
      polarities = np.array([w.polarity for w in text.words])
      polarized_positions = np.argwhere(polarities != 0)[0]
      polarized_non_entity_positions = non_entity_positions.intersection(polarized_positions)
      sentence_len = len(text.words)
      for i in polarized_non_entity_positions:
        min_dist = min(abs(self.start - i), abs(self.end - i))
        if text.words[i].polarity == 1:
          sum_pos += 1.0 - (min_dist - 1.0) / (2.0 * sentence_len)
        else:
          sum_neg += 1.0 - (min_dist - 1.0) / (2.0 *sentence_len)
    return (sum_pos, sum_neg)


class Sentence(BaseBlob):
  """A sentence within a Text object. Inherits from :class:`BaseBlob <BaseBlob>`.
  :param sentence: A string, the raw sentence.
  :param start_index: An int, the index where this sentence begins
                      in Text. If not given, defaults to 0.
  :param end_index: An int, the index where this sentence ends in
                      a Text. If not given, defaults to the
                      length of the sentence - 1.
  """

  def __init__(self, sentence, start_index=0, end_index=None):
    super(Sentence, self).__init__(sentence)
    #: The start index within a Text
    self.start = start_index
    #: The end index within a Text
    self.end = end_index or len(sentence) - 1

  @property
  def dict(self):
    '''The dict representation of this sentence.'''
    return {
        'raw': self.raw,
        'start_index': self.start_index,
        'end_index': self.end_index,
        'entities': self.entities,
        'polarity': self.polarity,
    }


class Text(BaseBlob):
  """.
  """

  def __init__(self, text):
    super(Text, self).__init__(text)

  def __str__(self):
    if len(self.raw) > 1000:
      return u"{}...{}".format(self.raw[:500], self.raw[-500:])
    else:
      return self.raw

  @property
  def sentences(self):
    """Return list of :class:`Sentence <Sentence>` objects."""
    return self._create_sentence_objects()

  @property
  def raw_sentences(self):
    """List of strings, the raw sentences in the blob."""
    return [sentence.raw for sentence in self.sentences]

  @property
  def serialized(self):
    """Returns a list of each sentence's dict representation."""
    return [sentence.dict for sentence in self.sentences]

  def to_json(self, *args, **kwargs):
    '''Return a json representation (str) of this blob.
    Takes the same arguments as json.dumps.
    .. versionadded:: 0.5.1
    '''
    return json.dumps(self.serialized, *args, **kwargs)

  @property
  def json(self):
    '''The json representation of this blob.
    .. versionchanged:: 0.5.1
        Made ``json`` a property instead of a method to restore backwards
        compatibility that was broken after version 0.4.0.
    '''
    return self.to_json()

  def _create_sentence_objects(self):
    '''Returns a list of Sentence objects from the raw text.
    '''
    sentence_objects = []
    sent_tokenizer = SentenceTokenizer(locale=self.language.code)
    seq = Sequence(self.raw)
    seq = sent_tokenizer.transform(seq)
    for start_index, end_index in zip(seq.idx[:-1], seq.idx[1:]):
      # Sentences share the same models as their parent blob
      sent = seq.text[start_index: end_index].strip()
      if not sent: continue
      s = Sentence(sent, start_index=start_index, end_index=end_index)
      s.detected_languages = self.detected_languages
      sentence_objects.append(s)
    return sentence_objects

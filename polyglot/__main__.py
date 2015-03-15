#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from io import open
from argparse import ArgumentParser, FileType
from collections import Counter
from signal import signal, SIGPIPE, SIG_DFL
import logging

import six
from six import text_type as unicode
from six import iteritems

from icu import Locale

from polyglot.base import Sequence, TextFile, TextFiles
from polyglot.detect import Detector
from polyglot.downloader import Downloader
from polyglot.load import load_morfessor_model
from polyglot.mapping import CountedVocabulary
from polyglot.tag import NEChunker, POSTagger
from polyglot.tokenize import SentenceTokenizer, WordTokenizer
from polyglot.transliteration import Transliterator
from polyglot.utils import _print

signal(SIGPIPE, SIG_DFL)
logger = logging.getLogger(__name__)
LOGFORMAT = "%(asctime).19s %(levelname)s %(filename)s: %(lineno)s %(message)s"


def vocab_counter(args):
  """Calculate the vocabulary."""
  if isinstance(args.input, TextFiles):
    v = CountedVocabulary.from_textfiles(args.input, workers=args.workers)
  else:
    v = CountedVocabulary.from_textfile(args.input, workers=args.workers)
  if args.min_count > 1: 
    v = v.min_count(args.min_count)
  if args.most_freq > 0:
    v = v.most_frequent(args.most_freq)
  print(v)


def detect(args):
  """ Detect the language of each line."""
  for l in args.input:
    if l.strip():
      _print("{:<20}{}".format(Detector(l).language.name, l.strip()))


def tag(tagger, args):
  """Chunk named entities."""
  for l in args.input:
    words = l.strip().split()
    line_annotations = [u"{:<16}{:<5}".format(w,p) for w, p in tagger.annotate(words)]
    _print(u"\n".join(line_annotations))
    _print(u"")


def transliterate(args):
  """Transliterate words according to the target language."""
  t = Transliterator(source_lang=args.lang,
                     target_lang=args.target)
  for l in args.input:
    words = l.strip().split()
    line_annotations = [u"{:<16}{:<16}".format(w, t.transliterate(w)) for w in words]
    _print(u"\n".join(line_annotations))
    _print(u"")


def morphemes(args):
  """Segment words according to their morphemes."""
  morfessor = load_morfessor_model(lang=args.lang)
  for l in args.input:
    words = l.strip().split()
    morphemes = [(w, u"_".join(morfessor.viterbi_segment(w)[0])) for w in words]
    line_annotations = [u"{:<16}{:<5}".format(w,p) for w, p in morphemes]
    _print(u"\n".join(line_annotations))
    _print(u"")


def ner_chunk(args):
  """Chunk named entities."""
  chunker = NEChunker(lang=args.lang)
  tag(chunker, args)


def pos_tag(args):
  """Tag words with their part of speech."""
  tagger = POSTagger(lang=args.lang)
  tag(tagger, args)


def cat(args):
  """ Concatenate the content of the input file."""
  for l in args.input:
    _print(l.strip())


def download(args):
  """ Download polyglot packages and models."""

  downloader = Downloader(server_index_url = args.server_index_url)
  if args.packages:
    for pkg_id in args.packages:
      rv = downloader.download(info_or_id=unicode(pkg_id), download_dir=args.dir,
                               quiet=args.quiet, force=args.force,
                               halt_on_error=args.halt_on_error)
      if rv == False and args.halt_on_error:
        break
  else:
    downloader.download(download_dir=args.dir, quiet=args.quiet, force=args.force,
                        halt_on_error=args.halt_on_error)


def segment(args):
  lang  = args.lang
  w_tokenizer = WordTokenizer(locale=lang)
  s_tokenizer = SentenceTokenizer(locale=lang)

  if args.only_sent:
    for l in args.input:
      seq = Sequence(l)
      if not seq.empty(): _print(s_tokenizer.transform(seq))

  elif args.only_word:
    for l in args.input:
      seq = Sequence(l)
      if not seq.empty(): _print(w_tokenizer.transform(seq))

  else:
    for l in args.input:
      seq = Sequence(l)
      sents = s_tokenizer.transform(seq)
      words = w_tokenizer.transform(seq)
      for tokenized_sent in words.split(sents):
        if not tokenized_sent.empty():
          _print(u' '.join(tokenized_sent.tokens()))


def remove_escape(text):
  if six.PY3:
    return unicode(text.encode("utf8").decode('unicode-escape'))
  return unicode(text.decode('unicode-escape'))


def debug(type_, value, tb):
  if hasattr(sys, 'ps1') or not sys.stderr.isatty():
    sys.__excepthook__(type_, value, tb)
  else:
    import traceback
    import pdb
    traceback.print_exception(type_, value, tb)
    print(u"\n")
    pdb.pm()


def main():
  parser = ArgumentParser("polyglot",
                          conflict_handler='resolve')
  subparsers = parser.add_subparsers(title='tools',
                                     description='multilingual tools for all languages')
  parser.add_argument('--lang', default='detect', help='Language to be processed')
  parser.add_argument('--delimiter', default=u'\n', help='Delimiter that '
                      'seperates documents, records or even sentences.')
  parser.add_argument('--workers', default=1, type=int,
                      help='Number of parallel processes.')
  parser.add_argument("-l", "--log", dest="log", help="log verbosity level",
                      default="INFO")
  parser.add_argument("--debug", dest="debug", action='store_true', default=False,
                      help="drop a debugger if an exception is raised.")

  # Language detector
  detector = subparsers.add_parser('detect',
                                   help="Detect the language(s) used in text.")
  detector.set_defaults(func=detect)

  # Morphological Analyzer
  morph = subparsers.add_parser('morph')
  morph.set_defaults(func=morphemes)

  # Tokenizer
  tokenizer = subparsers.add_parser('tokenize',
                                    help="Tokenize text into sentences and words.")
  group1= tokenizer.add_mutually_exclusive_group()
  group1.add_argument("--only-sent", default=False, action="store_true",
                      help="Segment sentences without word tokenization")
  group1.add_argument("--only-word", default=False, action="store_true",
                      help="Tokenize words without sentence segmentation")
  tokenizer.set_defaults(func=segment)

  # Package downloader
  downloader = subparsers.add_parser('download',
                                     help="Download polyglot resources and models.")
  downloader.add_argument("packages", nargs='*',
                          help="packages to be downloaded")
  downloader.add_argument("--dir", dest="dir",
                          help="download package to directory DIR", metavar="DIR")
  downloader.add_argument("--quiet", dest="quiet", action="store_true",
                          default=False, help="work quietly")
  downloader.add_argument("--force", dest="force", action="store_true",
                          default=False, help="download even if already installed")
  downloader.add_argument("--exit-on-error", dest="halt_on_error", action="store_true",
                          default=False, help="exit if an error occurs")
  downloader.add_argument("--url", dest="server_index_url",
                          default=None, help="download server index url")
  downloader.set_defaults(func=download)

  # Vocabulary Counter
  counter = subparsers.add_parser('count',
                                  help="Count words frequency in a corpus.")
  group1= counter.add_mutually_exclusive_group()
  group1.add_argument("--min-count", type=int, default=1,
                      help="Ignore all words that appear <= min_freq.")
  group1.add_argument("--most-freq", type=int, default=-1,
                      help="Consider only the most frequent k words.")
  counter.set_defaults(func=vocab_counter)

  # Concatenate the input file
  catter = subparsers.add_parser('cat',
                                 help="Print the contents of the input file to the screen.")
  catter.set_defaults(func=cat)

  # Named Entity Chunker
  ner = subparsers.add_parser('ner',
                              help="Named entity recognition chunking.")
  ner.set_defaults(func=ner_chunk)

  # Part of Speech Tagger
  ner = subparsers.add_parser('pos',
                              help="Part of Speech tagger.")
  ner.set_defaults(func=pos_tag)

  # Transliteration
  transliterator = subparsers.add_parser('transliteration',
                                         help="Rewriting the input in the "
                                              "target language script.")
  transliterator.add_argument("--target", default="en",
                              help="Language code of the target language.")
  transliterator.set_defaults(func=transliterate)

  # Sentiment Analysis
  senti = subparsers.add_parser('sentiment',
                                help="Classify text to positive and negative polarity.")
  for name, subparser in parser._subparsers._group_actions[0].choices.items():
    if name == 'download': continue
    subparser.add_argument('--input', nargs='*', type=TextFile,
                           default=[TextFile(sys.stdin.fileno())])

  args = parser.parse_args()
  numeric_level = getattr(logging, args.log.upper(), None)
  logging.basicConfig(format=LOGFORMAT)
  logger.setLevel(numeric_level)

  if args.debug:
   sys.excepthook = debug 

  #parser.set_defaults(func=cat)

  language_agnostic = {detect, vocab_counter}

  if args.func != download:
    if len(args.input) > 1:
      args.input = TextFiles(args.input)
    else:
      args.input = args.input[0]

    if args.lang == 'detect' and args.func not in language_agnostic:
      header = 4096
      text = args.input.peek(header)
      lang = Detector(text).language
      args.lang = lang.code
      logger.info("Language {} is detected while reading the first {} bytes"
                  ".".format(lang.name, lang.read_bytes))

    args.delimiter = remove_escape(args.delimiter)
    args.input.delimiter = args.delimiter
  args.func(args)

if __name__ == '__main__':
  sys.exit(main())

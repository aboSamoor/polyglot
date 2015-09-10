#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Polyglot Toolkit: Corpus & Model Downloader
#
# Copyright (C) 2014-2015 Polyglot Project
# Author: Rami Al-Rfou <rmyeid@gmail.com>
# URL: <http://bit.ly/embeddings/>
# For license information, see LICENSE.TXT

"""
The Polyglot corpus and module downloader.  This module defines several
interfaces which can be used to download corpora, models, and other
data packages that can be used with polyglot.

Downloading Packages
====================
If called with no arguments, ``download()`` will display an interactive
interface which can be used to download and install new packages.
If Tkinter is available, then a graphical interface will be shown,
otherwise a simple text interface will be provided.

Individual packages can be downloaded by calling the ``download()``
function with a single argument, giving the package identifier for the
package that should be downloaded:

  >>> download('treebank') # doctest: +SKIP
  [polyglot_data] Downloading package 'treebank'...
  [polyglot_data]   Unzipping corpora/treebank.zip.

Polyglot also provides a number of \"package collections\", consisting of
a group of related packages.  To download all packages in a
colleciton, simply call ``download()`` with the collection's
identifier:

  >>> download('all-corpora') # doctest: +SKIP
  [polyglot_data] Downloading package 'abc'...
  [polyglot_data]   Unzipping corpora/abc.zip.
  [polyglot_data] Downloading package 'alpino'...
  [polyglot_data]   Unzipping corpora/alpino.zip.
    ...
  [polyglot_data] Downloading package 'words'...
  [polyglot_data]   Unzipping corpora/words.zip.

Download Directory
==================
By default, packages are installed in either a system-wide directory
(if Python has sufficient access to write to it); or in the current
user's home directory.  However, the ``download_dir`` argument may be
used to specify a different installation target, if desired.

See ``Downloader.default_download_dir()`` for more a detailed
description of how the default download directory is chosen.

Polyglot Download Server
====================
Before downloading any packages, the corpus and module downloader
contacts the Polyglot download server, to retrieve an index file
describing the available packages.  By default, this index file is
loaded from ``http://nltk.googlecode.com/svn/trunk/polyglot_data/index.xml``.
If necessary, it is possible to create a new ``Downloader`` object,
specifying a different URL for the package index file.

Usage::

  python polyglot/downloader.py [-d DATADIR] [-q] [-f] [-k] PACKAGE_IDS

or::

  python -m polyglot.downloader [-d DATADIR] [-q] [-f] [-k] PACKAGE_IDS
"""
#----------------------------------------------------------------------
from __future__ import print_function, division, unicode_literals

import time
import os
import zipfile
import sys
import textwrap
import threading
import itertools
from hashlib import md5
from io import open
from collections import defaultdict
import logging
from os import path
from json import loads


from polyglot import data_path
from polyglot.detect.langids import isoLangs
from polyglot.utils import pretty_list
from icu import Locale

import stat
import six
from six import text_type as unicode
from six import string_types
from six.moves import input
from six.moves.urllib.request import urlopen
from six.moves.urllib.error import HTTPError, URLError
from six.moves.http_client import HTTPSConnection


logger = logging.getLogger(__name__)

######################################################################
# Exceptions
######################################################################

class ExceptionBase(Exception):
  """General base exception for the downloader module."""

class LanguageNotSupported(ExceptionBase):
  """Raised if the language is not covered by polyglot."""

class TaskNotSupported(ExceptionBase):
  """Raised if the task is not covered by polyglot."""

######################################################################
# Directory entry objects (from the data server's index file)
######################################################################

def is_writable(path):
  # Ensure that it exists.
  if not os.path.exists(path):
    return False

  # If we're on a posix system, check its permissions.
  if hasattr(os, 'getuid'):
    statdata = os.stat(path)
    perm = stat.S_IMODE(statdata.st_mode)
    # is it world-writable?
    if (perm & 0o002):
      return True
    # do we own it?
    elif statdata.st_uid == os.getuid() and (perm & 0o200):
      return True
    # are we in a group that can write to it?
    elif (statdata.st_gid in [os.getgid()] + os.getgroups()) and (perm & 0o020):
      return True
    # otherwise, we can't write to it.
    else:
      return False

  # Otherwise, we'll assume it's writable.
  # [xx] should we do other checks on other platforms?
  return True


def _path_from(parent, child):
  if os.path.split(parent)[1] == '':
      parent = os.path.split(parent)[0]
  path = []
  while parent != child:
    child, dirname = os.path.split(child)
    path.insert(0, dirname)
    assert os.path.split(child)[0] != child
  return path


class Package(object):
  """
  A directory entry for a downloadable package.  These entries are
  extracted from the XML index file that is downloaded by
  ``Downloader``.  Each package consists of a single file; but if
  that file is a zip file, then it can be automatically decompressed
  when the package is installed.
  """
  def __init__(self, id, url, name=None, subdir='',
               size=None, filename='', task='', language='',
               attrs=None, **kw):
    self.id = id
    """A unique identifier for this package."""

    self.name = name or id
    """A string name for this package."""

    self.subdir = subdir
    """The subdirectory where this package should be installed.
       E.g., ``'corpora'`` or ``'taggers'``."""

    self.url = url
    """A URL that can be used to download this package's file."""

    self.size = int(size)
    """The filesize (in bytes) of the package file."""

    self.filename = filename
    """The filename that should be used for this package's file."""

    self.task = task
    """The task this package is serving."""

    self.language = language
    """The langauge code this package belongs to."""

    self.attrs = attrs
    """Extra attributes generated by Google Cloud Storage."""

    # Include any other attributes provided by the XML file.
    self.__dict__.update(kw)

  @staticmethod
  def fromcsobj(csobj):
    attrs = csobj
    id_ = attrs["id"]
    id_ = id_.split(path.sep)
    id = ".".join(id_[1:3])
    name = attrs["name"].replace(path.sep, '.')
    subdir = path.dirname(attrs["name"])
    url = attrs["mediaLink"]
    size = attrs["size"]
    filename = attrs["name"]
    task = subdir.split(path.sep)[0]
    language = subdir.split(path.sep)[1]
    attrs = attrs
    return Package(**locals())

  def __lt__(self, other):
    return self.id < other.id

  def __repr__(self):
    return '<Package %s>' % self.id

class Collection(object):
  """
  A directory entry for a collection of downloadable packages.
  These entries are extracted from the XML index file that is
  downloaded by ``Downloader``.
  """
  def __init__(self, id, children, name=None, **kw):
    self.id = id
    """A unique identifier for this collection."""

    self.name = name or id
    """A string name for this collection."""

    self.children = children
    """A list of the ``Collections`` or ``Packages`` directly
       contained by this collection."""

    self.packages = None
    """A list of ``Packages`` contained by this collection or any
       collections it recursively contains."""

    # Include any other attributes provided by the XML file.
    self.__dict__.update(kw)

  def __lt__(self, other):
    return self.id < other.id

  def __repr__(self):
    return '<Collection %s>' % self.id

######################################################################
# Message Passing Objects
######################################################################

class DownloaderMessage(object):
  """A status message object, used by ``incr_download`` to
     communicate its progress."""


class StartCollectionMessage(DownloaderMessage):
  """Data server has started working on a collection of packages."""
  def __init__(self, collection): self.collection = collection


class FinishCollectionMessage(DownloaderMessage):
  """Data server has finished working on a collection of packages."""
  def __init__(self, collection): self.collection = collection

class StartPackageMessage(DownloaderMessage):
  """Data server has started working on a package."""
  def __init__(self, package): self.package = package


class FinishPackageMessage(DownloaderMessage):
  """Data server has finished working on a package."""
  def __init__(self, package): self.package = package


class StartDownloadMessage(DownloaderMessage):
  """Data server has started downloading a package."""
  def __init__(self, package): self.package = package


class FinishDownloadMessage(DownloaderMessage):
  """Data server has finished downloading a package."""
  def __init__(self, package): self.package = package


class StartUnzipMessage(DownloaderMessage):
  """Data server has started unzipping a package."""
  def __init__(self, package): self.package = package


class FinishUnzipMessage(DownloaderMessage):
  """Data server has finished unzipping a package."""
  def __init__(self, package): self.package = package


class UpToDateMessage(DownloaderMessage):
  """The package download file is already up-to-date"""
  def __init__(self, package): self.package = package


class StaleMessage(DownloaderMessage):
  """The package download file is out-of-date or corrupt"""
  def __init__(self, package): self.package = package


class ErrorMessage(DownloaderMessage):
  """Data server encountered an error"""
  def __init__(self, package, message):
    self.package = package
    if isinstance(message, Exception):
      self.message = str(message)
    else:
      self.message = message


class ProgressMessage(DownloaderMessage):
  """Indicates how much progress the data server has made"""
  def __init__(self, progress): self.progress = progress
class SelectDownloadDirMessage(DownloaderMessage):
  """Indicates what download directory the data server is using"""
  def __init__(self, download_dir): self.download_dir = download_dir

######################################################################
# Polyglot Data Server
######################################################################

class Downloader(object):
  """
  A class used to access the Polyglot data server, which can be used to
  download corpora and other data packages.
  """

  #/////////////////////////////////////////////////////////////////
  # Configuration
  #/////////////////////////////////////////////////////////////////

  INDEX_TIMEOUT = 60*60 # 1 hour
  """The amount of time after which the cached copy of the data
     server index will be considered 'stale,' and will be
     re-downloaded."""

  DEFAULT_SOURCE = 'mirror'
  """The source for index and other data files.
     Two values are supported: 'mirror' or 'google'.

     For 'mirror', the DEFAULT_URL should be set as a prefix of
     mirrored directory, like 'http://address.of.mirror/dir/',
     and the downloader expects a file named 'index.json' as index file.

     For 'google', the DEFAULT_URL should be the bucket of google cloud,
     and the downloader expects index from google api.

     So set the following DEFAULT_URL properly.
  """

  DEFAULT_URL = 'http://whoisbigger.com/polyglot/'
  """The default URL for the Polyglot data server's index.  An
     alternative URL can be specified when creating a new
     ``Downloader`` object.

     For 'google' as DEFAULT_SOURCE, 'polyglot-models' is the default place.
     For 'mirror' as DEFAULT_SOURCE, use an proper mirror.
     """

  #/////////////////////////////////////////////////////////////////
  # Status Constants
  #/////////////////////////////////////////////////////////////////

  INSTALLED = 'installed'
  """A status string indicating that a package or collection is
     installed and up-to-date."""
  NOT_INSTALLED = 'not installed'
  """A status string indicating that a package or collection is
     not installed."""
  STALE = 'out of date'
  """A status string indicating that a package or collection is
     corrupt or out-of-date."""
  PARTIAL = 'partial'
  """A status string indicating that a collection is partially
     installed (i.e., only some of its packages are installed.)"""

  LANG_PREFIX = "LANG:"
  """Collection ID prefix for collections that gathers models of a specific
     task."""

  TASK_PREFIX = "TASK:"
  """Collection ID prefix for collections that gathers models of a specific
     task."""

  #/////////////////////////////////////////////////////////////////
  # Cosntructor
  #/////////////////////////////////////////////////////////////////

  def __init__(self, server_index_url=None, source=None, download_dir=None):
    self._url = server_index_url or self.DEFAULT_URL
    """The URL for the data server's index file."""

    self._source = source or self.DEFAULT_SOURCE
    """The (type of) source of the index file."""

    self._collections = {}
    """Dictionary from collection identifier to ``Collection``"""

    self._packages = {}
    """Dictionary from package identifier to ``Package``"""

    self._download_dir = download_dir
    """The default directory to which packages will be downloaded."""

    self._index = None
    """The XML index file downloaded from the data server"""

    self._index_timestamp = None
    """Time at which ``self._index`` was downloaded.  If it is more
       than ``INDEX_TIMEOUT`` seconds old, it will be re-downloaded."""

    self._status_cache = {}
    """Dictionary from package/collection identifier to status
       string (``INSTALLED``, ``NOT_INSTALLED``, ``STALE``, or
       ``PARTIAL``).  Cache is used for packages only, not
       collections."""

    self._errors = None
    """Flag for telling if all packages got successfully downloaded or not."""

    # decide where we're going to save things to.
    if self._download_dir is None:
      self._download_dir = self.default_download_dir()

  #/////////////////////////////////////////////////////////////////
  # Information
  #/////////////////////////////////////////////////////////////////

  def list(self, download_dir=None, show_packages=False,
       show_collections=True, header=True, more_prompt=False,
       skip_installed=False):
    lines = 0 # for more_prompt
    if download_dir is None:
      download_dir = self._download_dir
      print('Using default data directory (%s)' % download_dir)
    if header:
      print('='*(26+len(self._url)))
      print(' Data server index for <%s>' % self._url)
      print('='*(26+len(self._url)))
      lines += 3 # for more_prompt
    stale = partial = False

    categories = []
    if show_packages: categories.append('packages')
    if show_collections: categories.append('collections')
    for category in categories:
      print('%s:' % category.capitalize())
      lines += 1 # for more_prompt
      for info in sorted(getattr(self, category)(), key=str):
        status = self.status(info, download_dir)
        if status == self.INSTALLED and skip_installed: continue
        if status == self.STALE: stale = True
        if status == self.PARTIAL: partial = True
        prefix = {self.INSTALLED:'*', self.STALE:'-',
              self.PARTIAL:'P', self.NOT_INSTALLED: ' '}[status]
        name = textwrap.fill('-'*27 + (info.name or info.id),
                   75, subsequent_indent=27*' ')[27:]
        print('  [%s] %s %s' % (prefix, info.id.ljust(20, '.'), name))
        lines += len(name.split('\n')) # for more_prompt
        if more_prompt and lines > 20:
          user_input = unicode(input("Hit Enter to continue: "))
          if (user_input.lower() in ('x', 'q')): return
          lines = 0
      print()
    msg = '([*] marks installed packages'
    if stale: msg += '; [-] marks out-of-date or corrupt packages'
    if partial: msg += '; [P] marks partially installed collections'
    print(textwrap.fill(msg+')', subsequent_indent=' ', width=76))

  def packages(self):
    self._update_index()
    return self._packages.values()

  def corpora(self):
    self._update_index()
    return [pkg for (id,pkg) in self._packages.items()
        if pkg.subdir == 'corpora']

  def models(self):
    self._update_index()
    return [pkg for (id,pkg) in self._packages.items()
        if pkg.subdir != 'corpora']

  def collections(self):
    self._update_index()
    return self._collections.values()

  #/////////////////////////////////////////////////////////////////
  # Downloading
  #/////////////////////////////////////////////////////////////////

  def _info_or_id(self, info_or_id):
    if isinstance(info_or_id, unicode):
      return self.info(info_or_id)
    else:
      return info_or_id

  # [xx] When during downloading is it 'safe' to abort?  Only unsafe
  # time is *during* an unzip -- we don't want to leave a
  # partially-unzipped corpus in place because we wouldn't notice
  # it.  But if we had the exact total size of the unzipped corpus,
  # then that would be fine.  Then we could abort anytime we want!
  # So this is really what we should do.  That way the threaded
  # downloader in the gui can just kill the download thread anytime
  # it wants.

  def incr_download(self, info_or_id, download_dir=None, force=False):
    # If they didn't specify a download_dir, then use the default one.
    if download_dir is None:
      download_dir = self._download_dir
      yield SelectDownloadDirMessage(download_dir)

    # If they gave us a list of ids, then download each one.
    if isinstance(info_or_id, (list,tuple)):
      for msg in self._download_list(info_or_id, download_dir, force):
        yield msg
      return

    # Look up the requested collection or package.
    try: info = self._info_or_id(info_or_id)
    except (IOError, ValueError) as e:
      yield ErrorMessage(None, 'Error loading %s: %s' %
                 (info_or_id, e))
      return

    # Handle collections.
    if isinstance(info, Collection):
      yield StartCollectionMessage(info)
      for msg in self.incr_download(info.children, download_dir, force):
        yield msg
      yield FinishCollectionMessage(info)

    # Handle Packages (delegate to a helper function).
    else:
      for msg in self._download_package(info, download_dir, force):
        yield msg

  def _num_packages(self, item):
    if isinstance(item, Package): return 1
    else: return len(item.packages)

  def _download_list(self, items, download_dir, force):
    # Look up the requested items.
    for i in range(len(items)):
      try: items[i] = self._info_or_id(items[i])
      except (IOError, ValueError) as e:
        yield ErrorMessage(items[i], e)
        return

    # Download each item, re-scaling their progress.
    num_packages = sum(self._num_packages(item) for item in items)
    progress = 0
    for i, item in enumerate(items):
      if isinstance(item, Package):
        delta = 1./num_packages
      else:
        delta = float(len(item.packages))/num_packages
      for msg in self.incr_download(item, download_dir, force):
        if isinstance(msg, ProgressMessage):
          yield ProgressMessage(progress + msg.progress*delta)
        else:
          yield msg

      progress += 100*delta

  def _download_package(self, info, download_dir, force):
    yield StartPackageMessage(info)
    yield ProgressMessage(0)

    # Do we already have the current version?
    status = self.status(info, download_dir)
    if not force and status == self.INSTALLED:
      yield UpToDateMessage(info)
      yield ProgressMessage(100)
      yield FinishPackageMessage(info)
      return

    # Remove the package from our status cache
    self._status_cache.pop(info.id, None)

    # Check for (and remove) any old/stale version.
    filepath = os.path.join(download_dir, info.filename)
    if os.path.exists(filepath):
      if status == self.STALE:
        yield StaleMessage(info)
      os.remove(filepath)

    # Ensure the download_dir exists
    if not path.exists(path.join(download_dir, info.subdir)):
      os.makedirs(path.join(download_dir, info.subdir))

    # Download the file.  This will raise an IOError if the url
    # is not found.
    yield StartDownloadMessage(info)
    yield ProgressMessage(5)
    try:
      infile = urlopen(info.url)
      with open(filepath, 'wb') as outfile:
        #print info.size
        num_blocks = max(1, float(info.size)/(1024*16))
        for block in itertools.count():
          s = infile.read(1024*16) # 16k blocks.
          outfile.write(s)
          if not s: break
          if block % 2 == 0: # how often?
            yield ProgressMessage(min(80, 5+75*(block/num_blocks)))
      infile.close()
    except IOError as e:
      yield ErrorMessage(info, 'Error downloading %r from <%s>:'
                 '\n  %s' % (info.id, info.url, e))
      return
    yield FinishDownloadMessage(info)
    yield ProgressMessage(80)

    # If it's a zipfile, uncompress it.
    if info.filename.endswith('.zip'):
      zipdir = os.path.join(download_dir, info.subdir)
      # Unzip if we're unzipping by default; *or* if it's already
      # been unzipped (presumably a previous version).
      if info.unzip or os.path.exists(os.path.join(zipdir, info.id)):
        yield StartUnzipMessage(info)
        for msg in _unzip_iter(filepath, zipdir, verbose=False):
          # Somewhat of a hack, but we need a proper package reference
          msg.package = info
          yield msg
        yield FinishUnzipMessage(info)

    yield FinishPackageMessage(info)

  def download(self, info_or_id=None, download_dir=None, quiet=False,
         force=False, prefix='[polyglot_data] ', halt_on_error=True,
         raise_on_error=False):
    # If no info or id is given, then use the interactive shell.
    if info_or_id is None:
      # [xx] hmm -- changing self._download_dir here seems like
      # the wrong thing to do.  Maybe the _interactive_download
      # function should make a new copy of self to use?
      if download_dir is not None: self._download_dir = download_dir
      self._interactive_download()
      return True

    else:
      if isinstance(info_or_id, string_types):
        info_or_id = unicode(info_or_id)
      # Define a helper function for displaying output:
      def show(s, prefix2=''):
        print(textwrap.fill(s, initial_indent=prefix+prefix2,
                  subsequent_indent=prefix+prefix2+' '*4))

      for msg in self.incr_download(info_or_id, download_dir, force):
        # Error messages
        if isinstance(msg, ErrorMessage):
          show(msg.message)
          if raise_on_error:
            raise ValueError(msg.message)
          if halt_on_error:
            return False
          self._errors = True
          if not quiet:
            print("Error installing package. Retry? [n/y/e]")
            choice = unicode(input().strip())
            if choice in ['y', 'Y']:
              if not self.download(msg.package.id, download_dir,
                         quiet, force, prefix,
                         halt_on_error, raise_on_error):
                return False
            elif choice in ['e', 'E']:
              return False

        # All other messages
        if not quiet:
          # Collection downloading messages:
          if isinstance(msg, StartCollectionMessage):
            show('Downloading collection %r' % msg.collection.id)
            prefix += '   | '
            print(prefix)
          elif isinstance(msg, FinishCollectionMessage):
            print(prefix)
            prefix = prefix[:-4]
            if self._errors:
              show('Downloaded collection %r with errors' %
                 msg.collection.id)
            else:
              show('Done downloading collection %s' %
                 msg.collection.id)

          # Package downloading messages:
          elif isinstance(msg, StartPackageMessage):
            show('Downloading package %s to %s...' %
               (msg.package.id, download_dir))
          elif isinstance(msg, UpToDateMessage):
            show('Package %s is already up-to-date!' %
               msg.package.id, '  ')
          #elif isinstance(msg, StaleMessage):
          #  show('Package %s is out-of-date or corrupt' %
          #     msg.package.id, '  ')
          elif isinstance(msg, StartUnzipMessage):
            show('Unzipping %s.' % msg.package.filename, '  ')

          # Data directory message:
          elif isinstance(msg, SelectDownloadDirMessage):
            download_dir = msg.download_dir
    return True

  def is_stale(self, info_or_id, download_dir=None):
    return self.status(info_or_id, download_dir) == self.STALE

  def is_installed(self, info_or_id, download_dir=None):
    return self.status(info_or_id, download_dir) == self.INSTALLED

  def clear_status_cache(self, id=None):
    if id is None:
      self._status_cache.clear()
    else:
      self._status_cache.pop(id, None)

  def status(self, info_or_id, download_dir=None):
    """
    Return a constant describing the status of the given package
    or collection.  Status can be one of ``INSTALLED``,
    ``NOT_INSTALLED``, ``STALE``, or ``PARTIAL``.
    """
    if download_dir is None: download_dir = self._download_dir
    info = self._info_or_id(info_or_id)

    # Handle collections:
    if isinstance(info, Collection):
      pkg_status = [self.status(pkg.id) for pkg in info.packages]
      if self.STALE in pkg_status:
        return self.STALE
      elif self.PARTIAL in pkg_status:
        return self.PARTIAL
      elif (self.INSTALLED in pkg_status and
          self.NOT_INSTALLED in pkg_status):
        return self.PARTIAL
      elif self.NOT_INSTALLED in pkg_status:
        return self.NOT_INSTALLED
      else:
        return self.INSTALLED

    # Handle packages:
    else:
      filepath = os.path.join(download_dir, info.filename)
      if download_dir != self._download_dir:
        status = self._pkg_status(info, filepath)
      else:
        if info.id not in self._status_cache:
          self._status_cache[info.id] = self._pkg_status(info,
                                   filepath)
        return self._status_cache[info.id]

  def _pkg_status(self, info, filepath):
    if not os.path.exists(filepath):
      return self.NOT_INSTALLED

    # Check if the file has the correct size.
    try: filestat = os.stat(filepath)
    except OSError: return self.NOT_INSTALLED
    if filestat.st_size != int(info.size):
      return self.STALE


    # If it's a zipfile, and it's been at least partially
    # unzipped, then check if it's been fully unzipped.
    if filepath.endswith('.zip'):
      unzipdir = filepath[:-4]
      if not os.path.exists(unzipdir):
        return self.INSTALLED # but not unzipped -- ok!
      if not os.path.isdir(unzipdir):
        return self.STALE

      unzipped_size = sum(os.stat(os.path.join(d, f)).st_size
                for d, _, files in os.walk(unzipdir)
                for f in files)
      if unzipped_size != info.unzipped_size:
        return self.STALE

    # Otherwise, everything looks good.
    return self.INSTALLED

  def update(self, quiet=False, prefix='[polyglot_data] '):
    """
    Re-download any packages whose status is STALE.
    """
    self.clear_status_cache()
    for pkg in self.packages():
      if self.status(pkg) == self.STALE:
        self.download(pkg, quiet=quiet, prefix=prefix)

  #/////////////////////////////////////////////////////////////////
  # Index
  #/////////////////////////////////////////////////////////////////

  def _update_index(self, url=None):
    """A helper function that ensures that self._index is
    up-to-date.  If the index is older than self.INDEX_TIMEOUT,
    then download it again."""
    # Check if the index is aleady up-to-date.  If so, do nothing.
    if not (self._index is None or url is not None or
        time.time()-self._index_timestamp > self.INDEX_TIMEOUT):
      return

    # If a URL was specified, then update our URL.
    self._url = url or self._url

    source = self._source
    assert source == 'google' or source == 'mirror'

    # Download the index file.
    if source == 'google':
        host = "www.googleapis.com"
        conn = HTTPSConnection(host)
        conn.request("GET", "/storage/v1/b/{}/o".format(self._url))
        r1 = conn.getresponse()
        data = r1.read()
    elif source == 'mirror':
        index_url = path.join(self._url, 'index.json')
        data = urlopen(index_url).read()

    if six.PY3:
      data = data.decode('utf-8')
    data = loads(data)
    objs = data["items"]

    self._index_timestamp = time.time()

    # Build a dictionary of packages.
    packages = []
    for p in objs:
      P = Package.fromcsobj(p)
      packages.append(P)
    self._packages = dict((p.id, p) for p in packages)

    # Build language collections.
    langs = defaultdict(lambda: [])
    for k in self._packages:
      package = self._packages[k]
      langs[package.language].append(package)

    tasks = defaultdict(lambda: [])
    for k in self._packages:
      package = self._packages[k]
      tasks[package.task].append(package)

    collections = []

    for lang in langs:
      children = langs[lang]

      name1 = Locale(lang).getDisplayLanguage()

      try:
        name2 = isoLangs[lang]['name']
      except:
        name2 = None

      if name1 and name1 != lang:
        name = name1
      elif name2:
        name = name2
      else:
        name = lang

      id = "{}{}".format(Downloader.LANG_PREFIX, lang)
      name = "{:<20} packages and models".format(name)
      c = Collection(id=id, name=name, children=children)
      collections.append(c)

    for task in tasks:
      children = tasks[task]
      id = "{}{}".format(Downloader.TASK_PREFIX, task)
      c = Collection(id=id, name=task, children=children)
      collections.append(c)


    self._collections = dict((c.id, c) for c in collections)

    # Replace identifiers with actual children in collection.children.
    for collection in self._collections.values():
      for i, child_id in enumerate(collection.children):
        if child_id in self._packages:
          collection.children[i] = self._packages[child_id]
        if child_id in self._collections:
          collection.children[i] = self._collections[child_id]

    # Fill in collection.packages for each collection.
    for collection in self._collections.values():
      packages = {}
      queue = [collection]
      for child in queue:
        if isinstance(child, Collection):
          queue.extend(child.children)
        else:
          packages[child.id] = child
      collection.packages = packages.values()

    # Flush the status cache
    self._status_cache.clear()

  def index(self):
    """
    Return the XML index describing the packages available from
    the data server.  If necessary, this index will be downloaded
    from the data server.
    """
    self._update_index()
    return self._index

  def info(self, id):
    """Return the ``Package`` or ``Collection`` record for the
       given item."""
    #self._update_index() # This is commented because it leads to
                          # excessive network load
    if id in self._packages: return self._packages[id]
    if id in self._collections: return self._collections[id]
    self._update_index() # If package is not found, most probably we did not
                         # warm up the cache
    if id in self._packages: return self._packages[id]
    if id in self._collections: return self._collections[id]
    raise ValueError('Package %r not found in index' % id)

  def get_collection(self, lang=None, task=None):
    """ Return the collection that represents a specific language or task.

    Args:
      lang (string): Language code.
      task (string): Task name.
    """
    if lang: id = "{}{}".format(Downloader.LANG_PREFIX, lang)
    elif task: id = "{}{}".format(Downloader.TASK_PREFIX, task)
    else: raise ValueError("You should pass either the task or the lang")
    try:
      return self.info(id)
    except ValueError as e:
      if lang: raise LanguageNotSupported("Language {} is not supported".format(id))
      if task: raise TaskNotSupported("Task {} is not supported".format(id))

  def supported_language(lang):
    """Return True if polyglot supports the language.

    Args:
      lang (string): Language code.
    """
    try:
      self.get_collection(lang=lang)
      return True
    except LanguageNotSupported as e:
      return False

  def supported_languages(self, task=None):
    """Languages that are covered by a specific task.

    Args:
      task (string): Task name.
    """
    if task:
      collection = self.get_collection(task=task)
      return [isoLangs[x.id.split('.')[1]]["name"]
                                         for x in collection.packages]
    else:
      return [x.name.split()[0] for x in self.collections()
                                         if Downloader.LANG_PREFIX in x.id]

  def supported_languages_table(self, task, cols=3):
    languages = self.supported_languages(task)
    return pretty_list(languages)


  def supported_tasks(self, lang=None):
    """Languages that are covered by a specific task.

    Args:
      lang (string): Language code name.
    """
    if lang:
      collection = self.get_collection(lang=lang)
      return [x.id.split('.')[0] for x in collection.packages]
    else:
      return [x.name.split()[0] for x in self.collections() if Downloader.TASK_PREFIX in x.id]

  def xmlinfo(self, id):
    """Return the XML info record for the given item"""
    self._update_index()
    for package in self._index.findall('packages/package'):
      if package.get('id') == id:
        return package
    for collection in self._index.findall('collections/collection'):
      if collection.get('id') == id:
        return collection
    raise ValueError('Package %r not found in index' % id)

  #/////////////////////////////////////////////////////////////////
  # URL & Data Directory
  #/////////////////////////////////////////////////////////////////

  def _get_url(self):
    """The URL for the data server's index file."""
    return self._url

  def _set_url(self, url):
    """
    Set a new URL for the data server. If we're unable to contact
    the given url, then the original url is kept.
    """
    original_url = self._url
    try:
      self._update_index(url)
    except:
      self._url = original_url
      raise
  url = property(_get_url, _set_url)

  def default_download_dir(self):
    """
    Return the directory to which packages will be downloaded by
    default.  This value can be overridden using the constructor,
    or on a case-by-case basis using the ``download_dir`` argument when
    calling ``download()``.

    On Windows, the default download directory is
    ``PYTHONHOME/lib/nltk``, where *PYTHONHOME* is the
    directory containing Python, e.g. ``C:\\Python25``.

    On all other platforms, the default directory is the first of
    the following which exists or which can be created with write
    permission: ``/usr/share/polyglot_data``, ``/usr/local/share/polyglot_data``,
    ``/usr/lib/polyglot_data``, ``/usr/local/lib/polyglot_data``, ``~/polyglot_data``.
    """
    # Check if we have sufficient permissions to install in a
    # variety of system-wide locations.
    for dir_ in data_path:
      if (os.path.exists(dir_) and is_writable(dir_)):
        return dir_

    # On Windows, use %APPDATA%
    if sys.platform == 'win32' and 'APPDATA' in os.environ:
      homedir = os.environ['APPDATA']

    # Otherwise, install in the user's home directory.
    else:
      homedir = os.path.expanduser('~/')
      if homedir == '~/':
        raise ValueError("Could not find a default download directory")

    # append "polyglot_data" to the home directory
    return os.path.join(homedir, 'polyglot_data')

  def _get_download_dir(self):
    """
    The default directory to which packages will be downloaded.
    This defaults to the value returned by ``default_download_dir()``.
    To override this default on a case-by-case basis, use the
    ``download_dir`` argument when calling ``download()``.
    """
    return self._download_dir
  def _set_download_dir(self, download_dir):
    self._download_dir = download_dir
    # Clear the status cache.
    self._status_cache.clear()
  download_dir = property(_get_download_dir, _set_download_dir)

  #/////////////////////////////////////////////////////////////////
  # Interactive Shell
  #/////////////////////////////////////////////////////////////////

  def _interactive_download(self):
    DownloaderShell(self).run()

class DownloaderShell(object):
  def __init__(self, dataserver):
    self._ds = dataserver

  def _simple_interactive_menu(self, *options):
    print('-'*75)
    spc = (68 - sum(len(o) for o in options))//(len(options)-1)*' '
    print('  ' + spc.join(options))
    print('-'*75)

  def run(self):
    print('Polyglot Downloader')
    while True:
      self._simple_interactive_menu(
        'd) Download', 'l) List', ' u) Update', 'c) Config', 'h) Help', 'q) Quit')
      user_input = unicode(input('Downloader> ').strip())
      if not user_input: print(); continue
      command = user_input.lower().split()[0]
      args = user_input.split()[1:]
      try:
        if command == 'l':
          print()
          self._ds.list(self._ds.download_dir, header=False,
                  more_prompt=True)
        elif command == 'h':
          self._simple_interactive_help()
        elif command == 'c':
          self._simple_interactive_config()
        elif command in ('q', 'x'):
          return
        elif command == 'd':
          self._simple_interactive_download(args)
        elif command == 'u':
          self._simple_interactive_update()
        else:
          print('Command %r unrecognized' % user_input)
      except HTTPError as e:
        print('Error reading from server: %s'%e)
      except URLError as e:
        print('Error connecting to server: %s'%e.reason)
      # try checking if user_input is a package name, &
      # downloading it?
      print()

  def _simple_interactive_download(self, args):
    if args:
      for arg in args:
        try: self._ds.download(arg, prefix='  ')
        except (IOError, ValueError) as e: print(e)
    else:
      while True:
        print()
        print('Download which package (l=list; x=cancel)?')
        user_input = unicode(input('  Identifier> '))
        if user_input.lower()=='l':
          self._ds.list(self._ds.download_dir, header=False,
                  more_prompt=True, skip_installed=True)
          continue
        elif user_input.lower() in ('x', 'q', ''):
          return
        elif user_input:
          for id in user_input.split():
            try: self._ds.download(id, prefix='  ')
            except (IOError, ValueError) as e: print(e)
          break

  def _simple_interactive_update(self):
    while True:
      stale_packages = []
      stale = partial = False
      for info in sorted(getattr(self._ds, 'packages')(), key=str):
        if self._ds.status(info) == self._ds.STALE:
          stale_packages.append((info.id, info.name))

      print()
      if stale_packages:
        print('Will update following packages (o=ok; x=cancel)')
        for pid, pname in stale_packages:
          name = textwrap.fill('-'*27 + (pname),
                   75, subsequent_indent=27*' ')[27:]
          print('  [ ] %s %s' % (pid.ljust(20, '.'), name))
        print()

        user_input = unicode(input('  Identifier> '))
        if user_input.lower()=='o':
          for pid, pname in stale_packages:
            try: self._ds.download(pid, prefix='  ')
            except (IOError, ValueError) as e: print(e)
          break
        elif user_input.lower() in ('x', 'q', ''):
          return
      else:
        print('Nothing to update.')
        return

  def _simple_interactive_help(self):
    print()
    print('Commands:')
    print('  d) Download a package or collection   u) Update out of date packages')
    print('  l) List packages & collections      h) Help')
    print('  c) View & Modify Configuration      q) Quit')

  def _show_config(self):
    print()
    print('Data Server:')
    print('  - URL: <%s>' % self._ds.url)
    print(('  - %d Package Collections Available' %
         len(self._ds.collections())))
    print(('  - %d Individual Packages Available' %
         len(self._ds.packages())))
    print()
    print('Local Machine:')
    print('  - Data directory: %s' % self._ds.download_dir)

  def _simple_interactive_config(self):
    self._show_config()
    while True:
      print()
      self._simple_interactive_menu(
        's) Show Config', 'u) Set Server URL',
        'd) Set Data Dir', 'm) Main Menu')
      user_input = input('Config> ').strip().lower()
      if user_input == 's':
        self._show_config()
      elif user_input == 'd':
        new_dl_dir = input('  New Directory> ').strip().lower()
        if new_dl_dir in ('', 'x', 'q'):
          print('  Cancelled!')
        elif os.path.isdir(new_dl_dir):
          self._ds.download_dir = new_dl_dir
        else:
          print(('Directory %r not found!  Create it first.' %
               new_dl_dir))
      elif user_input == 'u':
        new_url = input('  New URL> ').strip().lower()
        if new_url in ('', 'x', 'q'):
          print('  Cancelled!')
        else:
          if not new_url.startswith('http://'):
            new_url = 'http://'+new_url
          try: self._ds.url = new_url
          except Exception as e:
            print('Error reading <%r>:\n  %s' % (new_url, e))
      elif user_input == 'm':
        break


######################################################################
# Helper Functions
######################################################################

# change this to periodically yield progress messages?
# [xx] get rid of topdir parameter -- we should be checking
# this when we build the index, anyway.
def unzip(filename, root, verbose=True):
  """
  Extract the contents of the zip file ``filename`` into the
  directory ``root``.
  """
  for message in _unzip_iter(filename, root, verbose):
    if isinstance(message, ErrorMessage):
      raise Exception(message)

def _unzip_iter(filename, root, verbose=True):
  if verbose:
    sys.stdout.write('Unzipping %s' % os.path.split(filename)[1])
    sys.stdout.flush()

  try: zf = zipfile.ZipFile(filename)
  except zipfile.error as e:
    yield ErrorMessage(filename, 'Error with downloaded zip file')
    return
  except Exception as e:
    yield ErrorMessage(filename, e)
    return

  # Get lists of directories & files
  namelist = zf.namelist()
  dirlist = set()
  for x in namelist:
    if x.endswith('/'):
      dirlist.add(x)
    else:
      dirlist.add(x.rsplit('/',1)[0] + '/')
  filelist = [x for x in namelist if not x.endswith('/')]

  # Create the target directory if it doesn't exist
  if not os.path.exists(root):
    os.mkdir(root)

  # Create the directory structure
  for dirname in sorted(dirlist):
    pieces = dirname[:-1].split('/')
    for i in range(len(pieces)):
      dirpath = os.path.join(root, *pieces[:i+1])
      if not os.path.exists(dirpath):
        os.mkdir(dirpath)

  # Extract files.
  for i, filename in enumerate(filelist):
    filepath = os.path.join(root, *filename.split('/'))

    with open(filepath, 'wb') as outfile:
      try:
        contents = zf.read(filename)
      except Exception as e:
        yield ErrorMessage(filename, e)
        return
      outfile.write(contents)

    if verbose and (i*10/len(filelist) > (i-1)*10/len(filelist)):
      sys.stdout.write('.')
      sys.stdout.flush()
  if verbose:
    print()

######################################################################
# Index Builder
######################################################################
# This may move to a different file sometime.
import subprocess, zipfile

def build_index(root, base_url):
  """
  Create a new data.xml index file, by combining the xml description
  files for various packages and collections.  ``root`` should be the
  path to a directory containing the package xml and zip files; and
  the collection xml files.  The ``root`` directory is expected to
  have the following subdirectories::

    root/
    packages/ .................. subdirectory for packages
      corpora/ ................. zip & xml files for corpora
      grammars/ ................ zip & xml files for grammars
      taggers/ ................. zip & xml files for taggers
      tokenizers/ .............. zip & xml files for tokenizers
      etc.
    collections/ ............... xml files for collections

  For each package, there should be two files: ``package.zip``
  (where *package* is the package name)
  which contains the package itself as a compressed zip file; and
  ``package.xml``, which is an xml description of the package.  The
  zipfile ``package.zip`` should expand to a single subdirectory
  named ``package/``.  The base filename ``package`` must match
  the identifier given in the package's xml file.

  For each collection, there should be a single file ``collection.zip``
  describing the collection, where *collection* is the name of the collection.

  All identifiers (for both packages and collections) must be unique.
  """
  # Find all packages.
  packages = []
  for pkg_xml, zf, subdir in _find_packages(os.path.join(root, 'packages')):
    zipstat = os.stat(zf.filename)
    url = '%s/%s/%s' % (base_url, subdir, os.path.split(zf.filename)[1])
    unzipped_size = sum(zf_info.file_size for zf_info in zf.infolist())

    # Fill in several fields of the package xml with calculated values.
    pkg_xml.set('unzipped_size', '%s' % unzipped_size)
    pkg_xml.set('size', '%s' % zipstat.st_size)
    pkg_xml.set('subdir', subdir)
    pkg_xml.set('url', url)

    # Record the package.
    packages.append(pkg_xml)

  # Find all collections
  collections = list(_find_collections(os.path.join(root, 'collections')))

  # Check that all UIDs are unique
  uids = set()
  for item in packages+collections:
    if item.get('id') in uids:
      raise ValueError('Duplicate UID: %s' % item.get('id'))
    uids.add(item.get('id'))

  # Put it all together
  top_elt = ElementTree.Element('polyglot_data')
  top_elt.append(ElementTree.Element('packages'))
  for package in packages: top_elt[0].append(package)
  top_elt.append(ElementTree.Element('collections'))
  for collection in collections: top_elt[1].append(collection)

  _indent_xml(top_elt)
  return top_elt

def _indent_xml(xml, prefix=''):
  """
  Helper for ``build_index()``: Given an XML ``ElementTree``, modify it
  (and its descendents) ``text`` and ``tail`` attributes to generate
  an indented tree, where each nested element is indented by 2
  spaces with respect to its parent.
  """
  if len(xml) > 0:
    xml.text = (xml.text or '').strip() + '\n' + prefix + '  '
    for child in xml:
      _indent_xml(child, prefix+'  ')
    for child in xml[:-1]:
      child.tail = (child.tail or '').strip() + '\n' + prefix + '  '
    xml[-1].tail = (xml[-1].tail or '').strip() + '\n' + prefix

def _check_package(pkg_xml, zipfilename, zf):
  """
  Helper for ``build_index()``: Perform some checks to make sure that
  the given package is consistent.
  """
  # The filename must patch the id given in the XML file.
  uid = os.path.splitext(os.path.split(zipfilename)[1])[0]
  if pkg_xml.get('id') != uid:
    raise ValueError('package identifier mismatch (%s vs %s)' %
             (pkg_xml.get('id'), uid))

  # Zip file must expand to a subdir whose name matches uid.
  if sum( (name!=uid and not name.startswith(uid+'/'))
      for name in zf.namelist() ):
    raise ValueError('Zipfile %s.zip does not expand to a single '
             'subdirectory %s/' % (uid, uid))

# update for git?
def _svn_revision(filename):
  """
  Helper for ``build_index()``: Calculate the subversion revision
  number for a given file (by using ``subprocess`` to run ``svn``).
  """
  p = subprocess.Popen(['svn', 'status', '-v', filename],
             stdout=subprocess.PIPE,
             stderr=subprocess.PIPE)
  (stdout, stderr) = p.communicate()
  if p.returncode != 0 or stderr or not stdout:
    raise ValueError('Error determining svn_revision for %s: %s' %
             (os.path.split(filename)[1], textwrap.fill(stderr)))
  return stdout.split()[2]

def _find_collections(root):
  """
  Helper for ``build_index()``: Yield a list of ElementTree.Element
  objects, each holding the xml for a single package collection.
  """
  packages = []
  for dirname, subdirs, files in os.walk(root):
    for filename in files:
      if filename.endswith('.xml'):
        xmlfile = os.path.join(dirname, filename)
        yield ElementTree.parse(xmlfile).getroot()

def _find_packages(root):
  """
  Helper for ``build_index()``: Yield a list of tuples
  ``(pkg_xml, zf, subdir)``, where:
    - ``pkg_xml`` is an ``ElementTree.Element`` holding the xml for a
    package
    - ``zf`` is a ``zipfile.ZipFile`` for the package's contents.
    - ``subdir`` is the subdirectory (relative to ``root``) where
    the package was found (e.g. 'corpora' or 'grammars').
  """
  # Find all packages.
  packages = []
  for dirname, subdirs, files in os.walk(root):
    relpath = '/'.join(_path_from(root, dirname))
    for filename in files:
      if filename.endswith('.xml'):
        xmlfilename = os.path.join(dirname, filename)
        zipfilename = xmlfilename[:-4]+'.zip'
        try: zf = zipfile.ZipFile(zipfilename)
        except Exception as e:
          raise ValueError('Error reading file %r!\n%s' %
                   (zipfilename, e))
        try: pkg_xml = ElementTree.parse(xmlfilename).getroot()
        except Exception as e:
          raise ValueError('Error reading file %r!\n%s' %
                   (xmlfilename, e))

        # Check that the UID matches the filename
        uid = os.path.split(xmlfilename[:-4])[1]
        if pkg_xml.get('id') != uid:
          raise ValueError('package identifier mismatch (%s '
                   'vs %s)' % (pkg_xml.get('id'), uid))

        # Check that the zipfile expands to a subdir whose
        # name matches the uid.
        if sum( (name!=uid and not name.startswith(uid+'/'))
            for name in zf.namelist() ):
          raise ValueError('Zipfile %s.zip does not expand to a '
                   'single subdirectory %s/' % (uid, uid))

        yield pkg_xml, zf, relpath
    # Don't recurse into svn subdirectories:
    try: subdirs.remove('.svn')
    except ValueError: pass

######################################################################
# Main:
######################################################################

# There should be a command-line interface

# Aliases
downloader = Downloader()

def download_shell():
  DownloaderShell(_downloader).run()

def download_gui():
  DownloaderGUI(_downloader).mainloop()

def update():
  _downloader.update()

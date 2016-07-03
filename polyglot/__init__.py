# -*- coding: utf-8 -*-

__author__ = 'Rami Al-Rfou'
__email__ = 'rmyeid@gmail.com'
__version__ = '16.07.04'

import os
import sys
import types

from six.moves import copyreg
from .base import Sequence, TokenSequence
from .utils import _pickle_method, _unpickle_method

__all__ = ['Sequence', 'TokenSequence']

# On Windows, use %APPDATA%
if sys.platform == 'win32' and 'APPDATA' in os.environ:
  data_path = os.environ['APPDATA']
else:
  data_path = '~/'
data_path = os.environ.get('POLYGLOT_DATA_PATH', data_path)
data_path = os.path.abspath(os.path.expanduser(data_path))
polyglot_path = os.path.join(data_path, "polyglot_data")

copyreg.pickle(types.MethodType, _pickle_method, _unpickle_method)

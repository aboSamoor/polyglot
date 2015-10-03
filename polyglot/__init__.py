# -*- coding: utf-8 -*-

__author__ = 'Rami Al-Rfou'
__email__ = 'rmyeid@gmail.com'
__version__ = '15.10.03'

import types

from six.moves import copyreg
from .base import Sequence, TokenSequence
from .utils import _pickle_method, _unpickle_method

__all__ = ['Sequence', 'TokenSequence']

data_path = '~/'

copyreg.pickle(types.MethodType, _pickle_method, _unpickle_method)

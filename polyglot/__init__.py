# -*- coding: utf-8 -*-

__author__ = 'Rami Al-Rfou'
__email__ = 'rmyeid@gmail.com'
__version__ = '14.11'

import copy_reg
import types

from .base import Sequence, TokenSequence
from .utils import _pickle_method, _unpickle_method

__all__ = ['Sequence', 'TokenSequence']

data_path = '~/'

copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)

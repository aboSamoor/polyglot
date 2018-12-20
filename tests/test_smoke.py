#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_smoke
----------------------------------

smoke tests for `polyglot` module.
"""

import pytest


def test_for_fire():
    """Make sure nothing blows up while importing polyglot"""
    import polyglot


if __name__ == "__main__":
    pytest.main(["-v"])

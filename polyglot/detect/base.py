#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Detecting languages"""


import pycld2 as cld2

class Detector(object):
  def __init__(self):
    pass

  def detect(self, text):
    flag, index, top_3_choices = cld2.detect(text)
    top_choice, second_choice, third_choice = top_3_choices
    return top_choice[1:3]

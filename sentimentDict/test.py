#! /usr/bin/env python
# coding: utf-8
__author__ = 'Luffy'
import sys

a = [1]
b = list(a)
print id(a), a, id(b), b
import calendar
cal = calendar.month(2016, 3)
print cal
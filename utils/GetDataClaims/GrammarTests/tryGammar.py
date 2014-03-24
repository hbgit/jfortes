#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-
__author__ = 'Herbert OLiveira Rocha'


from pyparsing import *
import ebnf
import sets

grammar = """
digit_zero = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
digit                = "0" | digit_zero ;
"""



e = ebnf.parse(grammar)
#
tokens = e['digit'].parseString('5')
#e.parseString('5')

for i,token in enumerate(tokens):
    print(i,token)

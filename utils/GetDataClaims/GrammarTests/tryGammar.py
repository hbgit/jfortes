#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-
__author__ = 'Herbert OLiveira Rocha'


from pyparsing import *
import ebnf
import sets

grammar = """
prog =	(expr NEWLINE)* ;
expr =	expr ('*'|'/') expr
    |	expr ('+'|'-') expr
    |	INT
    |	'(' expr ')'
    ;
NEWLINE = [\r\n]+ ;
INT     = [0-9]+ ;
"""



e = ebnf.parse(grammar)
#
tokens = e['digit'].parseString('5122333')
print(tokens)
#e.parseString('5')

#for i,token in enumerate(tokens):
#    print(i,token)

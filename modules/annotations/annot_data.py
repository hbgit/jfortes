#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-
__author__ = 'lbentes'

class AnnotData(object):
    def __init__(self, listOfAnnot, listOfInput):
        self.name = listOfAnnot['attrName']
        self.seq = listOfAnnot['attrSequence']
        self.arg = listOfInput['Type']
        self.typeAnnot = listOfAnnot['annot_name']

    def getName(self):
        return self.name

    def getSequence(self):
        return self.seq

    def getArgs(self):
        return self.arg

    def getConstructors(self):
        allconstructors = []
        cont = -1
        for i in self.typeAnnot:
            constructor = []
            cont += 1
            if i == "jfortes_constructor":
                constructor.append(self.name[cont])
                constructor.append(self.seq[cont])
                constructor.append(self.arg[cont])
                allconstructors.append(constructor)
        return allconstructors

    def getAttributes(self):
        allattributes = []
        cont = -1
        for i in self.typeAnnot:
            attribute = []
            cont += 1
            if i == "jfortes_attribute":
                attribute.append(self.name[cont])
                attribute.append(self.seq[cont])
                attribute.append(self.arg[cont])
                allattributes.append(attribute)
        return allattributes

    def getMethods(self):
        allmethods = []
        cont = -1
        for i in self.typeAnnot:
            method = []
            cont += 1
            if i == "jfortes_method":
                method.append(self.name[cont])
                method.append(self.seq[cont])
                method.append(self.arg[cont])
                allmethods.append(method)
        return allmethods


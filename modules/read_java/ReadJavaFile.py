#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-

__author__ = 'Herbert OLiveira Rocha'


from modules.utils import ReaderCsvOutput


class ReadJavaFile(object):


    def __init__(self):
        self.file_actual_number_line  = 0


    def readFile(self, _javaPathFile):

        javafile = open(_javaPathFile)
        linesjavafile = javafile.readlines()
        javafile.close()

        for index, line in enumerate(linesjavafile):
            self.file_actual_number_line = index
            print("%s - %s" % (self.file_actual_number_line,line), end="")


    def instrumentCodeAssert(self, _javaPathFile, _csvPathFileToInst):
        javafile = open(_javaPathFile)
        linesjavafile = javafile.readlines()
        javafile.close()

        readCsv = ReaderCsvOutput.ReaderCsv()
        readCsv.loadCsvFile(_csvPathFileToInst)
        listOfCsvColummns = readCsv.getCsvColummns()


        for index, line in enumerate(linesjavafile):
            self.file_actual_number_line = index
            print(line, end="")
            #STOP. TODO: Identify the lines to be instrumented, and then generated a new instance of the code


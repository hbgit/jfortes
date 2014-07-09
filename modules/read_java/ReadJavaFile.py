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

        #text of the new program
        list_program_asserts = []

        javafile = open(_javaPathFile)
        linesjavafile = javafile.readlines()
        javafile.close()

        readCsv = ReaderCsvOutput.ReaderCsv()
        readCsv.loadCsvFile(_csvPathFileToInst)
        listOfCsvNewClColummns = readCsv.getCsvColummns()


        for index, line in enumerate(linesjavafile):
            self.file_actual_number_line = index
            for i, numLineCl in enumerate(listOfCsvNewClColummns['Number_of_line']):
                # Identify the lines to be instrumented
                numToCompare = int(numLineCl) - 1
                if numToCompare == index:
                    # DEBUG print(">>>>>>>>",numLineCl)
                    # generating the new with the assertion based on the claim
                    #print("assert( %s );" % str(listOfCsvNewClColummns['New_claim'][i]))
                    list_program_asserts.append("assert( "+str(listOfCsvNewClColummns['New_claim'][i])+" );")

            #print(line, end="")
            list_program_asserts.append(str(line).rstrip())

        return list_program_asserts




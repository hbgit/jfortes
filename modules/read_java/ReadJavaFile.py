#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-
from cups import modelSort

__author__ = 'Herbert OLiveira Rocha'


import sys
import commands
import re


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


    def checkClaimsFileEgual(self, _beforefilepre, _afterfilepre):
        numlinesbefore = 0
        numlinesafter = 0
        with open(_beforefilepre) as f:
            total = sum(1 for _ in f)

        numlinesbefore = total

        with open(_afterfilepre) as f:
            total = sum(1 for _ in f)

        numlinesafter = total

        if numlinesbefore == numlinesafter:
            return True
        else:
            return False


    def instrumentCodeAssert(self, _javaPathFile, _claimsbeforeprecode, _csvPathFileToInst, _modelUnitTest):

        modelToApply = self.getModelUnitTest(_modelUnitTest)
        #print(">>>", modelToApply)

        # Check what model to test should be applied in the analyzed program
        if modelToApply == "testng":
            # verifiyng if there are differences of the claims file
            numclaimsegual = self.checkClaimsFileEgual(_claimsbeforeprecode, _csvPathFileToInst)
            if numclaimsegual:
                # with the line number
                # Write msg with the line number in the assertions
                list_new_program_inst = self.applyTestNgModel(_javaPathFile, _claimsbeforeprecode, _csvPathFileToInst)
                return list_new_program_inst
            else:
                list_new_program_inst = self.applyTestNgModel(_javaPathFile, _claimsbeforeprecode, _csvPathFileToInst)
                return list_new_program_inst

        elif modelToApply == "jcute":
            # verifiyng if there are differences of the claims file
            numclaimsegual = self.checkClaimsFileEgual(_claimsbeforeprecode, _csvPathFileToInst)
            if numclaimsegual:
                # with the line number
                # Write msg with the line number in the assertions
                list_new_program_inst = self.apply_jcute_model(_javaPathFile, _claimsbeforeprecode, _csvPathFileToInst)
                return list_new_program_inst
            else:
                list_new_program_inst = self.apply_jcute_model(_javaPathFile, _claimsbeforeprecode, _csvPathFileToInst)
                return list_new_program_inst

        elif modelToApply == "junit":
            list_new_program_inst = self.applyJunitModel(_javaPathFile, _csvPathFileToInst)
            return list_new_program_inst

        elif modelToApply == "NO":

            # verifiyng if there are differences of the claims file
            numclaimsegual = self.checkClaimsFileEgual(_claimsbeforeprecode, _csvPathFileToInst)

            #text of the new program
            list_program_asserts = []

            javafile = open(_javaPathFile)
            linesjavafile = javafile.readlines()
            javafile.close()

            #claims before preprocessing code
            readCsv = ReaderCsvOutput.ReaderCsv()
            readCsv.loadCsvFile(_csvPathFileToInst)
            listOfCsvFirstClColummns = readCsv.getCsvColummns()

            #claims after preprocessing code
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
                        if numclaimsegual:
                            # with the line number
                            #list_program_asserts.append("// Number line in the original code: "+str(listOfCsvFirstClColummns['Number_of_line'][i]))
                            list_program_asserts.append("assert "+str(listOfCsvNewClColummns['New_claim'][i])+" : "+\
                                                        " \" \\n IN ORIGINAL CODE AT LINE: < "+str(listOfCsvFirstClColummns['Number_of_line'][i])+"> " +\
                                                    "\\n COMMENT: "+str(listOfCsvFirstClColummns['Comment'][i])+"\\n \";")
                        else:
                            list_program_asserts.append("assert( "+str(listOfCsvNewClColummns['New_claim'][i])+" );")

                #print(line, end="")
                list_program_asserts.append(str(line).rstrip())

            return list_program_asserts


    def getModelUnitTest(self, _dicModelTest):
        for key, value in _dicModelTest.items():
            if value:
                return key



    def applyTestNgModel(self,_javaPathFile, _claimsbeforeprecode, _csvPathFileToInst):

        #TODO: Identify the pre-requirements to run test with TESTNG, e.g., the class needs to be public (public class Bag(){)
        #TODO: Add an option in jfortes to generate XML to run the tests
        #Fix bug in the translation: NULL to null; a.length() to a.length. Checkout other.

        #text of the new program
        list_program_asserts = []

        # Reading java file
        javafile = open(_javaPathFile)
        linesjavafile = javafile.readlines()
        javafile.close()

        #claims before preprocessing code
        readCsv = ReaderCsvOutput.ReaderCsv()
        readCsv.loadCsvFile(_csvPathFileToInst)
        listOfCsvFirstClColummns = readCsv.getCsvColummns()

        # Reading CSV file with the claims translated
        readCsv = ReaderCsvOutput.ReaderCsv()
        readCsv.loadCsvFile(_csvPathFileToInst)
        listOfCsvNewClColummns = readCsv.getCsvColummns()

        #claims after preprocessing code
        # Getting the number lines of the methods from the analyzed program
        listnumstartmethod = self.identifyNumLineOfMethods(_javaPathFile)

        # verifiyng if there are differences of the claims file
        numclaimsegual = self.checkClaimsFileEgual(_claimsbeforeprecode, _csvPathFileToInst)


        # Adding imports of the TestNG
        # TODO: BUG in the preprocessing code. It was added a blank space in the Assert import
        list_program_asserts.append("import org.testng.Assert; // <- [JFORTES]")
        list_program_asserts.append("import org.testng.annotations.Test; // <- [JFORTES]")
        list_program_asserts.append("")


        for index, line in enumerate(linesjavafile):
            self.file_actual_number_line = index

            # Checking if is a method header, i.e., start point
            if (index+1) in listnumstartmethod:
                list_program_asserts.append("@Test")


            for i, numLineCl in enumerate(listOfCsvNewClColummns['Number_of_line']):
                # Identify the lines to be instrumented
                numToCompare = int(numLineCl) - 1
                if numToCompare == index:
                    # DEBUG print(">>>>>>>>",numLineCl)
                    if numclaimsegual:
                        # generating the new with the assertion based on the claim
                        list_program_asserts.append("Assert.assertTrue( "+str(listOfCsvNewClColummns['New_claim'][i])+\
                                                    ", \" \\n IN ORIGINAL CODE AT LINE: < "+str(listOfCsvFirstClColummns['Number_of_line'][i])+"> " +\
                                                    "\\n COMMENT: "+str(listOfCsvFirstClColummns['Comment'][i])+"\\n \" );")
                    else:
                        # generating the new with the assertion based on the claim
                        list_program_asserts.append("Assert.assertTrue( "+str(listOfCsvNewClColummns['New_claim'][i])+" );")

            #print(line, end="")
            list_program_asserts.append(str(line).rstrip())

        return list_program_asserts


    def apply_jcute_model(self,_javaPathFile, _claimsbeforeprecode, _csvPathFileToInst):

        #text of the new program
        list_program_asserts = []

        # Reading java file
        javafile = open(_javaPathFile)
        linesjavafile = javafile.readlines()
        javafile.close()

        #claims before preprocessing code
        readCsv = ReaderCsvOutput.ReaderCsv()
        readCsv.loadCsvFile(_csvPathFileToInst)
        listOfCsvFirstClColummns = readCsv.getCsvColummns()

        # Reading CSV file with the claims translated
        readCsv = ReaderCsvOutput.ReaderCsv()
        readCsv.loadCsvFile(_csvPathFileToInst)
        listOfCsvNewClColummns = readCsv.getCsvColummns()

        #claims after preprocessing code
        # Getting the number lines of the methods from the analyzed program
        listnumstartmethod = self.identifyNumLineOfMethods(_javaPathFile)

        # verifiyng if there are differences of the claims file
        numclaimsegual = self.checkClaimsFileEgual(_claimsbeforeprecode, _csvPathFileToInst)


        # Adding imports of the TestNG
        # TODO: BUG in the preprocessing code. It was added a blank space in the Assert import
        list_program_asserts.append("import cute.Cute; // <- [JFORTES]")
        list_program_asserts.append("")


        for index, line in enumerate(linesjavafile):
            self.file_actual_number_line = index

            for i, numLineCl in enumerate(listOfCsvNewClColummns['Number_of_line']):
                # Identify the lines to be instrumented
                # Identify the lines to be instrumented
                numToCompare = int(numLineCl) - 1
                if numToCompare == index:
                    list_program_asserts.append("// IN ORIGINAL CODE AT LINE: < "+str(listOfCsvFirstClColummns['Number_of_line'][i])+" > ")
                    list_program_asserts.append("// COMMENT: "+str(listOfCsvFirstClColummns['Comment'][i]))
                    list_program_asserts.append("Cute.Assert( " + str(listOfCsvNewClColummns['New_claim'][i]) + "); ")


            #print(line, end="")
            list_program_asserts.append(str(line).rstrip())

        return list_program_asserts



    def applyJunitModel(self,_javaPathFile, _csvPathFileToInst):
        print("Sorry about that. This model is not support yet :( ")
        sys.exit()


    def identifyNumLineOfMethods(self,_javaPathFile):

        # list of the line number where a method is started
        listnumstartmethods = []

        # Gettting the name of the functions
        get_start_data_method = commands.getoutput("ctags --sort=NO -x --c-kinds=f "+_javaPathFile).split("\n")
        for line in get_start_data_method:
            #print(line)
            matchDataMethod = re.search(r'([a-zA-Z0-9\_\(\)\[\]]*)[ ]*([a-zA-Z0-9]*)[ ]*([0-9]*)', line)
            if matchDataMethod:
                if matchDataMethod.group(2) == "method":
                    #print(matchDataMethod.group(1))
                    #self.list_name_func.append(matchDataMethod.group(1))
                    #print(">>>>> "+matchDataMethod.group(3))
                    listnumstartmethods.append(int(matchDataMethod.group(3)))
                    #self.list_num_start_func.append(matchDataMethod.group(3))

        return listnumstartmethods



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


    def instrumentCodeAssert(self, _javaPathFile, _claimsbeforeprecode, _csvPathFileToInst, _modelUnitTest, _datafileinput):

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
                list_new_program_inst = self.apply_jcute_model(_javaPathFile, _claimsbeforeprecode, _csvPathFileToInst, _datafileinput)
                return list_new_program_inst
            else:
                list_new_program_inst = self.apply_jcute_model(_javaPathFile, _claimsbeforeprecode, _csvPathFileToInst, _datafileinput)
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


    def apply_jcute_model(self,_javaPathFile, _claimsbeforeprecode, _csvPathFileToInst, _datafileinput):

        #Identify if the program has main
        hasmain = self.has_main_method(_javaPathFile)

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

        lenoffile = len(linesjavafile)

        for index, line in enumerate(linesjavafile):

            self.file_actual_number_line = index

            for i, numLineCl in enumerate(listOfCsvNewClColummns['Number_of_line']):
                # Identify the lines to be instrumented

                numToCompare = int(numLineCl) - 1
                #print(numToCompare+" = "+index)
                if numToCompare == index:
                    list_program_asserts.append("// IN ORIGINAL CODE AT LINE: < "+str(listOfCsvFirstClColummns['Number_of_line'][i])+" > ")
                    list_program_asserts.append("// COMMENT: "+str(listOfCsvFirstClColummns['Comment'][i]))
                    list_program_asserts.append("Cute.Assert( " + str(listOfCsvNewClColummns['New_claim'][i]) + "); ")


            if lenoffile == (index+1):
                # Write a generic main to test the method
                if not hasmain:
                    #TODO:
                    #Adding a new main based on data gathered form parser
                    #print(_datafileinput)
                    list_program_asserts.append("public static void main(String[] args){")

                    # Reading CSV file with the claims translated
                    readCsvi = ReaderCsvOutput.ReaderCsv()
                    readCsvi.loadCsvFile(_datafileinput)
                    listOfCsvDataInput = readCsvi.getCsvColummns()

                    #Creating instance of the class
                    list_not_gen = []
                    listclasses = self.list_all_class(_javaPathFile)
                    #if not len(listclasses) == 0
                    # Identify the contructor method
                    flag_has_constructor = False
                    for i, item in enumerate(listOfCsvDataInput['From']):
                        if item == "method":
                            # Identify if is a contructor method
                            if listOfCsvDataInput['Scope'][i] in listclasses:
                                flag_has_constructor = True
                                list_not_gen.append(i)
                                # has array in input?
                                analysisInput = self.is_list_input(listOfCsvDataInput['Type'][i])

                                if analysisInput[0]:
                                    tmpvararray = ''
                                    if analysisInput[1] == "int":
                                        tmpvararray = self.generateArrayInt(analysisInput[2])
                                    list_program_asserts.append(tmpvararray[0])
                                    list_program_asserts.append(
                                        listOfCsvDataInput['Scope'][i]+" runJFORTES = new "
                                        +listOfCsvDataInput['Scope'][i]+"( " + tmpvararray[1] + " );")
                                else:
                                    list_program_asserts.append(
                                        listOfCsvDataInput['Scope'][i]+" runJFORTES = new "
                                        +listOfCsvDataInput['Scope'][i]+"( );")

                    if not flag_has_constructor:
                        for classname in listclasses:
                            list_program_asserts.append(
                                        classname+" runJFORTES = new "
                                        +classname+"( );")


                    # DOING: Adding the attributes
                    for i, item in enumerate(listOfCsvDataInput['From']):
                        if item == "attribute":
                            # has array in input?
                            analysisInput = self.is_list_input(listOfCsvDataInput['Type'][i])
                            if analysisInput[0]:
                                genassignment = ''
                                if analysisInput[1] == "int":
                                    if analysisInput[2] == 1:
                                        genassignment = 'runJFORTES.'+listOfCsvDataInput['Variable'][i].strip()+' = new int [Cute.input.Integer()];'
                                        list_program_asserts.append(genassignment)
                                elif analysisInput[1] == "Object":
                                    if analysisInput[2] == 1:
                                        genassignment = 'runJFORTES.'+listOfCsvDataInput['Variable'][i].strip()+' = new Object [Cute.input.Object(".")];'
                                        list_program_asserts.append(genassignment)
                            else:
                                if listOfCsvDataInput['Type'][i] == 'int':
                                    genassignment = 'runJFORTES.'+listOfCsvDataInput['Variable'][i].strip()+' = Cute.input.Integer();'
                                    list_program_asserts.append(genassignment)

                                #sys.exit()
                                #

                    # DOING: Adding the methods
                    i = 0
                    while i < len(listOfCsvDataInput['From']):
                    #for i, item in enumerate(listOfCsvDataInput['From']):
                        if listOfCsvDataInput['From'][i] == "method" and not i in list_not_gen:
                            # With parameters
                            if not listOfCsvDataInput['Type'][i] == "0NONE":
                                #print("Generate parameters")
                                # has array in input?
                                analysisInput = self.is_list_input(listOfCsvDataInput['Type'][i])
                                if not analysisInput[0]:
                                    # Possible method with multiples inputs
                                    if (i+1) < len(listOfCsvDataInput['From']):
                                        flag_walk = True
                                        init_method = 'runJFORTES.'+listOfCsvDataInput['Scope'][i].strip()+'('
                                        list_args_input = []
                                        while i+1 < len(listOfCsvDataInput['From']) and flag_walk:
                                            if listOfCsvDataInput['Line'][i] == listOfCsvDataInput['Line'][i+1]:

                                                #list_args_input.append('TODO')
                                                # TODO: Replace by a function
                                                # has array in input?
                                                analysisInput = self.is_list_input(listOfCsvDataInput['Type'][i])
                                                if analysisInput[0]:
                                                    genassignment = ''
                                                    if analysisInput[1] == "int":
                                                        if analysisInput[2] == 1:
                                                            list_args_input.append('int[] inM_JFORTES = new int [Cute.input.Integer()]')
                                                    elif analysisInput[1] == "Object":
                                                        if analysisInput[2] == 1:
                                                            list_args_input.append('Object[] inM_JFORTES = new Object [Cute.input.Object()]')

                                                else:
                                                    if listOfCsvDataInput['Type'][i] == 'int':
                                                        list_args_input.append('Cute.input.Integer()')

                                                i += 1
                                                if not i+1 < len(listOfCsvDataInput['From']):
                                                    flag_walk = False
                                                elif listOfCsvDataInput['Line'][i] == listOfCsvDataInput['Line'][i+1]:
                                                    #list_args_input.append('TODO')
                                                    # TODO: Replace by a function
                                                    # has array in input?
                                                    analysisInput = self.is_list_input(listOfCsvDataInput['Type'][i])
                                                    if analysisInput[0]:
                                                        genassignment = ''
                                                        if analysisInput[1] == "int":
                                                            if analysisInput[2] == 1:
                                                                list_args_input.append('int[] inM_JFORTES = new int [Cute.input.Integer()]')
                                                        elif analysisInput[1] == "Object":
                                                            if analysisInput[2] == 1:
                                                                list_args_input.append('Object[] inM_JFORTES = new Object [Cute.input.Object()]')

                                                    else:
                                                        if listOfCsvDataInput['Type'][i] == 'int':
                                                            list_args_input.append('Cute.input.Integer()')
                                            else:
                                                flag_walk = False
                                        genassignment = ','.join(list_args_input)
                                        list_program_asserts.append(init_method+genassignment+');')
                                    # only one input arg
                                    else:
                                        # TODO: generate the args input
                                        genassignment = 'runJFORTES.'+listOfCsvDataInput['Scope'][i].strip()+'();'
                                        list_program_asserts.append(genassignment)

                                # TODO for arrays
                            else:
                                genassignment = 'runJFORTES.'+listOfCsvDataInput['Scope'][i].strip()+'();'
                                list_program_asserts.append(genassignment)

                        i += 1




                    list_program_asserts.append("}")



            list_program_asserts.append(str(line).rstrip())

        return list_program_asserts


    def is_list_input(self, _typetext):
        list_result = [] # True|False, type , array dimension
        matchQuantifiers = re.search(r'(.*)([\[][ ]*[\]])+', _typetext)
        if matchQuantifiers:
            list_result.append(True)
            list_result.append(matchQuantifiers.group(1))
            dim = matchQuantifiers.group(2).split('[').count(']')
            list_result.append(dim)
        else:
            list_result.append(False)
        return list_result


    def generateArrayInt(self, _dimension):
        codetxt = [] # new line, the var
        # For 1
        if _dimension == 1:
            codetxt.append('int[] arrJFORTES = new int [Cute.input.Integer()];')
            codetxt.append('arrJFORTES')
        return codetxt




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


    def has_main_method(self,_javaPathFile):
        # Gettting the name of the functions
        get_start_data_method = commands.getoutput("ctags --sort=NO -x --c-kinds=f "+_javaPathFile).split("\n")
        for line in get_start_data_method:
            #print(line)
            matchData = re.search(r'([a-zA-Z0-9\_\(\)\[\]]*)[ ]*([a-zA-Z0-9]*)[ ]*([0-9]*)', line)
            if matchData:
                #print(matchData.group(1)+" >> "+matchData.group(2))
                #sys.exit()
                if matchData.group(2) == "method":
                    if matchData.group(1) == "main":
                        return True
                    else:
                        return False


    def list_all_class(self, _javaPathFile):
        resultlistclasses = []
        # Gettting the name of the functions
        get_start_data_method = commands.getoutput("ctags --sort=NO -x --c-kinds=f "+_javaPathFile).split("\n")
        for line in get_start_data_method:
            #print(line)
            matchData = re.search(r'([a-zA-Z0-9\_\(\)\[\]]*)[ ]*([a-zA-Z0-9]*)[ ]*([0-9]*)', line)
            if matchData:
                if matchData.group(2) == "class":
                    resultlistclasses.append(matchData.group(1))

        return resultlistclasses





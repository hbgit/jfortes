#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-


# ------------------------------------------------------------------------
# TODO: Apply doc annotations in the programs
# TODO: BUG in test cases path with space
# TODO: Check when a test case to have main method
# ------------------------------------------------------------------------


__author__ = 'Herbert OLiveira Rocha'

# From Python
import sys
import re
import commands
import os
import argparse


# From JFORTES
from modules.get_data_claims import GetDataClaims
from modules.get_data_claims import ClaimsTranslate
from modules.uncrustify import RunPreprocessor
from modules.read_java import ReadJavaFile

class Jfortes(object):

    def __init__(self):
        self.ABS_PATH = os.path.dirname(__file__)
        self.javaFilePath = ""
        self.javaClassPath = ""
        self.setTranslationTest = False
        self.list_tmp_files = []



    def load_java_path(self, javafile, javaClassPath):
        """
        This method loads the java file to run ESC/Java
        :param javafile: The path of the java file
        :return : The result of the ESC/Java execution
        """
        self.javaFilePath = javafile
        self.javaClassPath = javaClassPath

        # Pre-processing the source code of the program
        pathprefilejava = self.javaFilePath.replace(".java","_pre.java")
        self.list_tmp_files.append(pathprefilejava)
        self.pre_processing(self.javaFilePath, pathprefilejava)

        self.javaFilePath = pathprefilejava
        return self.run_esc_java(self.javaFilePath)


    def pre_processing(self, _javafile, _pathtoprefile):
        run_pre = RunPreprocessor.CodeBeautify()
        run_pre.runBeatifyTool(_javafile, _pathtoprefile)


    def run_esc_java(self, javafile):
        """
        This method executes the ESC/Java that receives as input the javafile,
        and then it saves the ESC/Java output in the file.escout
        :param javafile: The path of the java file
        :return outPathEscJava: The ESC/Java output saved in the file
        """
        # WARNNING to run ESCJ
	    # Set also in the bashrc
        # escj -ClassPath /usr/lib/java/jdk1.5.0_22/bin/  test_cases/primary_tests/Bag.java
        #savePathFile = javafile
        outPathEscJava = javafile.replace(".java",".escout")
        self.list_tmp_files.append(outPathEscJava)
        # For Debug
        #os.system("escj -ClassPath "+self.javaClassPath+" "+javafile)
        #sys.exit()

        esc_result_status = commands.getoutput("escj -ClassPath "+self.javaClassPath+" "+javafile+" &> "+outPathEscJava)

        return outPathEscJava



    def gather_data_claims(self, escJavaOutPut):
        """
        Gather the data from claims generated by ESC/Java
        :param escJavaOutPut: The output from ESC/Java
        :return: File with the data gathered from ESC/Java output
        """
        # Gather the data claim
        getData = GetDataClaims.GetDataClaims()
        getData.readFile(escJavaOutPut)

        outPathDataClaims = self.javaFilePath.replace(".java","_claims.csv")
        self.list_tmp_files.append(outPathDataClaims)

        fileClaims = open(outPathDataClaims, "w")

        fileClaims.write( getData.writeHeader2Csv() )
        # Lines of the file with the claims translated
        for line in getData.getDataClaims():
            #print(line)
            fileClaims.write(line+"\n")

        fileClaims.close()
        #sys.exit()
        return outPathDataClaims


    def translate_claims(self, claimsFile):
        translateCl = ClaimsTranslate.IsolateDataClaim()

        if self.setTranslationTest:
            translateCl.set_testing_flag()

        translateCl.loadDataFromCsv(claimsFile,self.javaFilePath)
        translateCl.generateScopeByLineNumber(self.javaFilePath)

        try:
            translateCl.getObjectPointed()
        except Exception as e:
            print(self.javaFilePath+" ; ERROR ; ERROR ; ERROR ; ERROR ; ERROR")
            #print("Unexpected error: ", sys.exc_info()[0])
            raise # reraises the exception


    def insert_claims(self, _javafile, _claimstranslatedfile):
        readjavafile = ReadJavaFile.ReadJavaFile()
        readjavafile.readFile(_javafile)


    def delete_tmp_files(self):
        for pathFile in self.list_tmp_files:
            os.remove(pathFile)



# -------------------------------------------------
# Main JFORTES program
# -------------------------------------------------

if __name__ == "__main__":

    # TODO: Create a verify settings like map2check

    # --- Parse args options
    parser = argparse.ArgumentParser(description='Run JFORTES v1')
    parser.add_argument('-v','--version', action='version' , version="version 1")
    parser.add_argument(dest='inputJavaProgram', metavar='file.java', type=str,
               help='the Java program file to be analyzed')
    parser.add_argument('-t','--translation-test', action="store_true" , dest='setTranslationTest',
               help='run jfortes only to test the translation of the claims, where the ouput is as following: '
                    'Program ; NOT translation ; INCOMPLETE translation ; FAILED translation ; OKAY translation', default=False)
    parser.add_argument('-i','--insert-claims', type=str , metavar='file.claims', dest='inputClaimsFile',
               help='run jfortes only to insert assertion with claims in the analyzed program', default=False)

    args = parser.parse_args()

    # --- Check options in the args
    if args.inputJavaProgram:
        if not os.path.isfile(args.inputJavaProgram):
            print('Error: unable to open input file (%s)' % args.inputJavaProgram)
            parser.parse_args(['-h'])
            sys.exit()
        else:

            if args.inputClaimsFile:
                    #only to insert the assertion with the claims in the analyzed program
                    runJfortes = Jfortes()
                    #parameters need: (1) java file and (2) claims translated file
                    runJfortes.insert_claims(os.path.abspath(args.inputJavaProgram), os.path.abspath(args.inputClaimsFile))
                    sys.exit()

            else:
                # Apply all steps of the JFORTES method
                runJfortes = Jfortes()
                getLoad = runJfortes.load_java_path(os.path.abspath(args.inputJavaProgram), "/usr/lib/java/jdk1.5.0_22/bin/")
                getDataClaim = runJfortes.gather_data_claims(getLoad)

                if args.setTranslationTest:
                    runJfortes.setTranslationTest = True

                runJfortes.translate_claims(getDataClaim)
                # Clean all tmp files generated
                runJfortes.delete_tmp_files()



#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-


# ------------------------------------------------------------------------
# TODO List
# - Apply doc annotations in the programs
# - BUG in test cases path with space
# - Check when a test case has not main method
# - Create option to allow the execution of each step individually
# - pos-preprocessing in the imports
# - wrong line numbers in the asserts for some test cases
# ------------------------------------------------------------------------


__author__ = 'Herbert OLiveira Rocha'

# From Python
import sys
import commands
import os
import argparse
import ConfigParser


# From JFORTES
from modules.get_data_claims import GetDataClaims
from modules.get_data_claims import ClaimsTranslate
from modules.uncrustify import RunPreprocessor
from modules.read_java import ReadJavaFile


# Global VAR
# Check setup to run the program
ABS_PATH_JFORTES = os.path.dirname(__file__)
# Checkin is was executed the {configure.py} and if the ESBMC path was added
PATH_FILE_SETTINGS = ABS_PATH_JFORTES+'/settings.cfg'
if not os.path.isfile(PATH_FILE_SETTINGS):
    print("--------------------------- ERROR: ")
    print('  >> Error: unable to find the { settings.cfg } file')
    print('  >> Please run ./configure to check the prerequisites to use JFORTES tool')
    sys.exit()


JAVA_PARSER = os.path.abspath('')+"/modules/parser/partjavaparser.jar"


class Jfortes(object):
    """
    Jfortes class is adopted as a main start point of the tool.
    In this class is controlled the flow of the JFORTES method, which has the
    following steps:

    * **(1)** Execution of ESC/JAVA;
    * **(2)** Beatify code (preprocesing);
    * **(3)** Execution of ESC/JAVA (this is to keep the track the original line number);
    * **(4)** Properties translation that is executed to convert the assertions from ESC/JAVA to assertion to be\
      executed in java programs;
    * **(5)** Test cases creation that is set the properties translate in asserts according to framework adopted by the user;
    * **(6)** Apply the unit test framework model (TestNG, JCUTE, or only java asserts) choose by the user
    * **(7)** Execution the tests
    """

    def __init__(self):
        """
        This method has the main function to initialize the attributes of the Jfortes class
        :return: void
        """
        self.ABS_PATH = os.path.dirname(__file__)
        self.javaFilePath = ""
        self.javaClassPath = ""
        self.setTranslationTest = False
        self.list_tmp_files = []
        self.path_csvclaims_ori_code = ""
        #Model of unit testing supported
        self.dic_model_unit_test = {'testng':False,'jcute':False,'junit':False, 'NO':True}



    def load_java_path(self, javafile, javaClassPath):
        """
        This method loads the java file to run ESC/Java

        :param javafile: The path of the java file.
        :type javafile: str
        :param javaClassPath: Java class path to run java programs.
        :type javaClassPath: str
        :returns: The file path that has the ESC/Java execution execution.

        >>> runJfortes.load_java_path(os.path.abspath("/tests/Bag.java"), "/usr/lib/java/jdk1.5.0_22/bin/java")
        """
        self.javaFilePath = javafile
        self.javaClassPath = javaClassPath

        # Getting claims from the code without preprocessing
        path_escout_ori_code = self.run_esc_java(self.javaFilePath,"._before_pre_escout")
        # Generating csv from self.path_escout_ori_code
        self.path_csvclaims_ori_code = self.gather_data_claims(path_escout_ori_code,"_before_pre_claims.csv")


        # Pre-processing the source code of the program
        pathprefilejava = self.javaFilePath.replace(".java","_pre.java")
        self.list_tmp_files.append(pathprefilejava)
        self.pre_processing(self.javaFilePath, pathprefilejava, True)

        self.javaFilePath = pathprefilejava
        return self.run_esc_java(self.javaFilePath,".escout")


    def pre_processing(self, _javafile, _pathtoprefile, _mode):
        """

        :param _javafile: The path of the java file
        :param _pathtoprefile: The path to save the java file preprocessed
        :param _mode: True to write the code preprocessed
        :type _mode: bool
        :return: void, this because this method only write the code preprocessed in a new file
        """

        run_pre = RunPreprocessor.CodeBeautify()
        run_pre.runBeatifyTool(_javafile, _pathtoprefile, _mode)


    def run_esc_java(self, _javafile, _nameextension):
        """
        This method executes the ESC/Java that receives as input the javafile,
        and then it saves the ESC/Java output in the <file>.escout

        :param _javafile: The path of the java file
        :type: __javafile: str
        :param _nameextension: The file extension where the ESC/JAVA output will be java
        :type: __nameextension: str
        :returns: The the path file that has the ESC/Java output

        >>> self.run_esc_java(os.path.abspath("/tests/Bag.java"),".escout")
        """
        # WARNNING to run ESCJ
	    # Set also in the bashrc
        # escj -ClassPath /usr/lib/java/jdk1.5.0_22/bin/  test_cases/primary_tests/Bag.java
        #savePathFile = javafile
        outPathEscJava = _javafile.replace(".java",_nameextension)
        self.list_tmp_files.append(outPathEscJava)
        # For Debug
        #os.system("escj -ClassPath "+self.javaClassPath+" "+_javafile)
        #os.system("escj -ClassPath "+self.javaClassPath+" -h")
        #sys.exit()

        esc_result_status = commands.getoutput("escj -ClassPath "+self.javaClassPath+" "+_javafile+" &> "+outPathEscJava)

        return outPathEscJava



    def gather_data_claims(self, _escJavaOutPut,_nameextension):
        """
        Gather the data from claims generated by ESC/Java

        :param _escJavaOutPut: The output from ESC/Java
        :type _escJavaOutPut: str
        :param _nameextension: The file extension where the data gathered will be saved
        :type _nameextension: str
        :return: The CSV file with the data gathered from ESC/Java output

        >>> self.gather_data_claims("/tmp/file.escout","_before_pre_claims.csv")
        """
        # Gather the data claim
        getData = GetDataClaims.GetDataClaims()
        getData.readFile(_escJavaOutPut)

        outPathDataClaims = self.javaFilePath.replace(".java",_nameextension)
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
        """
        This method translated the properties generated by ESC/JAVA. This translation
        is to generate an assertion to be executed in java code out of the ESC/JAVA flow.

        :param claimsFile: The path of the file with the ESC/JAVA properties
        :type claimsFile: str
        :return: The file path with the properties translated
        """
        translateCl = ClaimsTranslate.IsolateDataClaim()

        if self.setTranslationTest:
            translateCl.set_testing_flag()

        translateCl.loadDataFromCsv(claimsFile,self.javaFilePath)
        translateCl.generateScopeByLineNumber(self.javaFilePath)

        try:
            listofclaimstranslated =  translateCl.getObjectPointed()
            # write the claims translated in a temporary file
            # first create the file name
            pathclaimstranslated = self.javaFilePath.replace(".java","_newcl.csv")
            self.list_tmp_files.append(pathclaimstranslated)

            filecltranslated = open(pathclaimstranslated, "w")
            # Write header of the translated claims in the CSV file
            filecltranslated.write("Number_of_line;Ori_claim;New_claim;Comment\n")

            for line in listofclaimstranslated:
                #print(line)
                filecltranslated.write(line+"\n")

            filecltranslated.close()

            # the path temporary file with the claims translated
            return pathclaimstranslated

        except Exception as e:
            print(self.javaFilePath+" ; ERROR ; ERROR ; ERROR ; ERROR ; ERROR")
            #print("Unexpected error: ", sys.exc_info()[0])
            raise # reraises the exception


    def generate_data2input(self, _javafile):
        """
        This method call our java parser that identifies the attributes and
        the input args of the methods in the analyzed program, and then
        the parser creates a list that has: (1) the variables name;
        (2) the type of the variables; and (3) the line number where the variable is located
        in the code.

        :param _javafile: The file path to analyzed program
        :type _javafile: str
        :return:

        >>> runJfortes.generate_data2input(os.path.abspath("tests/Bag.java"))
        """
        #os.system("java -jar "+JAVA_PARSER+" "+_javafile)
        #sys.exit()
        rec_output = commands.getoutput("java -jar "+JAVA_PARSER+" "+_javafile)
        # Write data gathered in a file
        pathdatainput = self.javaFilePath.replace(".java","_datainput.csv")
        self.list_tmp_files.append(pathdatainput)

        filedata = open(pathdatainput, "w")
        filedata.write(rec_output)
        filedata.close()

        return pathdatainput


    def insert_claims(self, _javafile, _claimstranslatedfile, _datainputfile):
        """
        This method creates a new instance of the analyzed program, and then
        it adds in this new instance asserts with properties generated by ESC/JAVA.
        It is woth noting that in this point the variable self.dic_model_unit_test was
        defined with the name of the framework that user choose.


        :param _javafile: The file path to the analyzed program
        :param _claimstranslatedfile: The file path to the translated properties
        :param _datainputfile: The csv file path generated by the method generate_data2input
        :return: void, this because the method only generates the new program
        """


        readjavafile = ReadJavaFile.ReadJavaFile()
        #readjavafile.readFile(_javafile)
        list_new_program = readjavafile.instrumentCodeAssert(_javafile,
                                                             self.path_csvclaims_ori_code,
                                                             _claimstranslatedfile,
                                                             self.dic_model_unit_test,
                                                             _datainputfile)

        #write new program in a temporary file
        pathnewprogram = self.javaFilePath.replace(".java","_assert.java")
        self.list_tmp_files.append(pathnewprogram)

        filenewprogram = open(pathnewprogram, "w")

        for line in list_new_program:
            #print(line)
            filenewprogram.write(line+"\n")

        filenewprogram.close()

        # Pre-processing the source code of the program
        pathendfilejava = pathnewprogram.replace("_assert.java","_end.java")
        #self.list_tmp_files.append(pathendfilejava)
        self.pre_processing(pathnewprogram, pathendfilejava, False)


    def delete_tmp_files(self):
        """
        This method remove all temporary files generated
        by Jfortes class that are saved in the global var self.list_tmp_files

        :return: void, the method only remove the files
        """
        for pathFile in self.list_tmp_files:
            os.remove(pathFile)



# -------------------------------------------------
# Main JFORTES program
# -------------------------------------------------

if __name__ == "__main__":

    # Verify settings to JFORTES
    config = ConfigParser.ConfigParser()
    config.read(PATH_FILE_SETTINGS)
    java_path_settings = config.get('JAVA', 'java_path', 0)
    if java_path_settings == 'empty':
        print("Sorry, you need to set up the java path in settings.cfg file. See REAME file.")
        sys.exit()

    # --- Parse args options
    parser = argparse.ArgumentParser(description='Run JFORTES v1')
    parser.add_argument('-v','--version', action='version' , version="version 1")
    parser.add_argument(dest='inputJavaProgram', metavar='file.java', type=str,
               help='the Java program file to be analyzed')
    parser.add_argument('-n','--apply-testng-model', action="store_true" , dest='setTestNg',
                help='run jfortes and then apply the TestNG model to run unit testing', default=False)

    parser.add_argument('-j', '--apply-jcute-model', action="store_true", dest='setJCute',
                help='run jfortes and then apply the jCUTE model', default=False)

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
                    #only to insert the assertioln with the claims in the analyzed program
                    runJfortes = Jfortes()
                    #parameters need: (1) java file and (2) claims translated file
                    runJfortes.insert_claims(os.path.abspath(args.inputJavaProgram), os.path.abspath(args.inputClaimsFile))
                    sys.exit()

            else:
                # Apply all steps of the JFORTES method
                runJfortes = Jfortes()
                getLoad = runJfortes.load_java_path(os.path.abspath(args.inputJavaProgram), java_path_settings)
                getDataClaim = runJfortes.gather_data_claims(getLoad,"_claims.csv")

                if args.setTranslationTest:
                    runJfortes.setTranslationTest = True

                getPathCLTranslated = runJfortes.translate_claims(getDataClaim)

                getpathdatainput = runJfortes.generate_data2input(os.path.abspath(args.inputJavaProgram))

                # DOING apply a model of the framework unit test to run the assertions with the claims
                if args.setTestNg:
                    runJfortes.dic_model_unit_test['testng'] = True
                    runJfortes.dic_model_unit_test['NO'] = False
                elif args.setJCute:
                    runJfortes.dic_model_unit_test['jcute'] = True
                    runJfortes.dic_model_unit_test['NO'] = False



                # Insert in the analyzed program the claims translated adopting assertions
                runJfortes.insert_claims(runJfortes.javaFilePath, getPathCLTranslated, getpathdatainput)

                # Clean all tmp files generated
                runJfortes.delete_tmp_files()



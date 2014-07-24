#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-


__author__ = 'Larissa Bentes'

# From Python
import sys
import re
import commands
import os
import argparse
import csv

class RunTests(object):
    def __init__(self):
        self.actualProgram = ""
        self.contMethod = 0
        self.contMain = 0
        self.c = csv.writer(open("test_cases.csv", "wb"))


    def load_dir_and_run_recursive(self, _pathdir):
        contMainTotal = 0
        loc = 0
        p = 0
        idProgram = 0
        contMethodByProgram = 0
        print("ID;", end="")
        print("Path program;", end="")
        print("Lines;", end="")
        print("Has Main;", end="")
        print("Methods;")
        b = open('test.csv', 'w')
        a = csv.writer(b)

        for root, dirs, files in os.walk(_pathdir):
            for file in files:
                if file.endswith(".java"):
                    idProgram += 1
                    print (idProgram, end=";")
                    get_path_program = os.path.join(root, file)
                    self.actualProgram = get_path_program
                    print(get_path_program, end=";")
                    loc = commands.getoutput("wc -l " + get_path_program + "| grep -o \"^[^ ]*\"")
                    print(loc, end=";")
                    get_start_data_method = commands.getoutput(
                        "ctags --sort=NO -x --c-kinds=f " + get_path_program).split("\n")
                    contMethodByProgram = 0
                    self.contMain = 0
                    for line in get_start_data_method:
                        matchDataMethod = re.search(r'([a-zA-Z0-9\_\(\)\[\]]*)[ ]*([a-zA-Z0-9]*)[ ]*([0-9]*)', line)
                        if matchDataMethod:
                            if matchDataMethod.group(2) == "method":
                                contMethodByProgram += 1
                                self.contMethod += 1
                                if (matchDataMethod.group(1) == 'main'):
                                    self.contMain += 1
                                    contMainTotal += self.contMain

                    if self.contMain > 0:
                        print("Yes", end=";")
                    else:
                        print("No", end=";")
                    print (contMethodByProgram)
        p = (100 * contMainTotal) / idProgram
        print("Test cases:", idProgram)
        print("Test cases with main:", contMainTotal)
        print ("Percentage of test cases with main", p, "%")

        print ("Arquivo gerado com sucesso")



# -------------------------------------------------
# Identifica quantidade de casos de testes com o metodo main e sem.
# -------------------------------------------------

if __name__ == "__main__":
    # -------------- Parse args options
    parser = argparse.ArgumentParser(description='Run script')
    parser.add_argument(dest='dirTestCasesDir', metavar='program_directory', type=str,
                        help='Directory with the test cases in directories to be analyzed')

    args = parser.parse_args()

    #---------------Check options in the args
    if args.dirTestCasesDir:
        if not os.path.isdir(args.dirTestCasesDir):
            print('Error: unable to open find the dir (%s)' % args.dirTestCasesDir)
            parser.parse_args(['-h'])
            sys.exit()
        else:
            executeTests = RunTests()
            executeTests.load_dir_and_run_recursive(args.dirTestCasesDir)

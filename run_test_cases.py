#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-


__author__ = 'Herbert OLiveira Rocha'

# From Python
import sys
import re
import commands
import os
import argparse


class RunTests(object):

    def __init__(self):
        self.actualProgram = ""
        self.pathJfortes = os.path.abspath("jfortes.py")


    def load_dir_and_run_recursive(self, _pathdir):
        for root, dirs, files in os.walk(_pathdir):
            for file in files:
                if file.endswith(".java"):
                    get_path_program = os.path.join(root, file)
                    self.actualProgram = get_path_program
                    #print(get_path_program)
                    self.run_test_in_jfortes(get_path_program)


    def run_test_in_jfortes(self, _pathjavafile):
        saveresult = commands.getoutput(self.pathJfortes+" -t "+_pathjavafile)
        print(saveresult)



# -------------------------------------------------
# Main JFORTES program
# -------------------------------------------------

if __name__ == "__main__":
    #-------------- Parse args options
    parser = argparse.ArgumentParser(description='Run experiment using JFORTES v1')
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
            print("Program ; NOT translation ; INCOMPLETE translation ; FAILED translation ; OKAY translation")
            executeTests.load_dir_and_run_recursive(args.dirTestCasesDir)
#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-

__author__ = 'Herbert OLiveira Rocha'

#Python
import sys
import os


class CodeBeautify(object):

    def __init__(self):
        self.option_to_run_tool = ''
        self.path_tool = 'uncrustify'
        self.setFileConf = ''


    def setOptions2Run(self, options):
        self.option_to_run_tool = options


    def setConfigFile(self, filePath):
        self.setFileConf = filePath


    def runBeatifyTool(self, pathJavaProgram):
        cmdRun = self.path_tool+" "+self.option_to_run_tool+" -c "+self.setFileConf+" -f "+pathJavaProgram
        #print(cmdRun)
        os.system("./"+cmdRun)




if __name__ == "__main__":

    path_input_file=""

    if 1 < len(sys.argv):
        path_input_file  = sys.argv[1]

    run = CodeBeautify()
    op = "-q -l C"
    run.setOptions2Run(op)
    configFile = "ben.cfg"
    run.setConfigFile(configFile)

    run.runBeatifyTool(path_input_file)






#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-

__author__ = 'Herbert OLiveira Rocha'

#Python
import sys
import os
import commands


class CodeBeautify(object):

    """
    This class is to apply a preprocessing in the source code of the analyzed program, i.e.,
    beautifier the code to define a set of code styles, such as: one command per line, and the block delimiters ({).
    """

    def __init__(self):
        self.path_tool = os.path.abspath('modules/uncrustify/uncrustify')
        self.option_to_run_tool = "-q -l C"
        self.setFileConf = os.path.abspath("modules/uncrustify/ben.cfg")


    def setOptions2Run(self, options):
        """
        Set the option to uncrustify tool that performs the preprocessing.
        The default option is -q -l C.

        :param options: the options to perform the preprocessing by uncrustify tool.
        :type options: str
        """
        self.option_to_run_tool = options


    def setConfigFile(self, filePath):
        """
        Define the file with option to perform the preprocessing by uncrustify tool.

        :param filePath: the path of the config file
        :type filePath: str
        """
        self.setFileConf = filePath


    def runBeatifyTool(self, pathJavaProgram, _pathfiletosave, _mode):
        """
        Execute the shell command to perform the preprocessing with uncrustify.

        :param pathJavaProgram: path of the java file
        :type pathJavaProgram: str
        :param _pathfiletosave: path to save the output of the preprocessing code
        :type _pathfiletosave: str
        :param _mode: True to save the preprocessing output in a file or False to print the output in the screen.
        :type _mode: bool
        """
        if _mode:
            cmdRun = self.path_tool+" "+self.option_to_run_tool+" -c "+self.setFileConf+" -f "+pathJavaProgram
            #print(cmdRun)
            #commands.getoutput(cmdRun+" &> "+_pathfiletosave) # BUG
            result = commands.getoutput(cmdRun) # BUG
            fileoutputbeatify = file(_pathfiletosave, "w")
            fileoutputbeatify.write(result)
            fileoutputbeatify.close()

        else:
            cmdRun = self.path_tool+" "+self.option_to_run_tool+" -c "+self.setFileConf+" -f "+pathJavaProgram
            os.system(cmdRun)


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






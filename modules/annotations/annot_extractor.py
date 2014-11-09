#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-

__author__ = 'Herbert OLiveira Rocha'

#Python
import sys
import os
import commands
import re


class AnnotExtractor(object):
    """
    This class identify and gather all jfortes annotations
    in the analyzed java program
    """

    def __init__(self):
        self.numtotalannot = 0
        self.actualclassname = ''


    def gather_annot(self, _javaprogram):
        """
        The method analysis each line of the java program to identify and gather
        the jfortes annotations.

        :param _javaprogram: the java file path
        :type _javaprogram: str
        :return: it is a tmp file path in csv format with the following data:
                (1) the line number of the program where the annotation was identified;
                (2) the name of the class
                (3) the annotation.

        >>> runextractor.gather_annot(os.path.abspath('test_cases/Bag.java'))
        >>> 10?Bag?//@ jfortes_getSequenceConstructor name = Bag, args = b, sequence = 1;
        """

        javafile = open(_javaprogram,'r')
        javafilelines = javafile.readlines()
        javafile.close()

        #print("line_number?class_name?annotation")

        # list of annotations
        annot_list = []
        annot_list.append("line_number?class_name?annotation")

        for index, line in enumerate(javafilelines):
            # Identify the current class to be read
            # according to http://docs.oracle.com/javase/tutorial/java/javaOO/classdecl.html
            matchclassname = re.search(r'class[ ]*([a-zA-Z_0-9]*)', line)
            if matchclassname:
                self.actualclassname = matchclassname.group(1)

            # Searching by jfortes annotations

            # identify if the line is an annotation this from //@ name_of_annotation
            # TODO: Improve this to recognize /*@ jfortenote */
            matchIsAnnot = re.search(r'(//[ ]*@)', line)
            if matchIsAnnot:
                # getting only the jfortes annotations
                matchIsJfortesAnnot = re.search(r'(.*jfortes_.*)', line)
                if matchIsJfortesAnnot:
                    annot_list.append(str(index+1) + "?" + self.actualclassname + "?" + matchIsJfortesAnnot.group(1).strip())
                    #print(str(index+1) + "?" + self.actualclassname + "?" + matchIsJfortesAnnot.group(1).strip())

        return annot_list




# -------------------------------------------------
# Main JFORTES program
# -------------------------------------------------
# Just used for tests
if __name__ == "__main__":
    runextractor = AnnotExtractor()
    runextractor.gather_annot(os.path.abspath(sys.argv[1]))



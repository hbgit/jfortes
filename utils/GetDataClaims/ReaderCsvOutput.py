#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-
from collections import defaultdict

__author__ = 'Herbert OLiveira Rocha'


#----------------------------------------------------------
# Goal: This program aims to read the data gathered from
#       ESC/JAVA output.
#
# Status: [DOING]
#----------------------------------------------------------

# Python Imports
import sys
import csv



class ReaderCsv(object):

    def __init__(self):
        self.flag_csv_reader = False
        self.columns = defaultdict(list) #we want a list to append each value in each column to


    def loadCsvFile(self, pathCsvFile):

        with open(pathCsvFile) as file:
            reader = csv.DictReader(file,delimiter=';')
            for row in reader:
                print(row)
                for (k,v) in row.items():
                    self.columns[k].append(v)
                    print(k)


    def printAllCsv(self):
        print(self.columns['Number_of_Line'])
        print(self.columns['Comments'])
        print(self.columns['Claim'])



# -------------------------------------------------
# Main python program
# -------------------------------------------------

if __name__ == "__main__":
    path_input_file = ""

    if len(sys.argv) > 1:
        path_input_file  = sys.argv[1]
    else:
        print("Incorrect Usage")
        print("Usage: ./script <CSV claims output")
        sys.exit()


    teste = ReaderCsv()
    teste.loadCsvFile(path_input_file)

    teste.printAllCsv()

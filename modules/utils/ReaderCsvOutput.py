#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-
from collections import defaultdict

__author__ = 'Herbert OLiveira Rocha'


#----------------------------------------------------------
# Goal:
#
# Status: [DOING]
#----------------------------------------------------------

# Python Imports
import sys
import csv



class ReaderCsv(object):
    """
    This Class aims to read a CSV file and the create a list for each column identify in the file.
    """

    def __init__(self):
        self.flag_csv_reader = False
        self.columns = defaultdict(list) #we want a list to append each value in each column to


    def loadCsvFile(self, pathCsvFile):
        """
        Read the csv file and split the csv column using the delimiter ; where each
        csv column is added in separeted list.

        :param pathCsvFile: path of the csv file
        :type pathCsvFile: str
        """

        with open(pathCsvFile) as file:
            reader = csv.DictReader(file,delimiter=';')
            for row in reader:
                #print(row)
                for (k,v) in row.items():
                    self.columns[k].append(v)
                    #print(k)


    def getCsvColummns(self):
        """
        Get all columns from a csv file where now each column were saved in a list.

        :return: a list of lists where each list is a column from the csv file.
        """
        return self.columns


    def printAllCsv(self):
        """
        Adopted to test the csv collector.
        """
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

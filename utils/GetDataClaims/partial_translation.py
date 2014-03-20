#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-
__author__ = 'Herbert OLiveira Rocha'


#----------------------------------------------------------
# Goal: This program aims to do a partial translation of the claim.
#       The focus of this program is isolate the variable or structure
#       related in the claim.
#
# Status: [DOING]
#----------------------------------------------------------


# From Python
import sys
import csv
from collections import defaultdict



class IsolateDataClaim(object):
    """
    This class has as main function isolate the variable or structure
    related in the claim
    """

    def __init__(self):
        self.claim_list_line_num = []
        self.claim_list_comments = []
        self.claim_list_claim = []
        self.claim_list_point_data = []

        # CSV input
        self.pathCsvFile = ''
        self.columns_csv = defaultdict(list) #we want a list to append each value in each column to


    def loadDataFromCsv(self, file):
        self.pathCsvFile = file
        with open(self.pathCsvFile) as file:
            reader = csv.DictReader(file,delimiter=';')
            for row in reader:
                for (k,v) in row.items():
                    self.columns_csv[k].append(v)

        self.setData2Lists()


    def setData2Lists(self):
        for line,comm,claim,pt_data in zip(self.columns_csv['Number of Line'],self.columns_csv['Comments'],self.columns_csv['Claim'],self.columns_csv['Point Data']):
            self.claim_list_line_num.append(line)
            self.claim_list_comments.append(comm)
            self.claim_list_claim.append(claim)
            self.claim_list_point_data.append(pt_data)


    def showDataLoaded(self):
        print(self.claim_list_line_num)
        print(self.claim_list_comments)
        #print(self.claim_list_claim)
        #print(self.claim_list_point_data)

        self.getObjectPointed()


    def getObjectPointed(self):
        """
        This method is related to get the object pointed by
        identifier in the claim
        """
        for eachCl,pt_data in zip(self.claim_list_claim,self.claim_list_point_data):
            # Generating a list from the text claim
            list_tmp_cl = list(eachCl)
            # Getting the index position pointed by identified
            get_index = (len(list(pt_data)) - 1)
            print()
            # TODO: Now is necessary to define the rule to get the correct object,
            #       this based on the comments
            print("From claim:    %s" % eachCl)
            print("The object is: %s" % list_tmp_cl[get_index])
            print()







# -------------------------------------------------
# Main python program
# -------------------------------------------------

if __name__ == "__main__":
    path_input_file = ""

    if len(sys.argv) > 1:
        path_input_file  = sys.argv[1]
    else:
        print("Incorrect Usage")
        print("Usage: ./script <csv file>")
        sys.exit()


    test = IsolateDataClaim()
    test.loadDataFromCsv(path_input_file)
    test.showDataLoaded()
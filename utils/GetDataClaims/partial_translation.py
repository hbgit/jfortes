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
import re
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
        self.claim_list_tag_comm = []

        # CSV input
        self.pathCsvFile = ''
        self.columns_csv = defaultdict(list) #we want a list to append each value in each column to

        # Dictionary of regex to get data claim
        # Here we have a list with regex and dictionary item related to tag_comm from claim
        self.regex_patterns = {
            # Case base: a[i] < m
            'IndexTooBig': ['[^\(]*']
        }


    def loadDataFromCsv(self, file):
        self.pathCsvFile = file
        with open(self.pathCsvFile) as file:
            reader = csv.DictReader(file,delimiter=';')
            for row in reader:
                for (k,v) in row.items():
                    self.columns_csv[k].append(v)

        self.setData2Lists()
        self.getTagsFromComments()


    def setData2Lists(self):
        for line,comm,claim,pt_data in zip(self.columns_csv['Number of Line'],self.columns_csv['Comments'],self.columns_csv['Claim'],self.columns_csv['Point Data']):
            self.claim_list_line_num.append(line)
            self.claim_list_comments.append(comm)
            self.claim_list_claim.append(claim)
            self.claim_list_point_data.append(pt_data)


    def getTagsFromComments(self):
        """
        This tag will help to apply the rules to get the objects pointed in the claim
        and also to apply the transformation rule
        """
        for eachComm in self.claim_list_comments:
            matchTag = re.search(r'\((.[^ ]*)\)$', eachComm)
            if matchTag:
                self.claim_list_tag_comm.append(matchTag.group(1).rstrip('\n'))


    def getObjectPointed(self):
        """
        This method is related to get the object pointed by
        identifier in the claim
        """
        id = 0
        while id < len(self.claim_list_claim):
            # Generating a list from the text claim
            list_tmp_cl = list(self.claim_list_claim[id])
            # Getting the index position pointed by identified
            get_index = (len(list(self.claim_list_point_data[id])) - 1)
            print()
            print("From claim   : %s" % self.claim_list_claim[id])
            print("Tag comment  : %s" % self.claim_list_tag_comm[id])
            # DOING: Create a method to select the object and then apply the transformation rule
            #       to the claims
            print("The translation: %s" % self.getObjectInClaim(self.claim_list_tag_comm[id],self.claim_list_claim[id],get_index))
            print()

            id += 1


    def getObjectInClaim(self, tagComm, claim, indexPointed):
        """
        Method to gather the object pointed in the claim
        """
        # TODO: Create a approach to get the object based on the tagComm
        #       Other point is thinking about how to get other objects
        #       need to execute the claim translation

        #self.isolateTextPointed(claim)

        if tagComm in ["IndexTooBig","IndexNegative"]:
            print(tagComm)
            # This tag is related to UPPER BOUND violation of ARRAY
            # I.e., A[I] -> "I < a.length()"
            # TODO: Here we isolate the text code located to gather the data

            #Isolating the text in the claim
            # Running the claim from indexPointed to last index of array name
            list_tmp_cl = list(claim)
            # How is an array we need isolate two parts the array name and the index
            # So we start to get the index
            tmpIndex = indexPointed
            isolateStrIndex = ''
            while list_tmp_cl[tmpIndex] != "]":
                #print(list_tmp_cl[tmpIndex],end="")
                isolateStrIndex += list_tmp_cl[tmpIndex]
                tmpIndex += 1
            isolateStrIndex += "]"


            # get the name array
            tmpIndex = indexPointed
            tmpIndex -= 1
            isolateStrVarArr = ''
            countFlag = 1
            while (not list_tmp_cl[tmpIndex] in ['(',')',';','=']) and (tmpIndex >= 0):
                matchBlank = re.search(r'\s', list_tmp_cl[tmpIndex])
                if not matchBlank:
                    countFlag += 1
                    isolateStrVarArr += list_tmp_cl[tmpIndex]

                if countFlag > 2:
                    tmpIndex = -1

                tmpIndex -= 1

            strIsolaCl = isolateStrVarArr+isolateStrIndex
            print("======> %s" % strIsolaCl)



    def isolateTextPointed(self, claim, indexPointed):
        return "as"









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
    #test.showDataLoaded()
    test.getObjectPointed()
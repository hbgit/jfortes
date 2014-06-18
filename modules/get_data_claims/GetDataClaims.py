#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-
__author__ = 'Herbert OLiveira Rocha'


#----------------------------------------------------------
# Goal: This program aims to gather the data in output from
#       the ESC/JAVA.
#
# Status: [DONE]
#----------------------------------------------------------



# From Python
import sys
import os.path
import re



class GetDataClaims(object):

    def __init__(self):
        self.list_lines_file = []
        self.list_data_claims_2_csv = []
        self.list_annoted_cl = ['Pre','Post','Invariant']
        self.list_claims_translated = []

    def readFile(self, pathFile):

        # Testing if the path file is correct
        if not os.path.exists(pathFile):
            print(pathFile)
            print('File path not found - Get data claims.')
            sys.exit()

        # Create a list with the lines with the file
        linesFile = open(pathFile,"r")
        for line in linesFile:
            self.list_lines_file.append(line)


    def prinFile(self):
        for line in self.list_lines_file:
            print(line, end="")


    def getDataClaims(self):

        flagNextBlock = False
        # Identify begin block, e.g., -----------------
        matchIdentifyBlock = re.compile(r'^-+')


        #print("Data about the claims: ")
        # print("-------------------------------------------------------------------")
        # Identifying block in the output with the data claims

        index = 0
        countBlocks = 0
        flag_write_csv = False

        while index < len(self.list_lines_file):

            # Identify begin block, e.g., -----------------
            matchTryBeginBlock = matchIdentifyBlock.match(self.list_lines_file[index])

            # Identify if in the claim block has the trace to variable in the claim
            flag_has_trace_var = False

            if matchTryBeginBlock:

                index += 1
                # Last check to identify the begin block
                # Check if the claim block has a counter example
                # IF has keep going to look for the next block
                # ELSE stop the search for the next block, because we already found the next block
                matchCheckBBlock = re.search(r'java:.*', self.list_lines_file[index])

                if matchCheckBBlock:

                    countBlocks += 1

                    #print(countBlocks)
                    #print("BEGIN: %s " % (index+1))

                    # Get the number of the number of line in the program where is located the claim
                    #print("\t At line: %s " % self.getNumLineInClaim(self.list_lines_file[index]))
                    self.list_data_claims_2_csv.append(self.getNumLineInClaim(self.list_lines_file[index]))

                    # Get comment about the claim, e.g.,  Warning:
                    comment_CL = self.getCommentInClaim(self.list_lines_file[index])
                    #print("\t Comment: %s " % comment_CL)
                    self.list_data_claims_2_csv.append(self.getCommentInClaim(self.list_lines_file[index]))
                    
                    
                    # Get tag from commets about the claim
                    tag_CL = self.getTagFromCommentCl(comment_CL)
                    self.list_data_claims_2_csv.append(tag_CL)
                    #print("\t Tag: %s" % tag_CL)
                    if str(tag_CL) in self.list_annoted_cl:                        
                            # Get the property in the claim block
                            index += 1                            
                            self.list_data_claims_2_csv.append(self.getClaim(self.list_lines_file[index]))
                            
                            # Get the variable location in the claim based on this ...^ <- Identifier
                            index += 1
                            self.list_data_claims_2_csv.append(self.list_lines_file[index].rstrip('\n'))
                                                        
                            ## Get Annoted info
                            index += 2
                            self.list_data_claims_2_csv.append(self.getClaim(self.list_lines_file[index]))
                            
                            ## Get the variable location in the claim based on this ...^ <- Identifier
                            index += 1
                            self.list_data_claims_2_csv.append(self.list_lines_file[index].rstrip('\n'))
                            

                    else:                    
                        # Get the property in the claim block
                        index += 1
                        #print("\t Claim: %s " % self.getClaim(self.list_lines_file[index]))
                        self.list_data_claims_2_csv.append(self.getClaim(self.list_lines_file[index]))

                        # Get the variable location in the claim based on this ...^ <- Identifier
                        index += 1
                        self.list_data_claims_2_csv.append(self.list_lines_file[index].rstrip('\n'))
                        
                        # Get Annoted info
                        self.list_data_claims_2_csv.append('None')
                        
                        # Get the variable location in the claim based on this ...^ <- Identifier
                        self.list_data_claims_2_csv.append('None')

                    flag_write_csv = True

                    # Identify the next block
                    while not flagNextBlock:

                        if index <= len(self.list_lines_file):
                            index += 1

                            # Identify end block
                            matchDelimitBlock = matchIdentifyBlock.match(self.list_lines_file[index])
                            if matchDelimitBlock:
                                # Here we identify the END of the block
                                flagNextBlock = True
                                #decrement the index, because is a new block
                                index -= 1
                                #print("END: %s " % (index+1))


                # reset flag
                flagNextBlock = False


            # write the line of CSV output
            if flag_write_csv:
                recFormatCsv = ';'.join(self.list_data_claims_2_csv)
                # if flag_has_trace_var:
                #     recFormatCsv = ' ; '.join(self.list_data_claims_2_csv)
                # else:
                #     recFormatCsv = ' ; '.join(self.list_data_claims_2_csv)
                #     recFormatCsv += ' ;  NO'
                #print(recFormatCsv)
                self.list_claims_translated.append( recFormatCsv )
                self.list_data_claims_2_csv = []
                flag_write_csv = False

            # While Increment
            index += 1



        return self.list_claims_translated
        #print("-------------------------------------------------------------------")


    def getNumLineInClaim(self, lineClaim):
        # Apply regex to get the  number of line i the claim
        matchNumLine = re.search(r'java:([0-9]+)', lineClaim)
        if matchNumLine:
            return matchNumLine.group(1)


    def getCommentInClaim(self, lineClaim):
        # Apply regex to get the  number of line i the claim
        matchNumLine = re.search(r'Warning:(.+)', lineClaim)
        if matchNumLine:
            return matchNumLine.group(1)
            
    def getTagFromCommentCl(self, comment):
        matchTag = re.search(r'\((.[^ ]+)\)$', comment)
        if matchTag:
            return matchTag.group(1)
            
    

    def getClaim(self, lineClaim):
        # Apply regex to get the claim of line i the claim
        matchNumLine = re.search(r'(.[^;]*)', lineClaim)
        #matchNumLine = re.search(r'(.[^=]*)[ ]*;', lineClaim)
        if matchNumLine:
            return matchNumLine.group(1).rstrip('\n')


    def writeHeader2Csv(self):
        head = ['Number of Line','Comments','Tag','Claim','Point Data','Annoted','Annoted Point']
        recFormatCsv = ';'.join(head)
        return recFormatCsv+"\n"




# -------------------------------------------------
# Main python program
# -------------------------------------------------

# if __name__ == "__main__":
#     path_input_file = ""
#
#     if len(sys.argv) > 1:
#         path_input_file  = sys.argv[1]
#     else:
#         print("Incorrect Usage")
#         print("Usage: ./script <output from ESC/JAVA>")
#         sys.exit()
#
#     test = GetDataClaims()
#     test.readFile(path_input_file)
#     #test.prinFile()
#     test.writeHeader2Csv()
#     test.getDataClaims()




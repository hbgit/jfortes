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
import commands
import os
from collections import defaultdict



class IsolateDataClaim(object):
    """
    This class has as main function isolate the variable or structure
    related in the claim

    TODO: Remove unsed code <- development process
    """

    def __init__(self):
        self.pathJavaFile = ''
        
        self.claim_list_line_num = []
        self.claim_list_comments = []
        self.claim_list_claim = []
        self.claim_list_point_data = []
        self.claim_list_tag_comm = []
        self.claim_list_annoted = []
        self.claim_list_annoted_pt = []
        
        #Data scope function
        self.list_name_func = []
        self.list_num_start_func = []
        self.list_num_end_func = []


        # Flags
        self.DEBUG_STATUS = False
        self.PRETTY_PRINT = False


        # CSV input
        self.pathCsvFile = ''
        self.columns_csv = defaultdict(list) #we want a list to append each value in each column to

        # Dictionary of regex to get data claim
        # Here we have a list with regex and dictionary item related to tag_comm from claim
        self.regex_patterns = {
            # Case base: a[i] < m
            'IndexTooBig': ['[^\(]*']
        }

        # Atributes for tags
        self.claim_translated = ''
        self.tag_name_array = ''
        self.tag_index_array = ''


    def set_debug_flag(self):
        self.DEBUG_STATUS = True


    def set_pretty_print(self):
        self.PRETTY_PRINT = True



    def loadDataFromCsv(self, csvFileClaims, javaFile):
        self.pathCsvFile = csvFileClaims
        self.pathJavaFile = javaFile
        with open(self.pathCsvFile) as csvFileClaims:
            reader = csv.DictReader(csvFileClaims,delimiter=';')
            for row in reader:
                for (k,v) in row.items():
                    self.columns_csv[k].append(v)

        self.setData2Lists()
        self.getTagsFromComments()


    def setData2Lists(self):
        for line,comm,claim,pt_data,tag,annoted,annoted_pt in zip(self.columns_csv['Number of Line'],self.columns_csv['Comments'],self.columns_csv['Claim'],self.columns_csv['Point Data'],self.columns_csv['Tag'],self.columns_csv['Annoted'],self.columns_csv['Annoted Point']):
            if self.DEBUG_STATUS:
                print("Data gather from csv file: ")
                print("Line    : ",line)
                print("Comments: ",comm)
                print("Claim   : ",claim)
                print("Pt claim: ",pt_data)
                print("Annoted : ",annoted)
                print("Pt annot: ",annoted_pt)
                print()
            
            self.claim_list_line_num.append(line)
            self.claim_list_comments.append(comm)
            self.claim_list_claim.append(claim)
            self.claim_list_point_data.append(pt_data)
            self.claim_list_annoted.append(annoted)
            self.claim_list_annoted_pt.append(annoted_pt)
            
        if self.DEBUG_STATUS:
            print("%s" % ("-"*50))


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
        if not self.DEBUG_STATUS and not self.PRETTY_PRINT:
            print("Number of Line ; Original Claim ; Claim Translated ; Comments ")

        if self.PRETTY_PRINT:
            print("%11s ;%11s ;%11s ;%11s " % ("Number of Line","Original Claim","Claim Translated","Comments"))
            print("%s" % ("-"*90))

        
        # >> Starting translation
        
        while id < len(self.claim_list_claim):
            
            # Generating a list from the text claim
            list_tmp_cl = list(self.claim_list_claim[id])
            # Getting the index position pointed by identified
            get_index = (len(list(self.claim_list_point_data[id])) - 1)

            if self.DEBUG_STATUS:
                print()
                print(">> Claim translation << ")
                print("From claim   : %s" % self.claim_list_claim[id])
                print("Tag comment  : %s" % self.claim_list_tag_comm[id])
                # DOING: Create a method to select the object and then apply the transformation rule
                #       to the claims
                print("The translation: %s" % self.getObjectInClaim(self.claim_list_line_num[id], self.claim_list_tag_comm[id],self.claim_list_claim[id],get_index,self.claim_list_annoted[id]))
                print()
            # Print the new csv
            else:
                claim_translated = self.getObjectInClaim(self.claim_list_line_num[id], self.claim_list_tag_comm[id],self.claim_list_claim[id],get_index, self.claim_list_annoted[id])

                if self.PRETTY_PRINT:
                    print("%3s ;%50s ;%20s ;%11s " % (self.claim_list_line_num[id].strip(),self.claim_list_claim[id].strip(),str(claim_translated),self.claim_list_comments[id].strip()))
                else:
                    row = self.claim_list_line_num[id].strip()+" ; "+self.claim_list_claim[id].strip()+" ; "+str(claim_translated)+" ; "+self.claim_list_comments[id].strip()
                    print(row)

            id += 1

        if self.PRETTY_PRINT:
            print("%s" % ("-"*90))


    def getObjectInClaim(self, lineNumber, tagComm, claim, indexPointed, annoted):
        """
        Method to gather the object pointed in the claim
        """
        # TODO: Create a approach to get the object based on the tagComm
        #       Other point is thinking about how to get other objects
        #       need to execute the claim translation

        #self.isolateTextPointed(claim)
        self.claim_translated = ''


        if tagComm in ["IndexTooBig","IndexNegative"]:

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
                if list_tmp_cl[tmpIndex] != "[":
                    self.tag_index_array += list_tmp_cl[tmpIndex]
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
                    self.tag_name_array += list_tmp_cl[tmpIndex]
                if countFlag > 2:
                    tmpIndex = -1

                tmpIndex -= 1

            strIsolaCl = isolateStrVarArr+isolateStrIndex
            #print("======> %s" % strIsolaCl)

            # Apply the correct transformation rule
            if tagComm == 'IndexTooBig':
                self.claim_translated = self.tag_index_array+" <= "+self.tag_name_array+".length"
            elif tagComm == 'IndexNegative':
                self.claim_translated = self.tag_index_array+" >= 0"


        elif tagComm == 'Null':

            # Avoid System.out
            matchSysOut = re.search(r'System\.out', claim)

            if not matchSysOut:

                list_tmp_cl = list(claim)

                # get the name var
                tmpIndex = indexPointed

                # Identify the type of NULL DEREFENCE
                # Is a array -> ex: array.length
                if list_tmp_cl[tmpIndex] == '.' or list_tmp_cl[tmpIndex] == '[':
                    tmpIndex -= 1
                    while tmpIndex >= 0 and not list_tmp_cl[tmpIndex] in ['(',')',';','=',' ']:
                        self.claim_translated += list_tmp_cl[tmpIndex]
                        tmpIndex -= 1
                    self.claim_translated = self.claim_translated[::-1]
                    self.claim_translated += " != NULL && "+self.claim_translated+".length() > 0"

            else:
                self.claim_translated = 1

        elif tagComm == 'ZeroDiv':
            list_tmp_cl = list(claim)
            # get the name var
            tmpIndex = indexPointed
            if list_tmp_cl[tmpIndex] == '/':
                tmpIndex += 1
                while tmpIndex < len(list_tmp_cl) and not list_tmp_cl[tmpIndex] in [';']:
                    self.claim_translated += list_tmp_cl[tmpIndex]
                    tmpIndex += 1
                self.claim_translated += " > 0"
                
                
        elif tagComm == 'ArrayStore':
            # We consider the assignment, e.g., s[0] = o
            text = claim.strip()
            assignment = text.split("=")
            if not len(assignment) == 0:
                # Get only var name for rvalue
                rvalue = self.getOnlyVarName(assignment[0].strip())
                # Get only var name for lvalue
                lvalue = self.getOnlyVarName(assignment[1].strip())
                txt = str(rvalue)+".getClass().getName() == "+str(lvalue)+".getClass().getName()"
                self.claim_translated = txt
                
        
        elif tagComm == 'Assert':
            # We consider the annotations, e.g.,  //@ assert i >= 0
            matchAssert = re.search(r'assert[ ]*(.*)', claim)
            if matchAssert:    
                self.claim_translated = matchAssert.group(1)
                
                
        elif tagComm == 'Reachable':
            self.claim_translated = "(0)"
            
            
        elif tagComm == 'Invariant':
            # Suport only to comparation
            # [TODO] WARNNING: fix untracked line
            matchInvariant = re.search(r'invariant[ ]*(.*)', annoted)
            if matchInvariant:
                self.claim_translated = matchInvariant.group(1)
            
            
        elif tagComm == 'Cast':
            #There are two types of object typecasting:
            #1. upcasting 
            #2. downcasting
            
            # Checking if a class if converted in a subclass downcasting possible BUG
            # if (view instanceof B)
            # boolean isInstance = someObject instanceof SomeTypeOrInterface;
            # Example:
            # assertTrue(Arrays.asList("a", "b", "c") instanceof List<?>);
            
            list_tmp_cl = list(claim)            
            tmpIndex = indexPointed
            
            # Getting the text to isolate the parts
            text=''
            if list_tmp_cl[tmpIndex] == '(':                
                while tmpIndex < len(list_tmp_cl) and not list_tmp_cl[tmpIndex] in [';']:
                    text += list_tmp_cl[tmpIndex]
                    tmpIndex += 1
            
            # Isolating the parts
            matchCast = re.search(r'\(([a-zA-Z0-9\_]*)\)*[ ]*([a-zA-Z0-9\_\[\]]*)', text)
            if matchCast:
                self.claim_translated += "( "+matchCast.group(2)+" instanceof "+matchCast.group(1)+" )"
                #print(matchCast.group(2))
                
            #.getClass().getSimpleName()
            
            
        elif tagComm == 'NonNull':
            text = claim.strip()
            assignment = text.split("=")
            self.claim_translated = "!("
            if not len(assignment) == 0:
                self.claim_translated += assignment[0].strip()+" == "+assignment[1].strip()+" )"
            
            
        elif tagComm == 'NegSize':
            list_tmp_cl = list(claim)            
            tmpIndex = indexPointed
            if list_tmp_cl[tmpIndex] == '[':
                tmpIndex += 1
                self.claim_translated = "!("
                while tmpIndex < len(list_tmp_cl) and not list_tmp_cl[tmpIndex] in [']']:
                    self.claim_translated += list_tmp_cl[tmpIndex]
                    tmpIndex += 1
                self.claim_translated += " < 0 )"
            else:
                self.claim_translated = "!("
                while tmpIndex < len(list_tmp_cl) and not list_tmp_cl[tmpIndex] in [';']:
                    self.claim_translated += list_tmp_cl[tmpIndex]
                    tmpIndex += 1
                self.claim_translated += " < 0 )"
                
                
                
                
        elif tagComm == 'Pre':
            
            # WARNNING for while we just consider @requires
            # Basead on this model -> @ requires i >= 0;
            
            tmpIndex = indexPointed
            list_tmp_cl = list(claim)
            # Pre conditions for methods call, e.g., int j = m(-1);
            # in this case we just get input args for the methods
            # >> First we get only the input args
            tmpIndex += 1
            tmp_str = ''
            while tmpIndex < len(list_tmp_cl) and not list_tmp_cl[tmpIndex] in [')',';']:
                tmp_str += list_tmp_cl[tmpIndex]
                tmpIndex += 1
            
            # >> Now getting the annoted code if has any            
            matchRequires = re.search(r'requires[ ]*[a-zA-Z0-9\_\[\]\(\)][ ]*(.*)', annoted)
            if matchRequires:
                # Now create the assert
                #print(matchRequires.group(1))
                tmp_str += " "+str(matchRequires.group(1).rstrip('\n'))
                self.claim_translated = tmp_str
                            
                        
            
            
        elif tagComm == 'Post':            
            # WARNNING for while we just consider @requires
            # Basead on this model -> //@ ensures \result > 0;
            # where \result is replaced by the return of the function
            
            # Checking if ESC/Java points to end of the method
            tmpIndex = indexPointed
            list_tmp_cl = list(claim)
            tmp_str = ''
            if list_tmp_cl[tmpIndex] == '}':
                # Get the scope of the program
                # the identification is done by the range by num line from the claim
                save_id_range_sc = self.whatIsTheScope(lineNumber)
                save_return = self.getValueFromReturn(save_id_range_sc)
                
                if not save_return == None:                
                    tmp_str = str(save_return)
                    
                    # Getting data from annoted code
                    matchEnsures = re.search(r'ensures[ ]*\\result[ ]*(.*)', annoted)
                    if matchEnsures:
                        #print(matchEnsures.group(1))
                        tmp_str += " "+str(matchEnsures.group(1))
                        self.claim_translated = tmp_str
                
            


        self.reset_var_claims()
        if self.claim_translated:
            return self.claim_translated
        else:
            return 1
            
            
    def getOnlyVarName(self, var):
        #print(var)
        matchVar = re.search(r'([a-zA-Z0-9\_]*).*', var)
        if matchVar:
            return matchVar.group(1)

    
    def getValueFromReturn(self, indexList):
        cprogram = open(self.pathJavaFile, "r")
        lines_from_program = cprogram.readlines()
        cprogram.close()
        
        tmp_count = int(self.list_num_start_func[indexList])
        while tmp_count <= int(self.list_num_end_func[indexList]):
            matchReturn = re.search(r'return[ ]*(.[^;]*)', lines_from_program[(tmp_count-1)])
            if matchReturn:
                #print(matchReturn.group(1))
                return matchReturn.group(1)
            
            tmp_count += 1

    
    def whatIsTheScope(self, lineNum):
        for index,startLine in enumerate(self.list_num_start_func):
            if self.list_num_end_func[index] <= lineNum and lineNum >= startLine:                
                return index
            
    
    
    def generateScopeByLineNumber(self, cfile):
        #print()
        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        cprogram = open(cfile, "r")
        lines_from_program = cprogram.readlines()
        cprogram.close()
        
        # Gettting the name of the functions
        get_start_data_method = commands.getoutput("ctags --sort=NO -x --c-kinds=f "+cfile).split("\n")
        for line in get_start_data_method:
            #print(line)
            matchDataMethod = re.search(r'([a-zA-Z0-9\_\(\)\[\]]*)[ ]*([a-zA-Z0-9]*)[ ]*([0-9]*)', line)
            if matchDataMethod:
                if not matchDataMethod.group(2) == "class":
                    #print(matchDataMethod.group(1))   
                    self.list_name_func.append(matchDataMethod.group(1))  
                    #print(">>>>> "+matchDataMethod.group(3))
                    self.list_num_start_func.append(matchDataMethod.group(3))                    
                    # Getting the end num of the line
                    # >> If the method is only a Decl, e.g., public int m(int i);
                    matchDeclMethod = re.search(r';', lines_from_program[int(matchDataMethod.group(3))-1])
                    if not matchDeclMethod:
                        getEndLineFunction = commands.getoutput("awk \'NR > first && /[ ]*}/ { print NR; exit }\' first="+matchDataMethod.group(3)+" "+cfile)
                        self.list_num_end_func.append(getEndLineFunction)
                    else:
                        # Is a decl, therefore the start == end
                        self.list_num_end_func.append(matchDataMethod.group(3))
                    
        
            
           
    
    

    def reset_var_claims(self):
        # Atributes for tags
        self.tag_name_array = ''
        self.tag_index_array = ''









# -------------------------------------------------
# Main python program
# -------------------------------------------------

# if __name__ == "__main__":
#     path_input_file = ""
#     path_c_file     = ""
#
#     if len(sys.argv) >= 2:
#         path_input_file  = sys.argv[1]
#         path_c_file = sys.argv[2]
#     else:
#         print("Incorrect Usage")
#         print("Usage: ./script <csv file> <CFile>")
#         sys.exit()
#
#
#     test = IsolateDataClaim()
#     test.loadDataFromCsv(path_input_file)
#     test.setNameJavaFile(path_c_file)
#     test.generateScopeByLineNumber(path_c_file)
#
#     #test.showDataLoaded()
#     test.getObjectPointed()

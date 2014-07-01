#!/usr/bin/env python
# -*- coding: latin1 -*-

from __future__ import print_function
__author__ = 'Herbert OLiveira Rocha'


#-------------------------------------------------------------------------------------------------
# Goal: This program aims to perfom the translation of the claim gathered from ESC/JAVA.
#       The focus of this program is isolate the variable or structure related in the claim.
#
# Status: [DOING]
#
#-------------------------------------------------------------------------------------------------


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
    related in the claim, and then apply its respective translation.
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
        self.claim_list_translated = [] # the return of the execution of this class
        
        #Data scope function
        self.list_name_func = []
        self.list_num_start_func = []
        self.list_num_end_func = []


        # Flags
        self.DEBUG_STATUS   = False
        self.TESTING_STATUS = False


        # For testing the translation
        self.test_num_total_cl            = 0
        self.test_num_total_failed_translate_cl = 0
        self.test_num_actual_failed_translate_cl = 0
        self.test_num_total_incomplete_trans_cl = 0
        self.test_num_actual_incomplete_trans_cl = 0


        # CSV input
        self.pathCsvFile = ''
        self.columns_csv = defaultdict(list) #we want a list to append each value in each column to


        # Atributes for tags
        self.claim_translated = ''
        self.tag_name_array = ''
        self.tag_index_array = ''


    def set_debug_flag(self):
        self.DEBUG_STATUS = True


    def set_testing_flag(self):
        self.TESTING_STATUS = True



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
        for line,comm,claim,pt_data,tag,annoted,annoted_pt in \
                zip(self.columns_csv['Number of Line'],self.columns_csv['Comments'],
                    self.columns_csv['Claim'],self.columns_csv['Point Data'],self.columns_csv['Tag'],
                    self.columns_csv['Annoted'],self.columns_csv['Annoted Point']):

            if self.TESTING_STATUS:
                self.test_num_total_cl += 1

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
        if not self.DEBUG_STATUS and not self.TESTING_STATUS:
            print("Number of Line ; Original Claim ; Claim Translated ; Comments ")

        # >> Starting translation
        while id < len(self.claim_list_claim):
            
            # Generating a list from the text claim
            list_tmp_cl = list(self.claim_list_claim[id])
            # Getting the index position pointed by identified
            #print(self.claim_list_point_data[id])
            get_index = (len(list(self.claim_list_point_data[id])) - 1)

            if self.DEBUG_STATUS:
                print()
                print(">> Claim translation << ")
                print("From claim   : %s" % self.claim_list_claim[id])
                print("Tag comment  : %s" % self.claim_list_tag_comm[id])
                # DOING: Create a method to select the object and then apply the transformation rule
                #       to the claims
                print("The translation: %s" % self.getObjectInClaim(self.claim_list_line_num[id],
                                                                    self.claim_list_tag_comm[id],
                                                                    self.claim_list_claim[id],
                                                                    self.claim_list_comments[id],
                                                                    get_index,self.claim_list_annoted[id]))
                print()

            # Print the new csv
            else:
                claim_translated = self.getObjectInClaim(self.claim_list_line_num[id],
                                                         self.claim_list_tag_comm[id],
                                                         self.claim_list_claim[id],
                                                         self.claim_list_comments[id],
                                                         get_index,
                                                         self.claim_list_annoted[id])

                row = self.claim_list_line_num[id].strip()+" ; "+\
                      self.claim_list_claim[id].strip()+" ; "+\
                      str(claim_translated)+" ; "+\
                      self.claim_list_comments[id].strip()

                # >>> Print the translation
                if not self.TESTING_STATUS:
                    print(row)

            id += 1

        if self.TESTING_STATUS:
            # Print log TOTAL
            print(self.pathJavaFile+" ; "+str(self.test_num_total_failed_translate_cl)+
                  " ; "+str(self.test_num_total_incomplete_trans_cl)+" ; "+
                  str(self.test_num_total_failed_translate_cl + self.test_num_total_incomplete_trans_cl)+" ; "+
                  str(self.test_num_total_cl - (self.test_num_total_failed_translate_cl +
                                                self.test_num_total_incomplete_trans_cl))+" ; "+
                  str(self.test_num_total_cl))


    def getObjectInClaim(self, lineNumber, tagComm, claim, _commentCl, indexPointed, annoted):
        """
        Method to gather the object pointed in the claim
        """
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
                # Checking parts translated]
                if not self.check_translated_is_empty(self.tag_index_array) and \
                   not self.check_translated_is_empty(self.tag_name_array):
                    self.claim_translated = self.tag_index_array+" <= "+self.tag_name_array+".length"
                else:
                    self.claim_translated = ""
                    self.test_num_total_incomplete_trans_cl += 1

            elif tagComm == 'IndexNegative':
                if not self.check_translated_is_empty(self.tag_index_array):
                    self.claim_translated = self.tag_index_array+" >= 0"
                else:
                    self.claim_translated = ""
                    self.test_num_total_incomplete_trans_cl += 1


        elif tagComm == 'Null':

            # Avoid System.out
            matchSysOut = re.search(r'System\.out', claim)

            if not matchSysOut:

                list_tmp_cl = list(claim)

                # get the name var
                tmpIndex = indexPointed
                #print(tmpIndex, len(list_tmp_cl))
                #print(list_tmp_cl)
                #print(claim)
                #sys.exit()

                # Identify the type of NULL DEREFENCE
                if list_tmp_cl[tmpIndex] == '.' or list_tmp_cl[tmpIndex] == '[':

                    #Checking if is a method return, e.g., Runtime.getRuntime().exec("ls " + file);
                    backOneItem = tmpIndex - 1
                    if list_tmp_cl[backOneItem] == ")":
                        # Isolating rvalue from assignment
                        matchRightAssig = re.search(r'=[ ]*(.[^;]*)', claim)
                        if matchRightAssig:
                            rvalueassi = matchRightAssig.group(1)
                            # Checking if is a exec command
                            matchExecComan = re.search(r'\.exec', rvalueassi)
                            if matchExecComan:
                                #print("JFORTES_CHECK_EXEC_RETURN( "+rvalueassi+" )")
                                self.claim_translated = "JFORTES_CHECK_EXEC_RETURN( "+rvalueassi+" )"
                    else:
                        # We conclude that is a array NULL -> ex: array.length
                        tmpIndex -= 1
                        while tmpIndex >= 0 and not list_tmp_cl[tmpIndex] in ['(',')',';','=',' ']:
                            self.claim_translated += list_tmp_cl[tmpIndex]
                            tmpIndex -= 1

                        self.claim_translated = self.claim_translated[::-1]

                        # Checking parts translated
                        if not self.check_translated_is_empty(self.claim_translated):
                            self.claim_translated += " != NULL && "+self.claim_translated+".length() > 0"
                        else:
                            self.claim_translated = ""
                            self.test_num_total_incomplete_trans_cl += 1

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

                # Checking parts translated
                if not self.check_translated_is_empty(self.claim_translated):
                    self.claim_translated += " > 0"
                else:
                    self.claim_translated = ""
                    self.test_num_total_incomplete_trans_cl += 1
                
                
        elif tagComm == 'ArrayStore':
            # We consider the assignment, e.g., s[0] = o
            text = claim.strip()
            assignment = text.split("=")
            if not len(assignment) == 0:
                # Get only var name for rvalue
                rvalue = self.getOnlyVarName(assignment[0].strip())
                # Get only var name for lvalue
                lvalue = self.getOnlyVarName(assignment[1].strip())

                # Checking parts translated
                if not self.check_translated_is_empty(str(rvalue)) and not self.check_translated_is_empty(str(lvalue)):
                    txt = str(rvalue)+".getClass().getName() == "+str(lvalue)+".getClass().getName()"
                    self.claim_translated = txt
                else:
                    self.claim_translated = ""
                    self.test_num_total_incomplete_trans_cl += 1
                
        
        elif tagComm == 'Assert':
            # We consider the annotations, e.g.,  //@ assert i >= 0
            matchAssert = re.search(r'assert[ ]*(.*)', claim)
            if matchAssert:
                # Checking parts translated
                if not self.check_translated_is_empty(matchAssert.group(1)):
                    self.claim_translated = matchAssert.group(1)
                else:
                    self.claim_translated = ""
                    self.test_num_total_incomplete_trans_cl += 1
                
                
        elif tagComm == 'Reachable':
            self.claim_translated = "(0)"
            
            
        elif tagComm == 'Invariant':
            # Only based on annotations
            if not annoted == "" and not annoted.isspace():
                # Suport only to comparation
                # TODO: WARNNING -> fix untracked line
                matchInvariant = re.search(r'invariant[ ]*(.*)', annoted)
                if matchInvariant:
                    # Checking parts translated
                    if not self.check_translated_is_empty(matchInvariant.group(1)):
                        self.claim_translated = matchInvariant.group(1)
                    else:
                        self.claim_translated = ""
                        self.test_num_total_incomplete_trans_cl += 1


        elif tagComm == 'Constraint':
            # Only based on annotations
            #self.claim_translated=annoted
            if not annoted == "" and not annoted.isspace():
                matchTagAnnot = re.search(r'\\.*', annoted)
                if matchTagAnnot:
                    self.claim_translated = annoted
                else:
                    matchConstraintLit = re.search(r'constraint[ ]*(.*)', annoted)
                    if matchConstraintLit:
                        # Checking parts translated
                        if not self.check_translated_is_empty(matchConstraintLit.group(1)):
                            self.claim_translated = matchConstraintLit.group(1)
                        else:
                            self.claim_translated = ""
                            self.test_num_total_incomplete_trans_cl += 1



            
            
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
                # Checking parts translated
                if not self.check_translated_is_empty(matchCast.group(2)) and \
                    not self.check_translated_is_empty(matchCast.group(1)):
                    self.claim_translated += "( "+matchCast.group(2)+" instanceof "+matchCast.group(1)+" )"

                else:
                    self.claim_translated = ""
                    self.test_num_total_incomplete_trans_cl += 1
                #print(matchCast.group(2))
                
            #.getClass().getSimpleName()
            
            
        elif tagComm == 'NonNull':
            text = claim.strip()
            assignment = text.split("=")
            self.claim_translated = "!("
            if not len(assignment) == 0:
                # Checking parts translated
                if not self.check_translated_is_empty(assignment[0].strip()) and \
                    not self.check_translated_is_empty(assignment[1].strip()):
                    self.claim_translated += assignment[0].strip()+" == "+assignment[1].strip()+" )"
                else:
                    self.claim_translated = ""
                    self.test_num_total_incomplete_trans_cl += 1


        elif tagComm == 'NonNullInit':
            self.claim_translated = "1"
            
            
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

            # Only based on annotations
            if not annoted == "" and not annoted.isspace():
                self.claim_translated = annoted
            # if not annoted == "" and not annoted.isspace():
            #     # WARNNING for while we just consider @requires
            #     # Basead on this model -> @ requires i >= 0;
            #
            #     tmpIndex = indexPointed
            #     list_tmp_cl = list(claim)
            #     # Pre conditions for methods call, e.g., int j = m(-1);
            #     # in this case we just get input args for the methods
            #     # >> First we get only the input args
            #     tmpIndex += 1
            #     tmp_str = ''
            #     while tmpIndex < len(list_tmp_cl) and not list_tmp_cl[tmpIndex] in [')',';']:
            #         tmp_str += list_tmp_cl[tmpIndex]
            #         tmpIndex += 1
            #
            #     # >> Now getting the annoted code if has any
            #     matchRequires = re.search(r'requires[ ]*[a-zA-Z0-9\_\[\]\(\)][ ]*(.*)', annoted)
            #     if matchRequires:
            #         # Now create the assert
            #         #print(matchRequires.group(1))
            #         tmp_str += " "+str(matchRequires.group(1).rstrip('\n'))
            #         # Checking parts translated
            #         if not self.check_translated_is_empty(tmp_str):
            #             self.claim_translated = tmp_str
            #         else:
            #             self.claim_translated = ""
            #             self.test_num_total_incomplete_trans_cl += 1
                            
                        
            
            
        elif tagComm == 'Post':
            # Only based on annotations
            if not annoted == "" and not annoted.isspace():
                #Get only the annotations
                #matchTagAnnot = re.search(r'([/]+[@].*)', annoted)
                #if matchTagAnnot:
                #    self.claim_translated = matchTagAnnot.group(1)
                matchWarNeedPos = re.search(r'(Postcondition possibly not established)', _commentCl)
                if matchWarNeedPos:
                    self.claim_translated = "1"
                else:
                    self.claim_translated = annoted
            # if not annoted == "" and not annoted.isspace():
            #     # WARNNING for while we just consider @requires
            #     # Basead on this model -> //@ ensures \result > 0;
            #     # where \result is replaced by the return of the function
            #
            #     # Checking if ESC/Java points to end of the method
            #     tmpIndex = indexPointed
            #     list_tmp_cl = list(claim)
            #     tmp_str = ''
            #     if list_tmp_cl[tmpIndex] == '}':
            #         # Get the scope of the program
            #         # the identification is done by the range by num line from the claim
            #         save_id_range_sc = self.whatIsTheScope(lineNumber)
            #         save_return = self.getValueFromReturn(save_id_range_sc)
            #
            #         if not save_return == None:
            #             tmp_str = str(save_return)
            #
            #             # Getting data from annoted code
            #             matchEnsures = re.search(r'ensures[ ]*\\result[ ]*(.*)', annoted)
            #             if matchEnsures:
            #                 #print(matchEnsures.group(1))
            #                 tmp_str += " "+str(matchEnsures.group(1))
            #                 if not self.check_translated_is_empty(tmp_str):
            #                     self.claim_translated = tmp_str
            #                 else:
            #                     self.claim_translated = ""
            #                     self.test_num_total_incomplete_trans_cl += 1


        elif tagComm == 'Exception':
            self.claim_translated = "@Test(expected = RuntimeException.class)"
            


        self.reset_var_claims()
        if self.claim_translated:
            return self.claim_translated
        else:
            self.test_num_total_failed_translate_cl += 1
            return 1


    def check_translated_is_empty(self, _string):
        if _string == "" or _string.isspace():
            return True
        else:
            return False

            
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
            #print(self.list_num_end_func[index]+" <= "+lineNum+" and "+lineNum+" >= "+startLine)
            if self.list_num_end_func[index] <= lineNum and lineNum >= startLine:                
                return index

        # We try to check again cuz Pre and Post, in this case we consider a line after and before
        # WARNNING: Need improvements
        for index,startLine in enumerate(self.list_num_start_func):
            #print(self.list_num_end_func[index]+" <= "+lineNum+" and "+lineNum+" >= "+startLine)
            if (int(self.list_num_end_func[index])+1) <= lineNum and lineNum >= (int(startLine)+1):
                return index
        #sys.exit()
            
    
    
    def generateScopeByLineNumber(self, cfile):
        """
        :param cfile: the path of the C program file
        :return void: the method set in the atributes of the class to
                      values related to number line of begin and end of the functions
                      in the analyzed program
        """
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
        """
        This method just reset the values of the following atributes
        """
        # Atributes for tags
        self.tag_name_array = ''
        self.tag_index_array = ''


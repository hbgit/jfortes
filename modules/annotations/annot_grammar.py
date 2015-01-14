#!/usr/bin/env python

from __future__ import print_function
from os import sysconf

"""
Author: Herbert O. Rocha
Email: herberthb12@gmail.com
Year: 2014
Version: 2
"""

from pyparsing import *
import sys
import re
import operator

#Utils
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#following from Python cookbook, #475186
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)

def printout(text, colour=WHITE):
        if has_colours:
                seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
                sys.stdout.write(seq)
        else:
                sys.stdout.write(text)


listannotdata = []

#----------------------------------------------------------
# Parse actions
tmplistdata = []

def savedata(recString):
    conc_str_token=""

    for token in recString:
        conc_str_token += str(token)
    tmplistdata.append(1)
    print(conc_str_token)

#----------------------------------------------------------

########################################################################
#---------------------------------------------------------------
"""
Grammar to JFORTES code annotation
"""

letter                      = Regex(r"([a-zA-Z_]+)")
number                      = Regex(r"([0-9]+)")
value2id                    = Regex(r"([a-zA-Z_0-9]+)")
string                      = OneOrMore(letter + number | letter )
identifyAnnot               = Literal("//@")
#booleano                    = ((Literal("true")) | (Literal("false")))

annotationName              = identifyAnnot + (Keyword("jfortes_constructor").setResultsName('annot_name') |
                                               Keyword("jfortes_method").setResultsName('annot_name') |
                                               Keyword("jfortes_attribute").setResultsName('annot_name'))

attrName                    = Literal("name") + Literal("=") + (string).setResultsName('attrName')
#attrArgs                    = Literal("args") + Literal("=") + Literal("(")+OneOrMore(string | Literal(",") + string | "none").setResultsName('attrArgs')+Literal(")")
attrSequence                = Literal("sequence") + Literal("=") + number.setResultsName('attrSequence')
attrId                      = Literal("id") + Literal("=") + (value2id).setResultsName('attrId')
#attrSequencebyconstructor   = Keyword("sequencebyconstructor") + Literal("=") + number.setResultsName('attrSeqConstr')
#name                        = Literal ("name") + Literal("=") + (string).setResultsName('name')
#typeAttr                    = Literal ("type") + Literal ("=") + (string).setResultsName('typeAttr')
#initialize                  = Literal ("initialize")+ Literal ("=") + (booleano).setResultsName('initialize')
#sequence                    = Literal("sequence") + Literal("=") + number.setResultsName(('sequence'))
#constructor                 = Literal("constructor") + Literal("=") + number.setResultsName(('constructor'))

attrFromConstructors           = Literal("from_constructors") + Literal("=") + Literal("{") + (OneOrMore(value2id | Literal(",") + value2id)).setResultsName('attrFromConstr') + Literal("}")


# TODO: The annotations should be flexible to write the attributes in any place
annotation2Constructor      = annotationName + attrName + Literal(",") + attrId + Literal(",") + attrSequence + Literal(";")

annotation2Method           = annotationName + attrName + Literal(",") + attrFromConstructors + Literal(",") + \
                              attrSequence  + Literal(";")

annotation2Attribute        = annotationName + attrName + Literal(",") + attrFromConstructors + Literal(",") + \
                              attrSequence + Literal(";")

rule                        = annotation2Constructor | annotation2Method | annotation2Attribute
grammar                     = rule

#---------------------------------------------------------------
########################################################################
def hasNoDuplicates (lst):
    return len( lst ) == len( set( lst ) )


# -------------------------------------------------
# Main python program
# -------------------------------------------------
if __name__ == "__main__":
#def main_grammar(_annot_list):
    # CVS file to update
    annot_csv_file = open(sys.argv[1])
    annot_lines_csv = annot_csv_file.readlines()
    #annot_lines_csv = _annot_list
    #print(annot_lines_csv)
    annot_csv_file.close()

    """
    Variables gathing from input csv file
    number line ; class name; annotation
    """
    list_lines_ANNOT = []
    list_nameclass_ANNOT = []
    list_txt_ANNOT = []

    for index, lineClaim in enumerate(annot_lines_csv):

        if index > 0:
            tmp = re.split("\?",lineClaim)

            tmp[0] = tmp[0].replace(" ","")
            tmp[1] = tmp[1].replace("^\s+","")
            tmp[2] = tmp[2].replace("^\s+",
                                    "")

            list_lines_ANNOT.append(tmp[0])
            list_nameclass_ANNOT.append(tmp[1])
            list_txt_ANNOT.append(tmp[2])


    # print the header csv file
    csvheader = 'seq;annot_name;attrName;attrID;attrSequence;attrFromConstructors'
    csvlistbody = []

    lldata = []
    head_dict = {}
    idC = 0

    head_dict['constructors'] = []
    for index, eachannot in enumerate(list_txt_ANNOT):

        # The parse moment
        #print(eachannot)
        try:
            indexList = len(lldata)
            parsed_annot = grammar.parseString( eachannot ).asDict()
            #idC = idC + 1
            #if parsed_annot['annot_name'] == "jfortes_constructor":
            #    constructor = parsed_annot['attrName'] + str(idC)

            listC = []
            #BUG
            if parsed_annot['annot_name'] == "jfortes_constructor":
                listC = [parsed_annot['attrName'], [int(parsed_annot['attrSequence']),indexList]]
                head_dict['constructors'].append(listC)

            else:
                head_dict[parsed_annot['attrName'][0]] = [int(parsed_annot['attrSequence']),indexList]

            # print the context csv file
            #text = parsed_annot.values()
            #print(';'.join(text))

            #print(parsed_annot)

            tmp_list = []
            count_columns = 0
            annotname = ''
            for key, value in parsed_annot.items():
                #print(key, '=>', value)
                if count_columns == 0:
                    annotname = value

                if type(value) == ParseResults:
                    if len(value) > 1:
                        strtemp = ''.join(value)
                        if count_columns == 2 and (annotname == 'jfortes_method' or annotname == 'jfortes_attribute'):
                            tmp_list.append("JFORTES_NONE")
                        tmp_list.append(strtemp)
                    else:
                        if count_columns == 2 and (annotname == 'jfortes_method' or annotname == 'jfortes_attribute'):
                            tmp_list.append("JFORTES_NONE")
                        tmp_list.append(value[0])
                else:
                    if count_columns == 2 and (annotname == 'jfortes_method' or annotname == 'jfortes_attribute'):
                        tmp_list.append("JFORTES_NONE")
                    tmp_list.append(value)

                count_columns += 1


            if annotname == 'jfortes_constructor':
                tmp_list.append("JFORTES_NONE")

            lldata.append(tmp_list)


            # Check if tmp_list == 4. True
            #if len(tmp_list) == 4:
            #    tmp_list.insert(len(tmp_list)+1,"none")

            #print(';'.join(tmp_list))
            #csvlistbody.append(';'.join(tmp_list))

            #printout(str(parsed_annot.asList()), BLUE)
            #print("")
        ##--------------------Improve thi


        except ParseBaseException, pe:
            print()
            print("ERROR. JFORTES syntax is not correct, as shown: ")
            printFLag = 1
            printout(str(pe.msg), RED)
            print("")
            printout(str(pe.pstr), RED)
            print("")
            print(" "*pe.loc+"^")
            sys.exit()

    print(head_dict)
    contConst = 0
    head_dict = sorted(head_dict.items(), key = operator.itemgetter(1))

    n = len(head_dict)
    for i in range(0, n):
        if lldata[i][0] == "jfortes_constructor":
            seq = head_dict['constructors'][contConst][1][0]

            lldata[i].insert(0, str(seq))
            contConst = contConst + 1
        else:
            seq = head_dict[i][1][0]
            lldata[i].insert(0, str(seq))
        if len(lldata[i])!= 0:
            #print (';'.join(lldata[i]))
            csvlistbody.append(';'.join(lldata[i]))
        #lldataindex = lldata[head_dict[i][1][1]]
        #data_csv = str(lldataindex)

    # Print the output in csv format
    # TODO: rewrite this in function of the new structure
    # if not hasNoDuplicates(list_sequence):
    #     print("ERROR. The sequence method are duplicated!")
    #     for line in csvlistbody:
    #         print(line)
    # else:
    #write the parse result
    parseresultfile = open("/tmp/jfortes_parseresult.tmp_j","w")
    parseresultfile.write(csvheader+"\n")
    #print(csvheader)
    for line in csvlistbody:

        parseresultfile.write(str(line)+"\n")
    parseresultfile.close()

    #return "/tmp/jfortes_parseresult.tmp_j"

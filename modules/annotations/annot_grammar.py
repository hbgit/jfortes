#!/usr/bin/env python

from __future__ import print_function
from os import sysconf

"""
Author: Herbert O. Rocha
Email: herberthb12@gmail.com
Year: 2014
Version: 1
"""

from pyparsing import *
import sys
import re

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
string                      = OneOrMore(letter | letter + number)
identifyAnnot               = Literal("//@")
booleano                    = ((Literal("true")) | (Literal("false")))

annotationName              = identifyAnnot + (Keyword("jfortes_getSequenceConstructor").setResultsName('annot_name') |
                                               Keyword("jfortes_getSequenceMethod").setResultsName('annot_name') |
                                               Keyword("jfortes_getAttribute").setResultsName('annot_name'))

attrName                    = Literal("name") + Literal("=") + (string).setResultsName('atrrName')
attrArgs                    = Literal("args") + Literal("=") + Literal("(")+OneOrMore(string | Literal(",") + string | "none").setResultsName('attrArgs')+Literal(")")
attrSequence                = Literal("sequence") + Literal("=") + number.setResultsName('attrSequence')
attrSequencebyconstructor   = Keyword("sequencebyconstructor") + Literal("=") + number.setResultsName('attrSeqConstr')
name                        = Literal ("name") + Literal("=") + (string).setResultsName('name')
typeAttr                    = Literal ("type") + Literal ("=") + (string).setResultsName('typeAttr')
initialize                  = Literal ("initialize")+ Literal ("=") + (booleano).setResultsName('initialize')
sequence                    = Literal("sequence") + Literal("=") + number.setResultsName(('sequence'))
constructor                 = Literal("constructor") + Literal("=") + number.setResultsName(('constructor'))

jGetSequenceConstructor     = annotationName + attrName + Literal(",") + attrArgs + Literal(",") + \
                              attrSequence + Literal(";")

jGetSequenceMethod          = annotationName + attrName + Literal(",") + attrArgs + Literal(",") + \
                              attrSequence + Literal(",") + attrSequencebyconstructor + Literal(";")

jgetAttribute               = annotationName + name + Literal(",") + typeAttr + Literal(",") + \
                              initialize (";")

rule                        = jGetSequenceConstructor | jGetSequenceMethod | jgetAttribute
grammar                     = rule

#---------------------------------------------------------------
########################################################################
def hasNoDuplicates (lst):
    return len( lst ) == len( set( lst ) )


# -------------------------------------------------
# Main python program
# -------------------------------------------------
if __name__ == "__main__":
    # CVS file to update
    list_sequence = []
    annot_csv_file = open(sys.argv[1])
    annot_lines_csv = annot_csv_file.readlines()
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
    csvheader = 'annot_name;atrrName;attrArgs;attrSequence;attrSeqConstr'
    csvlistbody = []

    for index, eachannot in enumerate(list_txt_ANNOT):

        # The parse moment
        #print(eachannot)
        try:
            parsed_annot = grammar.parseString( eachannot ).asDict()

            # print the context csv file
            #text = parsed_annot.values()
            #print(';'.join(text))

           # print(parsed_annot)


            list_sequence.append(parsed_annot['attrSequence'])


            tmp_list = []
            for key, value in parsed_annot.items():
                # print(key, '=>', value)
                if type(value) == ParseResults:
                    if len(value) > 1:
                        strtemp = ''.join(value)
                        tmp_list.append(strtemp)
                    else:
                        tmp_list.append(value[0])
                else:
                    tmp_list.append(value)

            # Check if tmp_list == 4. True
            if len(tmp_list) == 4:
                tmp_list.insert(len(tmp_list)+1,"none")

            #print(';'.join(tmp_list))
            csvlistbody.append(';'.join(tmp_list))

            #printout(str(parsed_annot.asList()), BLUE)
            #print("")
        ##--------------------Improve this
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

    # Print the output in csv format
    if not hasNoDuplicates(list_sequence):
        print("ERROR. The sequence method are duplicated!")
        for line in csvlistbody:
            print(line)
    else:
        for line in csvlistbody:
            print(line)

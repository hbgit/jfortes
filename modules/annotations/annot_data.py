#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-
import  sys
from __builtin__ import dict

__author__ = 'lbentes'

class AnnotData(object):
    def __init__(self, _listOfAnnot, _listOfInput):
        self.listOfAnnot = _listOfAnnot
        self.listOfInput = _listOfInput
        self.indexlist = None
        self.indexlistC = None


    def getdatadifromscopeConstr(self, _scopename):

        #print(self.listOfInput)
        dictInfo = {}
        arglist = []
        typelist = []
        index = 0
        #print("=======")
        if self.indexlistC != None:
            index = self.indexlistC

        while index < (len(self.listOfInput['Scope'])-1):
            scope = self.listOfInput['Scope'][index]
            variablename = self.listOfInput['Variable'][index]
            linenumber = self.listOfInput['Line'][index]

            #print("scope: "+ scope + " _scopename: " + _scopename + " linenumber: "+ linenumber)
            if scope == _scopename:
                # if self.indexlist == None:
                #     index = index_la
                # else:
                #     index = self.indexlist


                arglist.append(variablename)
                typelist.append(self.listOfInput['Type'][index])


                while (self.listOfInput['Line'][index+1]) == (self.listOfInput['Line'][index]):
                    index += 1
                    arglist.append(self.listOfInput['Variable'][index])
                    typelist.append(self.listOfInput['Type'][index])
            # Cuz we just want the actual element from this index, i.e., from the actual scope
                break
            index +=1

        dictInfo['Args'] = arglist
        dictInfo['Type'] = typelist

        self.indexlistC = index + 1
        return dictInfo

    def getdatadifromscopeMethod(self, _scopename):
        dictInfo = {}
        arglist = []
        typelist = []
        index = 0
        tamanho = len(self.listOfInput['Scope'])
        #print("=======")

        while index < (tamanho):
            scope = self.listOfInput['Scope'][index]
            variablename = self.listOfInput['Variable'][index]
            linenumber = self.listOfInput['Line'][index]

            #print("scope: "+ scope + " _scopename: " + _scopename +" _loc: "  + _loc + " linenumber: "+ linenumber)
            if scope == _scopename:
                # if self.indexlist == None:
                #     index = index_la
                # else:
                #     index = self.indexlist


                arglist.append(variablename)
                typelist.append(self.listOfInput['Type'][index])


                if (index < tamanho -1):
                    while (self.listOfInput['Line'][index+1]) == (self.listOfInput['Line'][index]):
                        index += 1
                        arglist.append(self.listOfInput['Variable'][index])
                        typelist.append(self.listOfInput['Type'][index])
            # Cuz we just want the actual element from this index, i.e., from the actual scope
                break
            index +=1

        dictInfo['Args'] = arglist
        dictInfo['Type'] = typelist

        self.indexlist = index + 1
        #print(dictInfo)

        return dictInfo
    def getdatadifromscopeAttributes(self, _scopename, _varname):
        dictInfo = {}
        arglist = []
        typelist = []
        index = 0
        tamanho = len(self.listOfInput['Scope'])
        #print("=======")

        while index < (tamanho):
            scope = self.listOfInput['Scope'][index]
            variablename = self.listOfInput['Variable'][index]
            linenumber = self.listOfInput['Line'][index]

            #print("scope: "+ scope + " _scopename: " + _scopename +" _loc: "  + _loc + " linenumber: "+ linenumber)
            if scope == _scopename and variablename == _varname:
                # if self.indexlist == None:
                #     index = index_la
                # else:
                #     index = self.indexlist


                arglist.append(variablename)
                typelist.append(self.listOfInput['Type'][index])


                if (index < tamanho -1):
                    while (self.listOfInput['Line'][index+1]) == (self.listOfInput['Line'][index]):
                        index += 1
                        arglist.append(self.listOfInput['Variable'][index])
                        typelist.append(self.listOfInput['Type'][index])
            # Cuz we just want the actual element from this index, i.e., from the actual scope
                break
            index +=1

        dictInfo['Args'] = arglist
        dictInfo['Type'] = typelist

        self.indexlist = index + 1
        #print(dictInfo)

        return dictInfo


    def print_annot(self):
        list_all = []

        for index_la, item in enumerate (self.listOfAnnot['annot_name']):
            lista = []
            dict_listofargs = []
            dict_resultattr = {'Args': [], 'Type': []}

            # get data from data_input
            if item == "jfortes_constructor":
                actualname = self.listOfAnnot['attrName'][index_la]
                # print(">>>>>>>>>>", actualname, self.listOfAnnot['attrName'][index_la])
                dict_listofargs = self.getdatadifromscopeConstr(actualname)
            elif item == "jfortes_method":
                actualname = self.listOfAnnot['attrName'][index_la]
                line = self.listOfAnnot['attrLoc'][index_la]
                dict_listofargs = self.getdatadifromscopeMethod(actualname)
            else:
                actualname = self.listOfAnnot['attrName'][index_la]
                dict_listofargs = self.getdatadifromscopeAttributes('class', actualname)

            #
            lista.append(item)
            lista.append(actualname)
            lista.append(dict_listofargs)
            list_all.append(lista)

        # print("")
        # for item in list_all:
        #     print(item)
        return list_all


    def getAttributes(self):
        #print(self.listOfInput)

        dict_resultattr = {'Args': [], 'Type': []}
        self.indexlist = None

        #print("====", self.listOfAnnot['annot_name'])

        for index_la, annotname in enumerate(self.listOfAnnot['annot_name']):
            if annotname == "jfortes_attribute":
                #print(annotname)
                #actualname = 'class'
                # adding elements from dict in the dict result from method self.getdatadifromscope
                # the for is needed cuz each element from dict returned by self.getdatadifromscope
                # is a list
                dict_listofargs = self.getdatadifromscope('class', self.listOfAnnot['attrName'][index_la])
                dict_listoftypes = self.getdatadifromscope('class', self.listOfAnnot['attrName'][index_la])


                for item_arg_type in dict_listofargs['Args']:
                    dict_resultattr['Args'].append(item_arg_type)
                for item_arg_type in dict_listoftypes['Type']:
                    dict_resultattr['Type'].append(item_arg_type)

        # print for DEBUG
        print(dict_resultattr)


    def getMethods(self):
        self.indexlist = None
        print(self.listOfInput['Scope'])
        for index_la, annotname in enumerate(self.listOfAnnot['annot_name']):
            if annotname == "jfortes_method":
                actualname = self.listOfAnnot['attrName'][index_la]
                print(actualname)
                self.getdatadifromscope(actualname)

    #
    # def getMethods(self):
    #     allmethods = []
    #     cont = -1
    #     for i in self.typeAnnot:
    #         method = []
    #         cont += 1
    #         if i == "jfortes_method":
    #             method.append(self.name[cont])
    #             method.append(self.seq[cont])
    #             method.append(self.arg[cont])
    #             allmethods.append(method)
    #     return allmethods


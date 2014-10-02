#!/usr/bin/env python
from __future__ import print_function
# -*- coding: latin1 -*-


__author__ = 'Herbert OLiveira Rocha'

# From Python
import sys
import re
import commands
import shutil
import os



# -------------------------------------------------
# Main program
# -------------------------------------------------
if __name__ == "__main__":
    print("Generating JFORTES documentation ...")

    abspath = os.path.dirname(os.path.abspath(__file__))

    # Removing old api doc
    dirpathapidoc = abspath+"/docs/api_doc"
    if os.path.exists(dirpathapidoc):
        shutil.rmtree(dirpathapidoc)
        os.makedirs(dirpathapidoc)
    else:
        os.makedirs(dirpathapidoc)

    # Generating api-doc
    os.system("sphinx-apidoc -F -o "+dirpathapidoc+" "+abspath)

    # Generating all docs about jfortes
    pathdocs = abspath+"/docs/"
    cwd = os.getcwd()


    #cd dir
    os.chdir(pathdocs)
    os.system("make html")
    #Backing to original path
    os.chdir(cwd)

    print("")
    print("")
    print("---------------------------------------------------------")
    print("JFORTES documentation was generated in: "+(abspath+"docs/_build/html/index.html"))




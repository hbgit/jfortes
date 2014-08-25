#!/usr/bin/env python
# -*- coding: latin1 -*-

from __future__ import print_function
import commands
import re
import subprocess
import sys
import os
import ConfigParser

VERSION = 'v1'

# -------------------------------------------------
# Main python program
# -------------------------------------------------

if __name__ == "__main__":
        
    print()
    print("Checking prerequisites for installing the JFORTES ... ")
    print()
    
    count_status_requisites = 0

    #-------------------------------------------------------
    ### Java version == 1.5
    get_java_version = ''
    get_java_path = ''

    get_java_version = commands.getoutput("java -version")
    matchversion = re.search(r'\"(.*)\"', get_java_version)
    if matchversion:
        if matchversion.group(1)[:3] == "1.5":
            get_java_version = True
            get_java_path = commands.getoutput("which java")
        else:
            print("--------------------------- WARNNING: ", end="")
            print("JAVA 1.5 not found")
            print("  >> Please install JAVA 1.5")
            print("  >> In case you already have the JAVA 1.5 installed, \n"
                  "     please manually set the JAVA path in the [JAVA_path] of the { settings.cfg } file")
            sys.exit()


     #-------------------------------------------------------
    ### Checking ESCJ
    try:
        # pipe output to /dev/null for silence
        null = open("/dev/null", "w")
        subprocess.Popen("escj", stdout=null, stderr=null)
        null.close()
    except OSError:
        print("--------------------------- ERROR: ", end="")
        print("ESCJ not found")
        print("  >> Please install ESC/JAVA")
        print("  >> Available at http://kindsoftware.com/products/opensource/ESCJava2/")


    #-------------------------------------------------------
    ### Checking Ctags
    try:
        # pipe output to /dev/null for silence
        null = open("/dev/null", "w")
        subprocess.Popen("ctags", stdout=null, stderr=null)
        null.close()
        count_status_requisites += 1
    except OSError:
        print("--------------------------- ERROR: ", end="")
        print("Ctags not found")
        print("  >> Please install Ctags")


    
    # Write CFG file
    #Start to generate the config file
    config = ConfigParser.RawConfigParser()
    
    config.add_section('MAPJFORTES_TOOL')
    config.set('MAPJFORTES_TOOL', 'MAPJFORTES_path', os.path.dirname(__file__))
    config.set('MAPJFORTES_TOOL', 'esc_java', 'installed')
    config.set('MAPJFORTES_TOOL', 'ctags', 'installed')
      
    
    config.add_section('JAVA')
    if get_java_path == '':
        config.set('JAVA', 'JAVA_path', 'empty')
    else:
        config.set('JAVA', 'JAVA_path', get_java_path)
        
    
    # Writing our configuration file to 'example.cfg'
    with open('settings.cfg', 'wb') as configfile:
        config.write(configfile)
        
    print("JFORTES installed ")
    print("Futher details: ./jfortes -h")
    print()
    
    
    

#!/usr/bin/python3
# coding=utf-8
'''
Created on 2012-1-5

@author: hbprotoss
'''

import platform, os
import urllib
import http.client
import xml.etree.ElementTree as ET

def GetExplanations(directory, word, conn):
    word = urllib.parse.quote(word.encode("utf8"))
    
    szURL = "/openapi.do?keyfrom=digimon&key=1660474757&type=data&doctype=xml&version=1.1&q=" + word
    conn.request("GET", szURL)
    explanationFile = word + ".xml"
    file = open(explanationFile, "wb")
    file.write(conn.getresponse().read())
    file.close()
    conn.close()
    
    return ET.parse(explanationFile).getroot()

def PrintPhonetic(basic):
    phonetic = basic.find("phonetic")
    if(phonetic != None):
        try:
            print("/" + phonetic.text + "/")
        except UnicodeEncodeError:
            # Not supported by Microsoft Windows default console
            return
        except Exception:
            print("Cannot print phonetic. Unknown error occurred!")


def PrintBasic(explains):
    try:
        exs = explains.findall("ex")
        for ex in exs:
            print(ex.text)
    except Exception:
        return
        
def PrintWeb(web):
    if(web == None):
        print("No translation found! Please retry :(")
        return
    
    explains = web.findall("explain")
    
    try:
        for explain in explains:
            print("> " + explain.find("key").text)
            exs = explain.find("value").findall("ex")
            for ex in exs:
                print("  " + ex.text)
    except Exception:
        return
        
def PrintSeparator():
    print("----------------------------------------------------") 

def Clear():
    os.system(cmd_clear_screen)
    os.system(cmd_del)

def Usage():
    print("pythonDict v1.2(Powered by youdao.com)")
    print("Author: hbprotoss(hbprotoss@qq.com)")
    print("Supported translation:")
    print("English -> Chinese")
    print("Chinese -> English")
    print("enjoy ;-)", "\n")

def MakeDirectory():
    if(not os.path.exists(directory)):
        os.system(cmd_mkdir)                # If directory does not exist, create it
        os.chdir(directory)
    else:
        os.chdir(directory)
        os.system(cmd_del)                  # If directory exists, clear all files in it

def InitGlobal():
    global system
    global directory
    global cmd_mkdir
    global cmd_del
    global cmd_clear_screen

    system = platform.system()
    if(system == "Linux" or system == "Darwin"):
        directory = "/tmp/pythonDict"
        cmd_mkdir = "mkdir %s" % directory
        cmd_del = "rm ./* -f"
        cmd_clear_screen = "clear"
    elif(system == "Windows"):
        directory = os.environ.get("TEMP") + "\\pythonDict"
        cmd_mkdir = "mkdir %s" % directory
        cmd_del = "del * /q"
        cmd_clear_screen = "cls"
    else:
        cmd_clear_screen = "echo " + "Not supported operating system. Please clear the screen manually if you wish :("

###################################################################
# Entry point

# Global variant for cross-platform
system = str()                      # System name
directory = str()                   # Directory to store temporary explanation files
cmd_mkdir = str()                   # Command for making the directory
cmd_del = str()                     # Command for clearing the directory
cmd_clear_screen = str()            # Command for clearing the screen
# End global variant
InitGlobal()

Usage()
directory = MakeDirectory()
conn = http.client.HTTPConnection("fanyi.youdao.com")
Continue = 'y'
while(Continue != 'N' and Continue != 'n'): 
    word = input("Please input the word you want to look up:")

    root = GetExplanations(directory, word, conn)

    more = ''
    basic = root.find("basic")
    if(basic != None):
        # Basic explanations
        PrintSeparator()
        PrintPhonetic(basic)
        PrintBasic(basic.find("explains"))
        PrintSeparator()

        more = input("Need more web explanations?(y/N)")
        print("")
        # More web explanations
        if(more == 'y' or more == 'Y'):
            PrintWeb(root.find("web"))
            PrintSeparator() 
    else:
        print("We are sorry, but only web explanations avaliable:")
        PrintSeparator()
        PrintWeb(root.find("web"))
        PrintSeparator()

    if(basic != None and more != 'y' and more != 'Y'):
        Continue = 'y'
    else:
        Continue = input("Continue looking up another word?(Y/n)")   

    # Clear the screen and temprary explanation file
    Clear()
else:
    print("Thank you for using pythonDict.")
    print("Contact me at hbprotoss@qq.com if you have any problems or bugs to report :)")
    tmp = input("\nPress any key to continue...")

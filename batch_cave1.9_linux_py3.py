import pdb
from tkinter import *
from tkinter.filedialog import askopenfilename
#import os, subprocess, re, htmlentitydefs, inspect, sys, MARC_lang, platform
import os, html.parser, sys, MARC_lang, platform
from time import sleep, strftime
from utilities import utilityFunctions

def BrowseFiles():#open file explorer
    root=Tk()
    root.withdraw()
    filenameOUT = askopenfilename(filetypes=[("MARC files","*.mrc"),("XML files","*.xml"),("All the files","*.*")], title="R.L.W.G Batch Edit -- select input file")
    print(type(filenameOUT))
    filename = filenameOUT
    root.destroy()
    print('\n\nSelected file: \"' + re.sub('.*/(.*?)$', '\\1\"', filename) )

    return filename

class batchEdits:

    def ER_EAI_2nd(self, x, name='ER-EAI-2ND'):
        print('\nRunning change script '+ name + '\n')
        #print(filename)
        x = utilities.MarcEditBreakFile(filename)
        # Change =001 field to =002, and add 003
        x = re.sub('(?m)^=001  (.*)', '=002  \\1\n=003  ER-EAI-2nd', x)
        # ADD local 730, 949 before supplied 008
        x = re.sub('(?m)^=008', r'=949  \\\\$a*b3=z;bn=buint;\n=949  \\1$luint$rs$t99\n=730  0\$aEarly American imprints (Online).$nSecond series,$pShaw-Shoemaker.$5OCU\n=506  \\$aAccess restricted to users at subscribing institutions\n=008', x)
        x = utilities.DeleteLocGov(x)
        x = utilities.Standardize856_956(x)
        x = utilities.CharRefTrans(x)
        x = utilities.MarcEditSaveToMRK(x, filename)
        x = utilities.MarcEditMakeFile(x, filename)
        return x

    def ER_EAI_1st(self, x, name='ER-EAI-1st'):
        print('\nRunning change script '+ name + '\n')
        #print(filename)
        x = utilities.MarcEditBreakFile(filename)
        # Change =001 field to =002, and add 003
        x = re.sub('(?m)^=001  (.*)', '=002  \\1\n=003  ER-EAI-1st', x)
        # ADD local 730, 949 before supplied 008
        x = re.sub('(?m)^=008', r'=949  \\\\$a*b3=z;bn=buint;\n=949  \\1$luint$rs$t99\n=730  0\$aEarly American imprints (Online).$nFirst series,$pEvans.$5OCU\n=506  \\\\$aAccess restricted to users at subscribing institutions\n=008', x)
        x = utilities.DeleteLocGov(x)
        x = utilities.Standardize856_956(x,'Readex')
        x = utilities.CharRefTrans(x)
        x = utilities.MarcEditSaveToMRK(x, filename)
        x = utilities.MarcEditMakeFile(x, filename)
        return x

    def ER_OECD(self, x, name='ER-OECD'):
        print('\nRunning change script '+ name + '\n')
        #translate xml to MARC and break file
        x = utilities.MarcEditXmlToMarc(x)
        x = utilities.MarcEditBreakFile(x)
        def ER_OECD_iLibrary_Bks_NO300(x):
            # Change =001 field to =002, and add 003
            x = re.sub('(?m)^=001  (.*)', '=002  oecd_\\1\n=003  ER-OECD-iLibrary-Bks', x)
            # ADD local 730, 949 before supplied 008
            x = re.sub('(?m)^=008', r'=949  \\\$a*b3=z;bn=buint;\n=949  \\1$luint$rs$t99\n=730  0\$aOECD iLibrary.$pBooks.$5OCU\n=300  \\\\$a1 electronic text :$bdigital PDF file\n=506  \\\\$aAccess restricted to users at subscribing institutions\n=008', x)
            # 04-05-10 DELETE  lines
            x = re.sub('(?m)^=024.*\n', '', x)
            x = re.sub('(?m)^=035.*\n', '', x)
            return x
reStart = ''

while reStart == '' or reStart == 'y':
    #Instantiate classes
    BatchEdits = batchEdits()
    utilities = utilityFunctions()

    #browse to input file and open
    filename = BrowseFiles()

    #get filename and strip extension
    filenameNoExt = re.sub('.\w*$', '', filename)

    #create dictionary/menu of all available change scripts
    ChangeScriptsDict = utilities.listChangeScripts(BatchEdits)

    #select change script by index in dictionary
    SelectedProcess = utilities.ScriptSelect(ChangeScriptsDict)
    methodToCall = getattr(BatchEdits, ChangeScriptsDict[int(SelectedProcess)][0])
    result = methodToCall(filename)
    print('\nOutput File...\n\n\t\tEditing finished ')
    reStart = ''
    while reStart != 'y' and reStart != 'n':
        reStart = input('\n\n\nWould you like to run BatchCave again? (y/n)\n\n\n')


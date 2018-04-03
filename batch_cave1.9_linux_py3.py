import pdb
from pymarc import MARCReader, Record, Field
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
        recs = utilities.BreakMARCFile(x)
        for rec in recs:
            # Change =001 field to =002, and add 003
            rec.add_ordered_field(Field(tag = '002',data = rec['001'].value()))
            rec.remove_field(rec.get_fields('001')[0])
            rec.remove_field(rec.get_fields('003')[0])
            rec.add_ordered_field(Field(tag = '003',data = 'ER-EAI-2nd'))
            # ADD local 730, 949 before supplied 008
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a','*b3=z;bn=buint;']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','uint', 'r', 's', 't', '99']))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'], subfields = ['a','Early American imprints (Online).', 'n', 'Second series,', 'p','Shaw-Shoemaker.', '5', 'OCU']))
            rec.remove_field(rec.get_fields('008')[0])
            rec = utilities.DeleteLocGov(rec)
            rec = utilities.Standardize856_956(rec)
            rec = utilities.CharRefTrans(rec)
        rec = utilities.SaveToMRK(recs, filename)
        x = utilities.MakeMARCFile(recs, filename)
        return x


    def ER_EAI_1st(self, x, name='ER-EAI-1st'):
        print('\nRunning change script '+ name + '\n')
        # x = re.sub('(?m)^=001  (.*)', '=002  \\1\n=003  ER-EAI-1st', x)
        #iterate over list of Record objects
        recs = utilities.BreakMARCFile(x)
        for rec in recs:
            # Change =001 field to =002, and add 003
            rec.add_ordered_field(Field(tag = '002',data = rec['001'].value()))
            rec.remove_field(rec.get_fields('001')[0])
            rec.remove_field(rec.get_fields('003')[0])
            rec.add_ordered_field(Field(tag = '003',data = 'ER-EAI-1st'))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a','*b3=z;bn=buint;']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','uint', 'r', 's', 't', '99']))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'],subfields = ['a','Early American imprints (Online).', 'n', 'First series,','p','Evans.', '5', 'OCU']))
            rec.add_ordered_field(Field(tag = '506', indicators = ['\\', ''], subfields = ['a','Access restricted to users at subscribing institutions']))
            rec.remove_field(rec.get_fields('008')[0])
            rec = utilities.DeleteLocGov(rec)
            rec = utilities.Standardize856_956(rec, 'Readex')
            rec = utilities.CharRefTrans(rec)
        rec = utilities.SaveToMRK(recs, filename)
        x = utilities.MakeMARCFile(recs, filename)
        return x

########### TODO: add ER_OECD ################


    def ER_OCLC_WCS_SDebk(self, x, name='ER-OCLC-WCS-SDebk'):
        print('\nRunning change script '+ name + '\n')
        x = utilities.BreakMARCFile(x)
        x = re.sub('(?m)^=003', r'=949  \\1$luint$rs$t99\n=949  \\\\$a*bn=buint;\n=730  0\\$aScienceDirect eBook Series.$5OCU\n=003  ER-OCLC-WCS-SDebk\n=002  OCLC-WCS-SDebk\n=003', x)
        #change 856 to 956
        x = re.sub('(?m)^=856', '=956', x)
        #add colon to 956$3
        x = re.sub('(?m)\$3ScienceDirect', '$3ScienceDirect :', x)
        x = utilities.DeleteLocGov(x)
        x = utilities.Standardize856_956(x)
        x = utilities.CharRefTrans(x)
        x = utilities.SaveToMRK(x, filename)
        x = utilities.MarcEditMakeFile(x, filename)
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


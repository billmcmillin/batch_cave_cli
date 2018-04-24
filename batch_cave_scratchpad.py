from pymarc import MARCReader, Record, Field
from tkinter import *
from tkinter.filedialog import askopenfilename
#import os, subprocess, re, htmlentitydefs, inspect, sys, MARC_lang, platform
import os, html.parser, sys, platform, re
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


#########################################
# Keep everything above this

#batchEdits
##########################################
class batchEdits:

    #### Keep everything from here to next comment ########
    def TEMPLATE_FUNCTION(self, x, name='Function Name'):
        print('\nRunning change script '+ name + '\n')
        recs = utilities.BreakMARCFile(x)
        for rec in recs:
        ##### Keep everything above this comment ########
        ##### Make changes to each record below ########
            # Change =001 field to =002, and add 003
            # rec.add_ordered_field(Field(tag = '002',data = rec['001'].value()))
            # remove 001
            # rec.remove_field(rec.get_fields('001')[0])
            ###### Keep everything below this ########
            rec = utilities.DeleteLocGov(rec)
            rec = utilities.Standardize856_956(rec)
        rec = utilities.SaveToMRK(recs, filename)
        x = utilities.MakeMARCFile(recs, filename)
        return x
        #### Keep everything above this ##########


    def ER_EAI_2nd(self, x, name='ER-EAI-2ND'):
        print('\nRunning change script '+ name + '\n')
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
        rec = utilities.SaveToMRK(recs, filename)
        x = utilities.MakeMARCFile(recs, filename)
        return x



##############################3
#end batchEdits

# Keep everything below here
##############################

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


import pdb
from pymarc import MARCReader, Record, Field
from tkinter import *
from tkinter.filedialog import askopenfilename
#import os, subprocess, re, htmlentitydefs, inspect, sys, MARC_lang, platform
import os, html.parser, sys, MARC_lang, platform, re
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
        recs = utilities.BreakMARCFile(x)
        for rec in recs:
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','uint', 'r', 's', 't', '99']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a','*b3=z;bn=buint;']))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0','\\'],subfields = ['a','ScienceDirect cBook Series.', '5', 'OCU']))
            rec.add_ordered_field(Field(tag = '003',data = 'ER-OCLC-WCS-SDebk'))
            rec.add_ordered_field(Field(tag = '002',data = 'OCLC-WCS-SDebk'))
            #change 856 to 956
            rec.add_ordered_field(Field(tag = '956', data = rec['856'].value()))
            rec.remove_field(rec.get_fields('856')[0])
            #add colon to 956$3
            #x = re.sub('(?m)\$3ScienceDirect', '$3ScienceDirect :', x)
            rec['956']['3'] = re.sub(r'ScienceDirect', 'ScienceDirect :', rec['956']['3'])
            rec = utilities.DeleteLocGov(rec)
            rec = utilities.Standardize856_956(rec, 'Readex')
            rec = utilities.CharRefTrans(rec)
        rec = utilities.SaveToMRK(recs, filename)
        x = utilities.MakeMARCFile(recs, filename)
        return x

##TODO########################################
    def ER_NBER(self, x, name='ER-NBER'):
        print('\nRunning change script '+ name + '\n')
        recs = utilities.BreakMARCFile(x)
        # NBER has begun using two 856 fields. DELETE 856 fields with www.nber.org ... RETAIN 856 fields with dx.doi.org
        for rec in recs:
            #x = re.sub('(?m)^=856.*www.nber.org.*\n', '', x)
            rec.remove_field(rec.get_fields('856')[0])
            #change 001 to 002, retain first letter and insert initial code
            rec.add_ordered_field(Field(tag = '002',data = 'nber_' +rec['001'].value()[:1]))
            #x = re.sub('(?m)^=001  (.*)', '=002  nber \\1', x)
            #x = re.sub('(?m)^=001  ', '=002  nber_', x) 
            #ADD 003, 006, , 533, 730, 949 before supplied 008
            #x = re.sub('(?m)^=008', r'=949  \\1$luint$rs$t99\n=949  \\\\$a*b3=z;bn=buint;\n=830  \\0$aWorking paper series (National Bureau of Economic Research : Online)\n=730  0\\$aNBER working paper series online.$5OCU\n=533  \\\\$aElectronic reproduction.$bCambridge, Mass.$cNational Bureau of Economic Research,$d200-$e1 electronic text : PDF file.$fNBER working paper series.$nAccess restricted to patrons at subscribing institutions\n=007  cr\\mnu\n=006  m\\\\\\\\\\\\\\\\d\\\\\\\\\\\\\\\\\n=003  ER-NBER\n=008', x)
            # 530 field, change Hardcopy to Print
            #x = re.sub('(?m)^(=530.*)Hardcopy(.*)', '\\1Print\\2', x)
            # 490 and 830 fields lack ISBD punctuation, supply where lacking
            #x = re.sub('(?m)^(=490.*)[^ ;](\$v.*)', '\\1 ;\\2', x)
            #x = re.sub('(?m)^(=830.*)[^ ;](\$v.*)', '\\1 ;\\2', x)
            # delete supplied 690 fields
            #x = re.sub('(?m)^=690.*\n', '', x)
            rec = utilities.DeleteLocGov(rec)
            rec = utilities.Standardize856_956(rec, 'NBER')
            rec = utilities.CharRefTrans(rec)
            rec = utilities.AddEresourceGMD(rec)
        rec = utilities.SaveToMRK(recs, filename)
        x = utilities.MakeMARCFile(recs, filename)
        return x

    def ER_OL_Safari(self, x, name='ER-O/L-Safari'):
        print('\nRunning change script '+ name + '\n')
        recs = utilities.BreakMARCFile(x)
        regexes = [
            re.compile(r'.*EBSCOhost.*\n'),
            re.compile(r'.*OhioLINK.*'),
            re.compile(r'.*SpringerLink.*\n'),
            re.compile(r'.*Wiley.*\n'),
        ]

        for rec in recs:
            for field in rec:
                if field.tag == '856':
                    #if any of the 856 fields match any of the above regex patterns, delete the whole field`
                    if any(regex.match(field.value()) for regex in regexes):
                        rec.remove_field(field)
                    #rename any 856$3 from Safari Books Online to Safari (ProQuest) :
                    if field['3'] == 'Safari Books Online':
                        field['3'] = 'Safari (ProQuest) :'
                    #edit proxy URLs
                    old_z = field['z']
                    old_z = re.sub('Connect to resource', 'Connect to resource online', old_z)
                    #old_z = re.sub('\(off-campus access\)', '(Off Campus Access)', old_z)
                    old_z = re.sub('\(off-campus\)', '(Off Campus Access)', old_z)
                    #old_z = re.sub('Connect to this resource online', 'Connect to resource online', old_z)
                    #old_z = re.sub('\(off-campus access\)', '(Off Campus Access)', old_z)
                    #old_z = re.sub('Connect to electronic resource', '$Connect to resource online', old_z)
                    field['z'] = old_z
                    #Change hyperlink tag from 856 to 956
                    #field.tag = '956'
            #Insert 002, 003, 730, 949 before supplied 008
            rec.add_ordered_field(Field(tag = '003',data = 'ER-EAI-1st'))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'],subfields = ['l','olink', 'r', 's', 't', '99']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'],subfields = ['a','*b3=z;bn=bolin;']))
            rec.add_ordered_field(Field(tag = '730', indicators =['0','\\'],subfields = ['a','Safari books online.', '5', 'OCU']))
            #rec.remove_field(rec.get_fields('003')[0])
            rec.add_ordered_field(Field(tag = '003',data = 'ER-O/L-Safari'))
            rec.add_ordered_field(Field(tag = '002',data = 'O/L-Safari'))
            #rec = utilities.Standardize856_956(rec, )
            rec = utilities.AddEresourceGMD(rec)
            rec = utilities.DeleteLocGov(rec)
            rec = utilities.CharRefTrans(rec)
        rec = utilities.SaveToMRK(recs, filename)
        x = utilities.MakeMARCFile(recs, filename)
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


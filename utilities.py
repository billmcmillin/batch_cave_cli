import inspect, re, subprocess
from io import BytesIO, StringIO
from pymarc import Record, Field, MARCReader, MARCWriter, marcxml, TextWriter

class utilityFunctions:

    def listChangeScripts(self, BatchEdits):
        num = 0
        ChangeScriptsDict = {}
        #pdb.set_trace()
        for i in dir(BatchEdits)[:-26]:
            num = num + 1
            ChangeScriptsDict[num] = [i,''.join(inspect.getargspec(getattr(BatchEdits, i))[3])]
        print(ChangeScriptsDict)
        for key in ChangeScriptsDict.keys():
            print(str(key) + ': ' + ChangeScriptsDict[key][0])
        return ChangeScriptsDict

    def ScriptSelect(self, ChangeScriptsDict):#options list
        NumberOfOptions = len(ChangeScriptsDict)
        def ScriptSelectValidate(low, high):
            prompt = '\nSelect number for desired process: '
            while True:
                try:
                    a = int(input(prompt))
                    if low <= a <= high:
                        return a
                    else:
                        print('\nPlease select a number between %d and %d!\a ' % (low, high))
                except ValueError:
                    print('\nPlease select a number between %d and %d!\a ' % (low, high))
            return
        x = ScriptSelectValidate(1, NumberOfOptions)
        verify = input('\nYou have selected:\n\n\t ' + ChangeScriptsDict[x][1] + '\n\nConfirm (y/n): ')
        while verify != 'y':
            while verify != 'y' and verify != 'n':
                verify = input('Please type \'y\' or \'n\'')
            if verify == 'y':
                pass
            else:
                x = ScriptSelectValidate(1, NumberOfOptions)
                verify = input('\nYou have selected:\n\n\t' + str(x) + '. ' + ChangeScriptsDict[x][1] + '\n\nConfirm (y/n): ')
        return x

    def MarcEditXmlToMarc(self, x):
        mrcFileName = re.sub('.xml', '.mrc', x)
        print('\n<Converting from XML to MARC>\n')
        #subprocess.call([MonoBin,MarcEditBin,"-s", x, "-d",mrcFileName,"-xmlmarc","-marc8", "-mxslt","/opt/marcedit/xslt/MARC21XML2Mnemonic_plugin.xsl"])
        marcStr = ''
        with open(x, 'rb') as fh:
            recs = marcxml.parse_xml_to_array(fh)
            for rec in recs:
                marcStr += str(rec)

        return marcStr

    def BreakMARCFileBACKUP(self, x):
        #break the file; output .mrk
        #mrkFileName = re.sub('.mrc', '.mrk', x)
        print("\n<Breaking MARC file>\n")
        #marcedit process
        #subprocess.call([MonoBin,MarcEditBin,"-s", x, "-d", mrkFileName,"-break"])
        with open(x, 'rb') as fh:
            reader = MARCReader(fh)
            x = ''
            for rec in reader:
                x += str(rec) + '\n'
        #marcedit process
        #x = open(mrkFileName).read()
        return x


    def BreakMARCFile(self, x):
        #break the file into a list of Record objects;
        #mrkFileName = re.sub('.mrc', '.mrk', x)
        print("\n<Breaking MARC file>\n")
        records = []
        with open(x, 'rb') as fh:
            reader = MARCReader(fh)
            for rec in reader:
                records.append(rec)
        return records

    def DeleteLocGov(self, rec):
        regexes = [
            re.compile(r'.*www.loc.gov.*\n'),
            re.compile(r'.*www.e-streams.com.*\n'),
            re.compile(r'.*Book review (E-STREAMS).*\n'),
            re.compile(r'.*catdir.loc.gov.*\n'),
            re.compile(r'.*books.google.com.*\n'),
            re.compile(r'.*cover image.*\n'),
            re.compile(r'.*http://d-nb.info.*\n'),
            re.compile(r'.*http://deposit.d-nb.de/cgi-bin.*\n'),
        ]
        #if an 856 field is present, check it against the above patterns.
        # if found, delete the field
        if rec['856'] is not None:
            url = rec['856']['u']
            if any(regex.match(url) for regex in regexes):
                rec.remove_field(rec.get_fields('856')[0])
        return rec

    def CleanURL(self,url):
        #delete all occurrences of $2
        url.delete_subfield('2')
        #delete all $z
        url.delete_subfield('z')
        #add standard $z
        url.add_subfield('z', 'Connect to resource online')
        #delete all $q
        url.delete_subfield('q')
        #delete all $y
        url.delete_subfield('y')
        #move leading $3 to EOF
        #
        return url

    def Standardize856_956(self, *args):
        rec = args[0]
        if rec['856'] is not None:
            field856 = rec['856']
            if rec['856'].indicator1 != '4':
                print('Found URL field with unexpected indicator')
            self.CleanURL(field856)
            if len(args) > 1 and type(args[1]) == str:
                rec['856'].add_subfield('3', args[1])

        if rec['956'] is not None:
            field956 = rec['956']
            if rec['956'].indicator1 != '4':
                print('Found URL field with unexpected indicator')
            self.CleanURL(field956)
            if len(args) > 1 and type(args[1]) == str:
                rec['956'].add_subfield('3', args[1])

        return rec

    def AddEresourceGMD(self, rec):
        if rec['245']['h'] is None:
            if rec['245']['b'] is not None:
                rec['245'].delete_subfield('b')
                rec['245'].add_subfield('h', '[electronic resource]')
            elif rec['245']['c'] is not None:
                rec['245'].delete_subfield('c')
                rec['245'].add_subfield('h', '[electronic resource]')
            else:
                rec['245'].add_subfield('h', '[electronic resource]')
        return rec

    # re-order 007 fields in a MARC record
    def order_007(self, rec):
        james_bond = []
        for field in rec:
            if field.tag == '007':
                james_bond.append(field.data)
                if len(james_bond) > 1:
                    rec.remove_fields('007')
                    james_bond.sort()
                    for f in james_bond:
                        rec.add_ordered_field(Field(tag = '007',data = f))
        return rec

    def SaveToMRK(self, recs, filename):
        filenameNoExt = re.sub('.\w*$', '', filename)
        print('\n<Writing file to MRK>\n')
        outfile = filenameNoExt + '_OUT.mrk'
        writer = TextWriter(open(outfile, 'wt'))
        counter = 1
        for record in recs:
            try:
                writer.write(record)
            except:
                record.force_utf8 = True
                try:
                    writer.write(record)
                except Exception as e:
                    print('encoding error in record ' + str(counter) + ': ' + str(e))
            counter += 1
        writer.close()
        return recs


    def MakeMARCFile(self, recs, filename):
        filenameNoExt = re.sub('.\w*$', '', filename)
        mrcFileName = filenameNoExt + '_OUT.mrc'
        print('\n<Compiling file to MARC>\n')
        writer = MARCWriter(open(mrcFileName, "wb"))
        for r in recs:
            try:
                writer.write(r.as_marc())
            except:
                r.force_utf8 = True
                writer.write(r)
        writer.close()
        return recs


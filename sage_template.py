import pymarc
from pymarc import MARCReader, Record, Field, Writer
#utitilites is the set of reusable functions we've developed for batchcave
from utilities import utilityFunctions
# enables calling of utilities
utilities = utilityFunctions()


# Steps:
#1. move 001 to 002
#2. create 003 with 'er-SRMO'
#3. order 007 fields so cr is first
#4. check 245 for delimiter h
#5. standardize 856
#6. add 2 949 fields


#first open our input and output files
outfile = open('srmo_rev.mrc', 'wb')
with open('SAGE_Research_Methods_Books_Reference.mrc', 'rb') as fh:
    #create a reader that pulls data from the mrc file
    reader = MARCReader(fh)
    #create a record counter for error reporting
    recordnum = 1

    #loop through each record
    for record in reader:
        #1. move 001 to 002
        field001 = record['001']
        #put value of 001 in 002
        record.add_ordered_field(Field(tag='002',data = field001.value()))
        record.remove_field(record.get_fields('001')[0])

#2. create 003 with 'er-SRMO'
        record.add_ordered_field(Field(tag = '003',data = 'ER-SRMO'))

#3. order 007 fields so cr is first
        record = utilities.order_007(record)

        print(record)

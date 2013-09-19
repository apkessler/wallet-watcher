#!/usr/bin/python

import sys
import pickle
import csv


if (len(sys.argv) != 2):
    print "usage: analyze.py <inputfile>"
    exit()



try:
    vendorTypes = pickle.load(open("VendorTypes.p","rb"))
except:
    print "VendorTypes.p does not exist - creating file."
    vendorTypes = {}
    pickle.dump(vendorTypes, open("VendorTypes.p", "wb"))
    

moneySpent = {}
types = ['Ignore', 'Living Expenses', 'Food', 'Fun', 'Other']
for ii in range(0,len(types)):
    moneySpent[types[ii]] = 0
    
transactions=[]

with open(sys.argv[1], 'rU') as csvfile:
    content = csv.reader(csvfile, delimiter = ',')
    for data in content:
        if (''.join(data) != ''):
            date = data[0]
            payee = ' '.join(data[2].split())

            try:
                type = vendorTypes[payee]
                print "%s is of type %s." % (payee, type)
            except KeyError:
                for ii in range(0,len(types)):
                    print "[%d]: %s" % (ii, types[ii])
                typeIndex = int(raw_input("What type of vendor is %s? " % payee))
                if (typeIndex):
                    type = types[typeIndex]
                    vendorTypes[payee] = type
                    print "OK, %s is of type %s." % (payee,type)
                else:
                    continue
                    
            amt = -1*float(data[4])
            moneySpent[type] += amt
            transactions.append((type, payee, amt, date))
                
        else:
            pass
   
print moneySpent


fOut = open("%s.out" % sys.argv[1].split('.')[0],'w')

for type in types:
    fOut.write("\n\n %s: $%s\n" % (type.upper(), moneySpent[type]))
    for trans in transactions:
        if (trans[0] == type):
            fOut.write("\t%s\n" % str(trans))
            
fOut.close()

#Write the updated vendor types to file
pickle.dump(vendorTypes, open("VendorTypes.p", "wb"))
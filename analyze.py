#!/usr/bin/python

import sys
import pickle
import csv
from matplotlib import pyplot

types = ['Ignore', 'Gas', 'Rent','Grocery', 'Living', 'Food', 'Cats','Fun', 'Other']

def askForType(payee):
    
    print "What type of vendor is %s? " % payee
    for ii in range(0,len(types)):
        print "\t[%d]: %s" % (ii, types[ii])
    try:
        typeIndex = int(raw_input(">> "))
        type = types[typeIndex]
        return type
    except IndexError:
        print "Bad input."
        return askForType(payee)
    except ValueError:
        print "Bad input."
        return askForType(payee)
        

def isLineBlank(line):
    return (''.join(line) == '')


def main(vargs):

    if (len(vargs) == 2):
        try:
            csvfile =  open(vargs[1], 'rU')
        except IOError as err:
            print err
            exit()
        content = csv.reader(csvfile, delimiter = ',')
    else:
        print "usage: analyze.py <inputfile.csv>"
        exit()


    #Attempt to load vendor type mapping file.
    try:
        vendorTypes = pickle.load(open("VendorTypes.p","rb"))
    except:
        print "VendorTypes.p does not exist - creating file."
        vendorTypes = {}
        pickle.dump(vendorTypes, open("VendorTypes.p", "wb"))
    

    #Initialize the moneySpent dictionary 
    moneySpent = {}
    for ii in range(1,len(types)):
        moneySpent[types[ii]] = 0
    
    #this will be a list of all transactions so we can write them to a file later    
    transactions=[]


    for data in content:
        if (isLineBlank(data)):
            pass #just skip a blank line
        else:
            date = data[0]
            payee = ' '.join(data[2].split())

            try:
                type = vendorTypes[payee]
                print "%s is of type %s." % (payee, type)
            except KeyError:
                type = askForType(payee)
                vendorTypes[payee] = type
                print "OK, %s is of type %s." % (payee,type)

            if (type != 'Ignore'):
                amt = -1*float(data[4])
                moneySpent[type] += amt
                transactions.append((type, payee, amt, date))
 
    print "Done parsing!"
    print "SUMMARY".center(50,'-')
    for tp,am in moneySpent.iteritems():
        print "%s$%s" % (tp.ljust(10,'.'), am)
    print "-"*50

    
    with open("%s_out.csv" % vargs[1].split('.')[0], 'w') as fOut:
        writer = csv.writer(fOut)

        for ii in range(1,len(types)):
            type = types[ii]
            writer.writerow([type.upper(), moneySpent[type]])
          
        writer.writerow([])
        for type in types:  
            for trans in transactions:
                if (trans[0] == type):
                    writer.writerow(trans)
            
            

    #Write the updated vendor types to file
    print "Writing new pickle file..."
    pickle.dump(vendorTypes, open("VendorTypes.p", "wb"))
    print "Done!"
    
    tps, ams = moneySpent.keys(), moneySpent.values()
    pyplot.pie(ams, labels = tps, autopct='%1.1f%%')
    pyplot.show()
    
    
if __name__ == "__main__":
    main(sys.argv)
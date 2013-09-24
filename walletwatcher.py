#!/usr/bin/python

import sys
import pickle
import csv
from matplotlib import pyplot
from optparse import OptionParser

types = ['Ignore', 'Gas', 'Rent','Grocery', 'Living', 'Food', 'Cats','Fun', 'Other']


def addMask(theMask):
    '''
        Add a vendor mask string to the list of vendor masks.
        
        Args:
            theMask: string -- vendor mask to add
    '''
    
    try:
        masks = pickle.load(open("VendorMasks.p","rb"))
        print "Found a vendor masks file!"
    except:
        print "VendorMasks.p does not exist - starting with a blank file."
        masks = []
        

    masks.append(theMask)    
    pickle.dump(masks, open("VendorMasks.p", "wb"))
    print "Added %s to mask file." % theMask

        
def viewMasks():
    '''
        Print any existing vendor masks.
    '''
    
    try:
        masks = pickle.load(open("VendorMasks.p","rb"))
        print("VENDOR MASKS".center(50, "-"))
        for mask in masks:
            print mask
        print "-"*50
    except:
        print "No masks found."

 



def askForType(payee):
    '''
        Prompt the user for the type of a given payee. If the user gives an invalid input,
        continue prompting.
        
        Args:
            payee: string -- The payee to prompt for the type of.
    
    '''
    
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
    '''
        Return whether or not a line of  a CSV (list of strings) is all empty. 
    '''
    return (''.join(line) == '')


def main():
    
    usage = "usage: %prog [options] inputfile.csv"
    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--pie", action = "store_true", dest = "showPiePlot", 
                default = False, help = "generate a pie graph showing relative spending")
    parser.add_option("-m", "--mask", action = "store_true", dest = "alterMask", 
                default = False, help = "add/view a vendor name mask")
            
    (options, args) = parser.parse_args()

    if (options.alterMask):
        if (len(args) == 1):
            confirm = raw_input("Add '%s' to vendor masks? [Y/n] " % args[0])
            if (confirm == 'Y'):
                addMask(args[0])
            else:
                print "Aborting add to masks."
        elif (len(args) == 0):
            viewMasks()
        else:
            parser.print_help()
        
        exit()
        

    if (len(args) == 1):
        try:
            csvfile =  open(args[0], 'rU')
        except IOError as err:
            print err
            exit()
        content = csv.reader(csvfile, delimiter = ',')
    else:
        parser.print_help()
        exit()

    #Attempt to load vendor type mapping file.
    try:
        vendorTypes = pickle.load(open("VendorTypes.p","rb"))
        print "Found a vendor mapping file!"
    except:
        print "VendorTypes.p does not exist - creating file."
        vendorTypes = {}
        pickle.dump(vendorTypes, open("VendorTypes.p", "wb"))
    
    #Any Payee name that contains one of these strings will be mapped by type to that substring
    #useful for when some payees show up different every time (Movie theatre, iTunes, etc.)
    try:
        masks = pickle.load(open("VendorMasks.p","rb"))
        print "Found a vendor masks file!"
    except:
        print "VendorMasks.p does not exist - creating file."
        masks = []
        pickle.dump(masks, open("VendorMasks.p", "wb"))

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
            
            payeeLookup = payee
            
            for mask in masks:
                if (payee.find(mask, 0, len(payee)) >= 0):
                    payeeLookup = mask
                    print "Found mask: %s!" % mask
                    break
            
            
            try:
                type = vendorTypes[payeeLookup]
                print "%s%s" % (payee.title().ljust(45,"."), type)
            except KeyError:
                type = askForType(payee)
                vendorTypes[payeeLookup] = type
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

    
    with open("%s_out.csv" % args[0].split('.')[0], 'w') as fOut:
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
    
    if (options.showPiePlot):
        tps, ams = moneySpent.keys(), moneySpent.values()
        pyplot.pie(ams, labels = tps, autopct='%1.1f%%')
        pyplot.show()
    
    
if __name__ == "__main__":
    main()
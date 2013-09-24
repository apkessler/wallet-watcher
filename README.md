#wallet-watcher

##About
Tools for parsing bank account summaries and monitoring spending habits. 
Andrew P. Kessler, 2013


##Usage
This program is designed to take as input CSV files from a bank listing credit card transactions,
and out a file that organizes purchases based on type and/or amount.

###Parsing a credit card record
If you have a file of credit card transactions as `Sept13.csv`, just do:
    
    $ ./walletwatcher.py Sept13.csv

This will create a file `Sept13_out.csv` that contains the parsed data, as well as pickle file
that stores known vendors/type pairs. 

###Generating a pie graph
To display a pie graph of relative spending between categories, use the `-p` flag. For example:
	
	$ ./walletwatcher.py -p Sept13.csv

###Vendor Masks
Some vendors will have a different name show up every time on your credit card statement - for instance, every purchase from iTunes shows up as `APL*ITUNES XYZ`, where *XYZ* is some unique ID. 

Rather than have to enter a vendor type each time an iTunes purchase shows up (since the vendor names will never match), you can set a *vendor mask*.  

For every vendor name on in the input file, *walletwatcher* will see if any names from the Vendor Masks list are contained within it. If so, the vendor type is referenced by this substring. 

For example, if you add`APL*ITUNES` as a vendor mask, a purchases that shows up like `APL*ITUNES 1234567` will all be linked to the same vendor. 

####Adding a vendor mask
Add a venfor mask using the `-m` flag. For example:

	$ ./walletwatcher.py -m "APL*ITUNES"
	
Wrapping the vendor name in quotes is not strictly necessary unless the vendor mask contains spaces. 

####Viewing vendor masks
To see what vendor masks are stored in the `VendorMasks.p` reference file, just call `-m` with no arguments:

	 ./walletwatcher.py -m 	
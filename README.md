#wallet-watcher

Tools for parsing bank account summaries and monitoring spending habits. 
Andrew P. Kessler, 2013


##Usage
This program is designed to take as input CSV files from a bank listing credit card transactions,
and out a file that organizes purchases based on type and/or amount.

If you have a file of credit card transactions as `Sept13.csv`, just do:
    `$ python analyze.py Sept13.csv`

This will create a file `Sept13.out` that contains the parsed data, as well as pickle file
that stores known vendors/type pairs. 


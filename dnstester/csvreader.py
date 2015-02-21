# -*- coding: utf-8 -*-
import csv

def generateDNSDataFromCSV(csvfile):
    """
    :param string inputfile: An iterable object that ....
    """
    csvreader = csv.reader(csvfile, delimiter=',',)
    
    for line in csvreader:
        yield line
    


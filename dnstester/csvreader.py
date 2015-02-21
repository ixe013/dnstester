# -*- coding: utf-8 -*-
import csv
import logging

def generateDNSDataFromCSV(csvfile):
    """
    :param string inputfile: An iterable object that ....
    """
    csvreader = csv.reader(csvfile, delimiter=',',)
    
    for line in csvreader:
        try:
            host,rdtype,value = line
            yield (host.strip('.'), rdtype, value)
        except ValueError:
            logging.error('Malformed line {}'.format(line))

    


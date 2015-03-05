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
            yield (host.lower().strip('.'), rdtype.upper(), value.lower())
            if rdtype == 'A' and not value == 'NXDOMAIN':
                yield (value.lower(), 'PTR', host.lower().strip('.'))
        except ValueError:
            logging.error('Malformed line: ' + str(line))

    


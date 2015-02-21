# -*- coding: utf-8 -*-
try:
    from collections import OrderedDictz
except ImportError:
    from ordereddictbackport import OrderedDict

import csvreader
from pprint import pprint as pp

if __name__ == '__main__':
    import dnsfacade
    from pprint import pprint as pp

    cache = {}
    dnsdata = OrderedDict()

    with open('data.csv') as datafile:
        datafile.readline()
        for host,rtype,value in csvreader.generateDNSDataFromCSV(datafile):
            dnsdata.setdefault(host, {}).setdefault(rtype.upper(), []).append(value)

    #pp(dnsdata)

    #nameservers = dnsfacade.getNameserverForHost('www.google.com')
    nameservers = ['8.8.8.8', '8.8.4.4']

    for nameserver in nameservers:                     
        cache[nameserver] = { 'www.paralint.com' : dnsfacade.getRecordValues('www.paralint.com', nameserver) }

    pp(cache)

    results = []

    #For every DNS records of a single hostname, get all the DNS entries
    for host,entries in dnsdata.items():
        #For every record type, get all the values
        for rdtype,values in entries.items():
            #For each value of the current record type
            for value in values:
                difference_found = False
                #Append a new result line
                results.append( [host, rdtype, value] )
                #For every nameserver we must lookup
                for nameserver in cache:
                    try:
                        #If the value is in the cache
                        if value in cache[nameserver][host][rdtype]:
                            results[-1].append(value)
                        else:
                            difference_found = True
                            #Append the result we found
                            results[-1].append('*'+cache[nameserver][host][rdtype][0])
                    except KeyError:
                        difference_found = True
                        results[-1].append('NXDOMAIN')

                if difference_found:
                   results[-1].append('FAILED')
                else:    
                   results[-1].append('PASS')


    for line in results:
        pp(line)


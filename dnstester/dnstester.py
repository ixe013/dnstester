# -*- coding: utf-8 -*-
try:
    from collections import OrderedDict
except ImportError:
    from ordereddictbackport import OrderedDict

import sys

import csvreader
from pprint import pprint as pp

if __name__ == '__main__':
    import dnsfacade
    import analyze
    import socket

    from pprint import pprint as pp

    cache = {}
    dnsdata = OrderedDict()

    inputfilename = sys.argv[1]

    datafile = open(inputfilename) 
    datafile.readline()
    for host,rtype,value in csvreader.generateDNSDataFromCSV(datafile):
        dnsdata.setdefault(host.strip().strip('.'), {}).setdefault(rtype.upper().strip(), []).append(value.strip())

    datafile.close()

    #pp(dnsdata)

    if '-lookup' in sys.argv:
        #nameservers = dnsfacade.getNameserverForHost('www.google.com')
        nameservers = ['10.64.28.20', '10.68.28.20']

        for nameserver in nameservers:                     
            for entry in dnsdata:
                try:
                    #If this is an IP address
                    socket.inet_aton(entry)
                    cache.setdefault(nameserver, {})[entry] = dnsfacade.reverseLookup(entry, nameserver)
                except socket.error:
                    #Forward lookup
                    values = dnsfacade.getRecordValues(entry, nameserver)
                    cache.setdefault(nameserver, {})[entry] = values 

        #pp(cache)

        headers = analyze.getComparaisonHeaders(dnsdata, nameservers)
        results = analyze.getComparaisonResults(dnsdata, cache)

        print ','.join(headers)

        for line in results:
            print ','.join(line)

    if '-hostfile' in sys.argv:
        results = analyze.getEquivalentHostFile(dnsdata)

        for ip, host in results:
            print ip,host


# -*- coding: utf-8 -*-
try:
    from collections import OrderedDictz
except ImportError:
    from ordereddictbackport import OrderedDict

import csvreader
from pprint import pprint as pp

if __name__ == '__main__':
    import dnsfacade
    import analyze

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

    headers = analyze.getComparaisonHeaders(dnsdata, nameservers)

    for line in results:
        pp(line)


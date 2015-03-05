# -*- coding: utf-8 -*-

def getComparaisonHeaders(dnsdata, cache):
    """Returns the table header that would be output for those nameservers.

    The pattern is this :
    [ 'Host', 'Record type', 'Expected', 'NS1', 'Result for NS1', ..., 'NSn', 'Result for NSn', Overall result']

    So the list will contain 3+2N+1 column, where N is the number of 
    nameservers in the cache.

    :param dict dnsdata: The dnsdata that will be verified (Unused)
    :param dict cache: The dnsdata that will used for verifiation
    :rtype: list
    """
    result = ['Host', 'Record type', 'Expected']
    for nameserver in cache:
        result.append('Nameserver '+nameserver)
        result.append('Result')

    result.append('Overall result')

    return result


def getComparaisonResults(dnsdata, cache):
    results = []

    #For every DNS records of a single hostname, get all the DNS entries
    for host,entries in dnsdata.items():
        #For every record type, get all the values
        for rdtype,values in entries.items():
            #For each value of the current record type
            for value in values:
                difference_found = 0
                #Append a new result line
                results.append( [host, rdtype, value] )
                #For every nameserver we must lookup
                for nameserver in cache:
                    try:
                        #If the value is in the cache
                        if value in cache[nameserver][host][rdtype]:
                            results[-1].append(value)
                            results[-1].append('PASS')
                        else:
                            difference_found += 1
                            #Append the result we found
                            results[-1].append(cache[nameserver][host][rdtype][0])
                            results[-1].append('FAILED')
                    except KeyError:
                        difference_found += 1
                        results[-1].append('NXDOMAIN')
                        results[-1].append('FAILED')

                if difference_found > 0:
                   results[-1].append('FAILED')
                else:    
                   results[-1].append('PASS')

    return results


def getEquivalentHostFile(dnsdata):
    results = []

    #For every DNS records of a single hostname, get all the DNS entries
    for host in dnsdata:
        try:
            #For every record type, get all the values
            current_host = host
            current_ip = None
            entries = dnsdata[host]

            while True:
                if 'A' in entries:
                    #Found
                    current_ip = entries['A'][0]
                    results.append( (current_ip, host) )
                    break
                elif 'CNAME' in entries:
                    current_host = entries['CNAME'][0]
                    entries = dnsdata[current_host]
                else:
                    break

        except KeyError:
            pass

    return results


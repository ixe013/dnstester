# -*- coding: utf-8 -*-
import dns
import dns.flags
import dns.message
import dns.name
import dns.query
import dns.rdatatype
import dns.resolver
import logging
import socket

def getAuthoritativeNameserver(domain, log=lambda msg: None):
    """Returns the IP address of the authoritative for *domain*.
    Taken from http://stackoverflow.com/a/4066624/591064

    :param string domain: The domain for which the DNS servers is requested
    :param log: A callable object that will log progress
    """
    n = dns.name.from_text(domain)

    depth = 2
    default = dns.resolver.get_default_resolver()
    nameserver = default.nameservers[0]

    last = False
    while not last:
        s = n.split(depth)

        last = s[0].to_unicode() == u'@'
        sub = s[1]

        log('Looking up %s on %s' % (sub, nameserver))
        query = dns.message.make_query(sub, dns.rdatatype.NS)
        response = dns.query.udp(query, nameserver)

        rcode = response.rcode()
        if rcode != dns.rcode.NOERROR:
            if rcode == dns.rcode.NXDOMAIN:
                raise Exception('%s does not exist.' % sub)
            else:
                raise Exception('Error %s' % dns.rcode.to_text(rcode))

        rrset = None
        if len(response.authority) > 0:
            rrset = response.authority[0]
        else:
            rrset = response.answer[0]

        rr = rrset[0]
        if rr.rdtype == dns.rdatatype.SOA:
            log('Same server is authoritative for %s' % sub)
        else:
            authority = rr.target
            log('%s is authoritative for %s' % (authority, sub))
            nameserver = default.query(authority).rrset[0].to_text()

        depth += 1

    return nameserver


def getNameserverForHost(host=None):
    """Returns an list of nameservers configured for this *host*.

    :para string host: The host name the nameservers are requested for. 
    The hostname will be used instead if host is None.
    """
    nameservers = []
    hostname = host

    if host :
        hostname = host
    else:
        hostname = socket.getfqdn()     

    domain = '.'.join(hostname.split('.')[1:])

    for nameserver in dns.resolver.query(domain, 'NS'):
        for records in dns.resolver.query(nameserver.to_text(), 'A'):
            nameservers.append(records.to_text())

    return nameservers


def getRecordValues(domain, name_server):
    """
    Returns a simplified Python data structure that is easier to
    work with, at the expense of loosing some information like TTL.

    Heavily inspired by http://stackoverflow.com/a/17695103/591064
    """
    result = {}

    ADDITIONAL_RDCLASS = 65535

    domain = dns.name.from_text(domain)
    if not domain.is_absolute():
        domain = domain.concatenate(dns.name.root)

    request = dns.message.make_query(domain, dns.rdatatype.ANY)
    request.flags |= dns.flags.AD
    request.find_rrset(request.additional, dns.name.root, ADDITIONAL_RDCLASS,
                       dns.rdatatype.OPT, create=True, force_unique=True)
    response = dns.query.udp(request, name_server)

    for record in response.answer:
        result.setdefault(dns.rdatatype.to_text(record.rdtype), [])
        for entry in record:
            result[dns.rdatatype.to_text(record.rdtype)].append(entry.to_text())

    return result


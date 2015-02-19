# -*- coding: utf-8 -*-
from pprint import pprint as pp
import dnsfacade

def log(msg):
    print msg

#print dnsfacade.getAuthoritativeNameserver('www.paralint.com', log)
cache = {}

nameservers = dnsfacade.getNameserverForHost('www.paralint.com')

for nameserver in nameservers:
    cache[nameserver] = { 'paralint.com' : dnsfacade.getRecordValues('paralint.com', nameserver) }

pp(cache)

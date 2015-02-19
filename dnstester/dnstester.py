# -*- coding: utf-8 -*-
if __name__ == '__main__':
    import dnsfacade
    from pprint import pprint as pp

    cache = {}

    nameservers = dnsfacade.getNameserverForHost('www.paralint.com')

    for nameserver in nameservers:
        cache[nameserver] = { 'paralint.com' : dnsfacade.getRecordValues('paralint.com', nameserver) }

    pp(cache)


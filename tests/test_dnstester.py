import dnstester.analyze

class TestClass:
    def test_getComparaisonHeaders(self):
        nameservers = { 'NS1':None, 'NS2':None }
        headers = dnstester.analyze.getComparaisonHeaders({}, nameservers)
        assert headers == ['Host', 'Record type', 'Expected', 'Nameserver NS1', 'Result', 'Nameserver NS2', 'Result', 'Overall result']

        


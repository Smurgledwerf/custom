import os, sys, math, hashlib, getopt, tacticenv
from tactic_client_lib import TacticServerStub
server = TacticServerStub.get()
sources = server.eval("@SOBJECT(twog/source)")
len_sources = len(sources)
count1 = 0
while count1 < len_sources:
    count2 = count1 + 1
    while count2 < len_sources:
        if sources[count1].get('barcode') == sources[count2].get('barcode'):
            sc1 = sources[count1]
            sc2 = sources[count2]
            print "BARCODE: %s, SOURCE1 Title/CODE = %s:%s/%s, SOURCE2 Title/CODE = %s:%s/%s" % (sc1.get('barcode'), sc1.get('title'), sc1.get('episode'), sc1.get('code'), sc2.get('title'), sc2.get('episode'), sc2.get('code'))
        count2 = count2 + 1
    count1 = count1 + 1
    


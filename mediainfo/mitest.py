import os, sys, getopt, pprint
from random import randint
class MITest:
    def __init__(self):
        nothing = 'true'
    def get_mi(my, filename):
        rando = randint(2,100)
        info = {}
        handle = ''
        if filename not in [None,'']:
            pp = pprint.PrettyPrinter(depth=3)
            dump_file = 'mediainfo%s' % rando
            os.system('mediainfo %s > %s' % (filename, dump_file))
            f = open(dump_file, 'r')
            for line in f:
                if not line.strip():
                    continue
                else:
                    line = line.replace('\n','')
                    if 'ERROR:' not in line:
                        if ':' not in line:
                            handle = line.rstrip()
                            handle = handle.lstrip()
                            #if '#' in handle and 'Audio' in handle:
                            #    number = handle.split('#')[1]
                            #    handle = 'audio_ch_%s' % number
                            if handle not in info.keys():
                                info[handle] = {}
                        else:
                            colsplit = line.split(':')
                            what = colsplit[0].replace('  ','')
                            value = ''
                            for r in range(1,len(colsplit)):
                                if value == '':
                                    value = colsplit[r].strip()
                                else:
                                   value = '%s:%s' % (value, colsplit[r].strip())
                            info[handle][what] = value
            os.system('rm -rf %s' % dump_file)
            #pp.pprint(info)
        return info
    

import os, sys, math, hashlib, getopt, tacticenv, time
from tactic_client_lib import TacticServerStub
def kill_mul_spaces(origstrg):
    newstrg = ''
    for word in origstrg.split():
        newstrg=newstrg+' '+word
    return newstrg
def extract_key_and_value(xml_string):
    chunker = xml_string.split('"')
    key = chunker[1]
    first_chunk = chunker[2].split('</')[0]
    value = first_chunk[1:]
    return [key, value]
def split_and_insert(in_str, ch, missing_ch):
    new_str = in_str
    changed = False
    if ch in in_str:
        splits = in_str.split(ch)
        for sp in splits:
            if sp != '':
                if sp[len(sp) - 2] != missing_ch:
                    if changed:
                        new_str = '%s%s%s%s' % (new_str, sp[:len(sp) - 2], missing_ch, ch) 
                    else:
                        new_str = '%s%s%s' % (sp[:len(sp) - 2], missing_ch, ch) 
                    changed = True
    return new_str
def correct_quotes(in_str):
    in_str = split_and_insert(in_str, "'", "\\")
    in_str = split_and_insert(in_str, '"', "\\")
    in_str = split_and_insert(in_str, "`", "\\")
    return in_str
    
lines_arr = []
opts, file_name = getopt.getopt(sys.argv[1], '-m')
print "file_name = %s" % file_name
print file_name
f= open(file_name, 'r')
locations = []
line_num = 0
record_count = 0
for line in f:
    if not line.strip():
        continue
    else:
        if '<row>' in line:
            record_count = record_count + 1
        elif '</row>' in line:
            source_data = {}
        else:
	    line = line.rstrip('\r\n')
            key, value = extract_key_and_value(line)
            key = key.strip()
            value = value.strip()
            if key == 'location':
                if value.upper() not in locations:
                    locations.append(value.upper())
    line_num = line_num + 1

f.close()
locations.sort()
print "done sorting..."
for location in locations:
    print "'%s': ''," % location
                


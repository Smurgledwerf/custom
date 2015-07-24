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
def internal_search_by_code(code, lookup_dict):
    send_back = None
    for guy in lookup_dict:
        if code == guy.get('code'):
            send_back = guy
            break
    return send_back
def make_table_dict(filename):
    f= open(filename, 'r')
    data = []
    line_data = {}
    counter = 0
    columns = None
    for line in f:
        if not line.strip():
            continue
        else:
	    line = line.rstrip('\r\n')
            if counter == 0:
                columns = line.split('\t')
            else:
                line_data = {}
                splitted = line.split('\t')
                count2 = 0
                for spli in splitted:
                    line_data[kill_mul_spaces(columns[count2]).strip()] = kill_mul_spaces(spli).strip()
                    count2 = count2 + 1
                data.append(line_data)
            counter = counter + 1
        
    f.close()
    return data
     
opts, source_filename = getopt.getopt(sys.argv[1], '-m')
print "source_filename = %s" % source_filename
opts, locations_filename = getopt.getopt(sys.argv[2], '-m')
print "locations_filename = %s" % locations_filename
server = TacticServerStub.get(protocol="xmlrpc")
#server.start('FIXING SOURCES AND THINGS')
all_atms = server.eval("@SOBJECT(twog/asset_to_movement)")
print "GOT ATMS"
all_movements = server.eval("@SOBJECT(twog/movement)")
print "GOT MOVEMENTS"
#all_sources = server.eval("@SOBJECT(twog/source)")
all_sources = make_table_dict(source_filename)
print "GOT SOURCES"
all_companies = server.eval("@SOBJECT(twog/company)")
print "GOT COMPANIES"
id_to_in_out = {}
sources = []
last_atm = all_atms[len(all_atms) - 1]
result_file = open('sql_update_atm_result', 'w')
for atm in all_atms:
    movement_code = atm.get('movement_code')
    strat2g_id = source_code = atm.get('source_code')
    movement = internal_search_by_code(movement_code, all_movements)
    sending_company_name = ''
    receiving_company_name = ''
    source = None
    if movement not in [None,[]]:
        sender = internal_search_by_code(movement.get('sending_company_code'), all_companies)
        if sender not in [None,[]]:
            sending_company_name = sender.get('name')
        receiver = internal_search_by_code(movement.get('receiving_company_code'), all_companies)
        if receiver not in [None,[]]:
            receiving_company_name = receiver.get('name')
        source = internal_search_by_code(source_code, all_sources)
    barcode = ''
    if source not in [None,[]]:
        barcode = source.get('barcode')
        print "BARCODE = %s, source = %s" % (barcode, source.get('code'))
        strat2g_id = source.get('strat2g_id')
        if source.get('id') not in sources:
            sources.append(source.get('id'))
        if source.get('strat2g_id') in [None,'']:
            result_file.write("update source set strat2g_id = '%s' where code = '%s';\n" % (source.get('code'), source.get('code')))
        if atm.get('barcode') in [None,''] and barcode not in [None,'']:
            result_file.write("update asset_to_movement set barcode = '%s' where code = '%s';\n" % (barcode, atm.get('code')))
    location_bool = False
    if '2g digital' in sending_company_name.lower():
        location_bool = False
    if '2g digital' in receiving_company_name.lower():
        location_bool = True
    if strat2g_id not in id_to_in_out.keys():
        id_to_in_out[strat2g_id] = []
    comp_insert = str(receiving_company_name.upper().strip())
    if comp_insert == 'NULL':
        comp_insert = 'CLIENT'
    id_to_in_out[strat2g_id] = [str(location_bool), comp_insert]
result_file.close()

lines_arr = []
print locations_filename
f= open(locations_filename, 'r')
source_data = {}
record_count = 0
line_num = 0
for line in f:
    if not line.strip():
        continue
    else:
	line = line.rstrip('\r\n')
        if '<row>' in line:
            record_count = record_count + 1
        elif '</row>' in line:
            source_data = {}
        else:
            key, value = extract_key_and_value(line)
            key = key.strip()
            value = value.strip()
            correct_key = ''
            location_bool = False
            if key == 'id':
                source_id = value
                if source_id not in sources:
                    sources.append(source_id)
            if key == 'location' and source_id not in id_to_in_out.keys(): 
                if '2g digital' in value.lower(): 
                    location_bool = True
                    id_to_in_out[source_id] = [str(location_bool), str('2G DIGITAL'.strip())]
                else:
                    comp_insert = str(value.upper().strip())
                    if comp_insert == 'NULL':
                        comp_insert = 'CLIENT'
                    id_to_in_out[source_id] = [str(location_bool), comp_insert]
        line_num = line_num + 1

f.close()
print id_to_in_out
location_fixer = open('sql_update_location_fixer', 'w')
sources.sort()
print "done sorting..."
all_atm_sources = []
for atm in all_atms:
    all_atm_sources.append(atm.get('source_code'))
for source in sources:
    if source in id_to_in_out.keys():
         print "update source set in_house = '%s', company_location = '%s' where strat2g_id = '%s';\n" % (id_to_in_out[source][0], id_to_in_out[source][1].strip(), source) 
         location_fixer.write("update source set in_house = '%s', company_location = '%s' where strat2g_id = '%s';\n" % (id_to_in_out[source][0], id_to_in_out[source][1].strip(), source)) 
for source in all_sources:
    if source.get('in_house') in [None,'']:
        if source.get('strat2g_id') in [None,'']:
            if source.get('code') not in all_atm_sources:
                location_fixer.write("update source set in_house = 'True', company_location = '2G DIGITAL ASSUMED', strat2g_id = '%s' where code = '%s';\n" % (source.get('code'),source.get('code')))
location_fixer.close()









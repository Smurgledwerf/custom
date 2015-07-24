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
            result_file.write('update source set strat2g_id = "%s" where code = "%s";\n' % (source.get('code'), source.get('code')))
        if atm.get('barcode') in [None,''] and barcode not in [None,'']:
            result_file.write('update asset_to_movement set barcode = "%s" where code = "%s";\n' % (barcode, atm.get('code')))
    location_bool = False
    if '2g digital' in sending_company_name.lower():
        location_bool = False
    if '2g digital' in receiving_company_name.lower():
        location_bool = True
    if strat2g_id not in id_to_in_out.keys():
        id_to_in_out[strat2g_id] = []
    id_to_in_out[strat2g_id] = [str(location_bool), str(receiving_company_name.upper().strip())]
result_file.close()


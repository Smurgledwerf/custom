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
    
server = TacticServerStub.get(protocol="xmlrpc")
lines_arr = []
opts, file_name = getopt.getopt(sys.argv[1], '-m')
print "file_name = %s" % file_name
opts, last_passed_in = getopt.getopt(sys.argv[2], '-m')
print "last_passed_in = %s" % last_passed_in
print file_name
f= open(file_name, 'r')
active_directory = ''
count = 0
fields = [] 
sd = {}
sources = []
correct_fields = {'id': 'strat2g_id', 'people_id': 'strat2g_people_id', 'element_creation_date': 'timestamp', 'studio_id': 'strat2g_studio_id', 'label_date': 'strat2g_label_date', 'client_ref1': 'strat2g_client_ref1', 'client_ref2': 'strat2g_client_ref2', 'parent': 'strat2g_parent', 'child': 'strat2g_child', 'wo_num': 'strat2g_wo_num', 'project_num': 'strat2g_project_num', 'box_barcode': 'strat2g_box_barcode', 'studio': 'strat2g_studio', 'last_update': 'strat2g_last_update', 'creation_date': 'strat2g_creation_date', 'search_field': 'strat2g_search_field', 'mergebc': 'strat2g_mergebc', 'merge_notes': 'strat2g_merge_notes', 'prod_co': 'strat2g_prod_co', 'aka': 'strat2g_aka','production_number': 'strat2g_production_number', 'season_number': 'strat2g_season_number', 'episode_number': 'strat2g_episode_number', 'type': 'strat2g_type', 'version': 'version', 'alert': 'strat2g_alert', 'part': 'strat2g_part', 'location_id': 'strat2g_location_id', 'file_id': 'strat2g_file_id', 'asset_dir': 'strat2g_asset_dir', 'last_movement_id': 'strat2g_last_movement_id', 'f_type': 'strat2g_f_type', 'PO_num': 'strat2g_po_num', 'trt_all': 'strat2g_trt_all', 'trt': 'total_run_time', 'framerate': 'frame_rate', 'outside_bc_1': 'strat2g_outside_bc_1', 'outside_bc_2': 'strat2g_outside_bc_2', 'outside_bc_3': 'strat2g_outside_bc_3'}
record_count = 0
line_num = 1
source_data = {}
source_id = ''
for line in f:
	if not line.strip():
		continue
	else:
		line = line.rstrip('\r\n')
                if '<row>' in line:
                    record_count = record_count + 1
                elif '</row>' in line:
                    sd[source_id] = source_data
                    source_data = {}
                else:
                    key, value = extract_key_and_value(line)
                    key = key.strip()
                    value = value.strip()
                    correct_key = ''
                    if key == 'id':
                        source_id = value
                        sources.append(source_id)
                    if 'audio_ch' in key:
                        correct_key = 'audio_ch_%s' % key.split('ch')[1]
                    else:
                        if key in correct_fields.keys():
                            correct_key = correct_fields[key]
                        else:
                            correct_key = key
                    source_data[correct_key] = correct_quotes(kill_mul_spaces(value)).lstrip().rstrip()
        line_num = line_num + 1

f.close()
server.start('IMPORTING SOURCES AND THINGS')
data = []
counter = 0
begin = 100000000000
end = 0
print "sorting..."
sources.sort()
print "done sorting..."
print "SD = %s" % sd
for source in sources:
    if int(source) > int(last_passed_in):
        data = sd[source]
        bc_expr = "@SOBJECT(twog/source['barcode','%s'])" % data.get('barcode')
        bcs = server.eval(bc_expr)
        if len(bcs) < 1:
            if int(source) < begin:
                begin = int(source)
            if int(source) > end:
                end = int(source)
            server.insert('twog/source',data) 
            print "%s Inserted %s" % (file_name, source)
            counter = counter + 1
        else:
            bcs_list = ''
            for bc in bcs:
                if bcs_list == '':
                    bcs_list = '%s' % (bc.get('strat2g_id'))
                else:
                    bcs_list = '%s,%s' % (bcs_list, bc.get('strat2g_id'))
            os.system('echo "BARCODE: %s  -- The following strat2g_ids have the same barcode as the one you tried to import (%s): %s" >> bad_outputs' % (data.get('barcode'), data.get('strat2g_id'), bcs_list))
print "Did import of %s assets. Begin Source_id = %s, End Source_id = %s" % (counter, begin, end)
time.sleep(20)
                
server.finish()


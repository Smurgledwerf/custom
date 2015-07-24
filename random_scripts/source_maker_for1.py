import os, sys, math, hashlib, getopt, tacticenv
from tactic_client_lib import TacticServerStub
def kill_mul_spaces(origstrg):
    newstrg = ''
    for word in origstrg.split():
        newstrg=newstrg+' '+word
    return newstrg

server = TacticServerStub.get(protocol="xmlrpc")
lines_arr = []
opts, file_name = getopt.getopt(sys.argv[1], '-m')
opts, last_passed_in = getopt.getopt(sys.argv[2], '-m')
print file_name
f= open(file_name, 'r')
active_directory = ''
count = 0
fields = [] 
sd = {}
sources = []
correct_fields = {'id': 'strat2g_id', 'people_id': 'strat2g_people_id', 'element_creation_date': 'timestamp', 'studio_id': 'strat2g_studio_id', 'label_date': 'strat2g_label_date', 'client_ref1': 'strat2g_client_ref1', 'client_ref2': 'strat2g_client_ref2', 'parent': 'strat2g_parent', 'child': 'strat2g_child', 'wo_num': 'strat2g_wo_num', 'project_num': 'strat2g_project_num', 'box_barcode': 'strat2g_box_barcode', 'studio': 'strat2g_studio', 'last_update': 'strat2g_last_update', 'creation_date': 'strat2g_creation_date', 'search_field': 'strat2g_search_field', 'mergebc': 'strat2g_mergebc', 'merge_notes': 'strat2g_merge_notes', 'prod_co': 'strat2g_prod_co', 'aka': 'strat2g_aka','production_number': 'strat2g_production_number', 'season_number': 'strat2g_season_number', 'episode_number': 'strat2g_episode_number', 'type': 'strat2g_type', 'version': 'version', 'alert': 'strat2g_alert', 'part': 'strat2g_part', 'location_id': 'strat2g_location_id', 'file_id': 'strat2g_file_id', 'asset_dir': 'strat2g_asset_dir', 'last_movement_id': 'strat2g_last_movement_id', 'f_type': 'strat2g_f_type', 'PO_num': 'strat2g_po_num', 'trt_all': 'strat2g_trt_all', 'trt': 'total_run_time', 'framerate': 'frame_rate', 'outside_bc_1': 'strat2g_outside_bc_1', 'outside_bc_2': 'strat2g_outside_bc_2', 'outside_bc_3': 'strat2g_outside_bc_3'}
for line in f:
	if not line.strip():
		continue
	else:
		line = line.rstrip('\r\n')
                if count == 0:
                    fields_preclean = line.split('\t')
                    for field in fields_preclean:
                        if field.find('xbb') == -1:
                            if field in correct_fields.keys():
                                fields.append(correct_fields.get(field))
                            elif field.find('audio') != -1:
                                fields.append('audio_ch_%s' % field.split('ch')[1])
                            else:
                                fields.append(field)
                else:
                    data = line.split('\t')
                    source_id = data[0]
                    if source_id not in sources and int(source_id) > int(last_passed_in):
                        sources.append(source_id)
                        sd[source_id] = {}
                        ind = 0
                        for d in data:
                            #print "D = %s" % d
                            preclean = kill_mul_spaces(d.strip())
                            print "SID =%s" % source_id
                            #print "IND = %s" % ind
                            #print "F[IND] = %s" % fields[ind]
                            sd[source_id][fields[ind]] = preclean.strip() 
                            #sd[source_id][fields[ind]] = cleaned 
                            ind = ind + 1
                count = count + 1
f.close()
server.start('IMPORTING SOURCES AND THINGS')
for source in sources:
    print "SOURCE ID = %s" % source
    if int(source) > int(last_passed_in):
        data = sd[source]
        server.insert('twog/source',data) 
                
server.finish()

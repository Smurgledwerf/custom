import os, sys, math, hashlib, getopt, tacticenv, time
def kill_mul_spaces(origstrg):
    newstrg = ''
    for word in origstrg.split():
        newstrg=newstrg+' '+word
    return newstrg

def make_data_dict(file_name):
    the_file = open(file_name, 'r')
    fields = []
    data_dict = {}
    count = 0
    boolio = True
    code_index = 0
    for line in the_file:
        line = line.rstrip('\r\n')
        #data = line.split('\t')
        data = line.split('|')
        if boolio:
            if count == 0:
                field_counter = 0
                for field in data:
                    field = kill_mul_spaces(field)
                    field = field.strip(' ')
                    fields.append(field)
                    if field == 'code':
                        code_index = field_counter
                    field_counter = field_counter + 1
                        
            elif count == 1:
                print file_name
                print line
            elif data[0][0] == '(':
                print "END OF FILE"
                boolio = False
            else:
                data_count = 0
                this_code = ''
                this_data = {}
                for val in data:
                    val = kill_mul_spaces(val)
                    val = val.strip(' ')
                    if data_count == code_index:
                        this_code = val
                    this_data[fields[data_count]] = val
                    data_count = data_count + 1 
                data_dict[this_code] = this_data
            count = count + 1  
    the_file.close()
    #print "File = %s FIELDS = %s" % (file_name, fields)
    id_dict = {}
    for code, dd in data_dict.iteritems():
        id_dict[dd.get('id')] = dd
    return [data_dict, id_dict]

opts, note_file = getopt.getopt(sys.argv[1], '-m')
print "note_file = %s" % note_file
opts, work_order_file = getopt.getopt(sys.argv[2], '-m')
print "work_order_file = %s" % work_order_file
opts, proj_file = getopt.getopt(sys.argv[3], '-m')
print "proj_file = %s" % proj_file
opts, title_file = getopt.getopt(sys.argv[4], '-m')
print "title_file = %s" % title_file
opts, order_file = getopt.getopt(sys.argv[5], '-m')
print "order_file = %s" % order_file

CODE = 0
ID = 1
notes = make_data_dict(note_file)
work_orders = make_data_dict(work_order_file)
projs = make_data_dict(proj_file)
titles = make_data_dict(title_file)
orders = make_data_dict(order_file)
note_codes = notes[CODE].keys()
work_order_codes = work_orders[CODE].keys()
proj_codes = projs[CODE].keys()
title_codes = titles[CODE].keys()
order_codes = orders[CODE].keys()
out_lines = []
problem_lines = []
st_lookup = {'twog/order': orders[ID], 'twog/title': titles[ID], 'twog/proj': projs[ID], 'twog/work_order': work_orders[ID]}
for note_code in note_codes:
    #Expected first
    note = notes[CODE][note_code]
    st = note.get('search_type').split('?')[0]
    search_id = note.get('search_id')
    wo_code = ''
    p_code = ''
    t_code = ''
    o_code = ''
    if search_id not in [None,''] and st in st_lookup.keys() and st in ['twog/title','twog/order'] and (note.get('title_code') in [None,''] or note.get('order_code') in [None,'']): #MTM added this because we don't want dupes at the order level with the work order notes
	    if search_id in st_lookup[st].keys():
		item = st_lookup[st][search_id]
		item_code = item.get('code')
		if 'WORK_ORDER' in item_code:
		    wo_code = item_code
		    p_code = item.get('proj_code')
		    if p_code in proj_codes:
			proj = projs[CODE][p_code]
			t_code = proj.get('title_code')
			if t_code in title_codes:
			    title = titles[CODE][t_code]
			    o_code = title.get('order_code')
		elif 'PROJ' in item_code:
		    p_code = item_code
		    t_code = item.get('title_code')
		    if t_code in title_codes:
			title = titles[CODE][t_code]
			o_code = title.get('order_code')
		elif 'TITLE' in item_code:
		    t_code = item_code
		    o_code = item.get('order_code')
		elif 'ORDER' in item_code:
		    o_code = item_code
		out_lines.append('''update note set order_code = '%s', title_code = '%s', proj_code = '%s', work_order_code = '%s' where code = '%s';''' % (o_code, t_code, p_code, wo_code, note.get('code')))
	    else:
		problem_lines.append('''%s has search type of %s, BAD Search_Id = %s''' % (note.get('code'), st, search_id))
    else:
        problem_lines.append('''%s has search type of %s, BAD Search_Id = %s''' % (note.get('code'), st, search_id))
                                                      
                                
out_file = open('note_relinker','w')
for ol in out_lines:
    out_file.write('%s\n' % ol)
out_file.close()
problem_file = open('note_problems', 'w')
for pl in problem_lines:
    problem_file.write('%s\n' % pl)
problem_file.close()

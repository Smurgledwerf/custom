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
    for line in the_file:
        line = line.rstrip('\r\n')
        data = line.split('\t')
        if count == 0:
            for field in data:
                field = kill_mul_spaces(field)
                field = field.strip(' ')
                fields.append(field)
        else:
            data_count = 0
            this_code = ''
            for val in data:
                val = kill_mul_spaces(val)
                val = val.strip(' ')
                if data_count == 0:
                    data_dict[val] = {}
                    this_code = val
                else:
                    data_dict[this_code][fields[data_count]] = val
                data_count = data_count + 1 
        count = count + 1  
    the_file.close()
    return data_dict
lookup_codes = {'EQUIPMENT00102': 'EQUIPMENT00193','EQUIPMENT00103': 'EQUIPMENT00194','EQUIPMENT00104': 'EQUIPMENT00195','EQUIPMENT00105': 'EQUIPMENT00195','EQUIPMENT00106': 'EQUIPMENT00195','EQUIPMENT00107': 'EQUIPMENT00195','EQUIPMENT00108': 'EQUIPMENT00195','EQUIPMENT00109': 'EQUIPMENT00196','EQUIPMENT00110': 'EQUIPMENT00196','EQUIPMENT00111': 'EQUIPMENT00196','EQUIPMENT00112': 'EQUIPMENT00196','EQUIPMENT00113': 'EQUIPMENT00197','EQUIPMENT00114': 'EQUIPMENT00198','EQUIPMENT00115': 'EQUIPMENT00198','EQUIPMENT00116': 'EQUIPMENT00198','EQUIPMENT00117': 'EQUIPMENT00198','EQUIPMENT00118': 'EQUIPMENT00198','EQUIPMENT00119': 'EQUIPMENT00198','EQUIPMENT00120': 'EQUIPMENT00198','EQUIPMENT00121': 'EQUIPMENT00199','EQUIPMENT00122': 'EQUIPMENT00199','EQUIPMENT00123': 'EQUIPMENT00199','EQUIPMENT00124': 'EQUIPMENT00199','EQUIPMENT00125': 'EQUIPMENT00199','EQUIPMENT00126': 'EQUIPMENT00199','EQUIPMENT00052': 'EQUIPMENT00199','EQUIPMENT00130': 'EQUIPMENT00201','EQUIPMENT00146': 'EQUIPMENT00201','EQUIPMENT00147': 'EQUIPMENT00201','EQUIPMENT00148': 'EQUIPMENT00201','EQUIPMENT00149': 'EQUIPMENT00201','EQUIPMENT00150': 'EQUIPMENT00201','EQUIPMENT00189': 'EQUIPMENT00201','EQUIPMENT00151': 'EQUIPMENT00202','EQUIPMENT00050': 'EQUIPMENT00202','EQUIPMENT00152': 'EQUIPMENT00203','EQUIPMENT00153': 'EQUIPMENT00204','EQUIPMENT00154': 'EQUIPMENT00204','EQUIPMENT00155': 'EQUIPMENT00204','EQUIPMENT00156': 'EQUIPMENT00204','EQUIPMENT00157': 'EQUIPMENT00204','EQUIPMENT00158': 'EQUIPMENT00204','EQUIPMENT00159': 'EQUIPMENT00204','EQUIPMENT00160': 'EQUIPMENT00204','EQUIPMENT00161': 'EQUIPMENT00204','EQUIPMENT00162': 'EQUIPMENT00204','EQUIPMENT00163': 'EQUIPMENT00204','EQUIPMENT00164': 'EQUIPMENT00204','EQUIPMENT00165': 'EQUIPMENT00204','EQUIPMENT00166': 'EQUIPMENT00205','EQUIPMENT00167': 'EQUIPMENT00206','EQUIPMENT00168': 'EQUIPMENT00207','EQUIPMENT00033': 'EQUIPMENT00098','EQUIPMENT00038': 'EQUIPMENT00036','EQUIPMENT00066': 'EQUIPMENT00036','EQUIPMENT00045': 'EQUIPMENT00036','EQUIPMENT00047': 'EQUIPMENT00036','EQUIPMENT00072': 'EQUIPMENT00036','EQUIPMENT00064': 'EQUIPMENT00036','EQUIPMENT00067': 'EQUIPMENT00036','EQUIPMENT00068': 'EQUIPMENT00036','EQUIPMENT00076': 'EQUIPMENT00036','EQUIPMENT00077': 'EQUIPMENT00036','EQUIPMENT00079': 'EQUIPMENT00036','EQUIPMENT00101': 'EQUIPMENT00036','EQUIPMENT00043': 'EQUIPMENT00081','EQUIPMENT00181': 'EQUIPMENT00048','EQUIPMENT00049': 'EQUIPMENT00100','EQUIPMENT00055': 'EQUIPMENT00085','EQUIPMENT00056': 'EQUIPMENT00195','EQUIPMENT00105': 'EQUIPMENT00195','EQUIPMENT00106': 'EQUIPMENT00195','EQUIPMENT00107': 'EQUIPMENT00195','EQUIPMENT00108': 'EQUIPMENT00195','EQUIPMENT00104': 'EQUIPMENT00195','EQUIPMENT00063': 'EQUIPMENT00046','EQUIPMENT00090': 'EQUIPMENT00192','EQUIPMENT00091': 'EQUIPMENT00054','EQUIPMENT00092': 'EQUIPMENT00211','EQUIPMENT00166': 'EQUIPMENT00096','EQUIPMENT00099': 'EQUIPMENT00098','EQUIPMENT00176': 'EQUIPMENT00040', 'EQUIPMENT00129': 'EQUIPMENT00200', 'EQUIPMENT00128': 'EQUIPMENT00200', 'EQUIPMENT00069': 'EQUIPMENT00071','EQUIPMENT00173': 'EQUIPMENT00036','EQUIPMENT00073': 'EQUIPMENT00216','EQUIPMENT00074': 'EQUIPMENT00216', 'EQUIPMENT00075': 'EQUIPMENT00214', 'EQUIPMENT00177': 'EQUIPMENT00036','EQUIPMENT00178': 'EQUIPMENT00036','EQUIPMENT00179': 'EQUIPMENT00036', 'EQUIPMENT00180': 'EQUIPMENT00036','EQUIPMENT00183': 'EQUIPMENT00036','EQUIPMENT00184': 'EQUIPMENT00036','EQUIPMENT00185': 'EQUIPMENT00036','EQUIPMENT00174': 'EQUIPMENT00071'}
name_lookup = {'San Storage': 'EQUIPMENT00041','FCP': 'EQUIPMENT00036','HDCAM-SR DECK': 'EQUIPMENT00098','Aspera': 'EQUIPMENT00042','Digital Rapids': 'EQUIPMENT00040','San': 'EQUIPMENT00041','VTR-HDCAMSR': 'EQUIPMENT00098','VTR-DBC-NTSC': 'EQUIPMENT00082','VTR-DA88': 'EQUIPMENT00084','MacCaption': 'EQUIPMENT00096','Transporter': 'EQUIPMENT00044','VTR-D5': 'EQUIPMENT00085','Signiant': 'EQUIPMENT00048','Audio-Protools': 'EQUIPMENT00046','Oxygen': 'EQUIPMENT00036','ProTools': 'EQUIPMENT00046','HDCAM-SR STOCK': 'EQUIPMENT00199','Aspera-Faspex': 'EQUIPMENT00071','Legal': 'EQUIPMENT00192','SmartJog': 'EQUIPMENT00070','VTR-DBC-PAL': 'EQUIPMENT00081','VTR-HDCAM': 'EQUIPMENT00098','AudioLimit': 'EQUIPMENT00211','DBC DECK - PAL': 'EQUIPMENT00081','VTR DBC NTSC': 'EQUIPMENT00082','Aspera-Enterprise': 'EQUIPMENT00042','Media-HDCAMSR-124': 'EQUIPMENT00199','Ultech': 'EQUIPMENT00054','D5 DECK': 'EQUIPMENT00085','D5 STOCK': 'EQUIPMENT00195','Minnetonka-ATS': 'EQUIPMENT00187','Soft-Baton-QC': 'EQUIPMENT00175','Watermark-Civilution': 'EQUIPMENT00095','Volume 1 Storage': 'EQUIPMENT00041','Alchemist': 'EQUIPMENT00035','Soft-Amberfin': 'EQUIPMENT00186','NTSC Deck': 'EQUIPMENT00082','HDCAMSR': 'EQUIPMENT00098','VTR-BCSP': 'EQUIPMENT00088','Ukon': 'EQUIPMENT00078','Edit-FCP': 'EQUIPMENT00036','FinalCut': 'EQUIPMENT00036','Media-DBC064': 'EQUIPMENT00201'}
opts, equipment_used_file = getopt.getopt(sys.argv[1], '-m')
print "equipment_used_file = %s" % equipment_used_file
opts, equipment_used_cost_file = getopt.getopt(sys.argv[2], '-m')
print "equipment_used_cost_file = %s" % equipment_used_cost_file
opts, equipment_file = getopt.getopt(sys.argv[3], '-m')
print "equipment_file = %s" % equipment_file
opts, equipment_templ_file = getopt.getopt(sys.argv[4], '-m')
print "equipment_templ_file = %s" % equipment_templ_file
eq_used = make_data_dict(equipment_used_file)
eq_costs = make_data_dict(equipment_used_cost_file)
eq = make_data_dict(equipment_file)
eq_templs = make_data_dict(equipment_templ_file)
eq_used_codes = eq_used.keys()
out_lines = []
problem_lines = []
lost_names = []
for ec in eq_used_codes:
   #FIGURE OUT THE RESOLVED EQ CODE FROM LOOKUP LIST
   #IF CODE IS NOT IN LOOKUP LIST, KEEP THE CODE AND DO THE SAME THING BELOW 
   eq_used_code = ec
   current_name = eq_used[ec]['name']
   #print "this entry = %s" % eq_used[ec]
   current_eq_code = eq_used[ec]['equipment_code']
   if current_eq_code in [None,'']:
       if current_name in name_lookup.keys():
           current_eq_code = name_lookup[current_name]
   if current_eq_code not in [None,'']:
       resolved_eq_code = current_eq_code
       if current_eq_code in lookup_codes.keys():
           #print "IT HAS A LOOKUP"
           resolved_eq_code = lookup_codes[current_eq_code] 
       #GET NAME FROM EQ LIST AND SET NAME AND CODE TO RESOLVED NAME
       if resolved_eq_code in eq.keys():
           new_name = eq[resolved_eq_code]['name']
           out_lines.append("update equipment_used set name = '%s' where code = '%s';" % (new_name, eq_used_code))
           out_lines.append("update equipment_used set equipment_code = '%s' where code = '%s';" % (resolved_eq_code, eq_used_code))
           #LOOK AT RESOLVED EQ CODE LENGTHS, IF IT HAS LENGTHS, TRY TO FIGURE OUT WHAT THE LENGTH WAS FROM THE OLD NAME.
           #IF YOU FIND IT, SET THE EQUIPMENT_USED LENGTH, as LONG AS THE EQ_USED DOESNT CURRENTLY HAVE A LENGTH
           if eq[resolved_eq_code]['lengths'] not in [None,'']:
               if eq_used[eq_used_code]['length'] in [None,'']:
                   possible_lengths = eq[resolved_eq_code]['lengths']
                   len_to_add = ''
                   if possible_lengths == 'SINGLE':
                       len_to_add = 'SINGLE' 
                   else:
                       possible_lengths = possible_lengths.split(',')
                       possible_lengths = possible_lengths[::-1]
                       for le in possible_lengths:
                           if le in current_name or le == 'SINGLE':
                               if len_to_add == '':
                                   len_to_add = le
                   if len_to_add != '':
                       out_lines.append("update equipment_used set length = '%s' where code = '%s';" % (len_to_add, eq_used_code)) 
                   else:
                       problem_lines.append("Could not find a length for %s, %s" % (eq_used_code, current_name))
                   # Calculate the length cost here, update
                   if len_to_add != '':
                       found = False
                       for eck in eq_costs.keys():
                           if eq_costs[eck]['equipment_code'] == resolved_eq_code and eq_costs[eck]['length'] == len_to_add and eq_costs[eck]['unit'] == 'length':
                               cost = eq_costs[eck]['cost']
                               if cost in [None,'']:
                                   cost = 0
                               cost = float(cost)
                               quant = eq_used[eq_used_code]['expected_quantity']
                               if quant in [None,'',0,'0']:
                                   quant = 1
                               quant = float(quant)
                               set_cost = float(cost * quant)
                               if set_cost > 0:
                                   out_lines.append("update equipment_used set expected_cost = '%s' where code = '%s';" % (set_cost, eq_used_code))
                                   out_lines.append("update equipment_used set actual_cost = '%s' where code = '%s';" % (set_cost, eq_used_code))
                               else:
                                   problem_lines.append("ZERO COST calculated for %s:%s, %s:%s::: %s" % (len_to_add, eq_used_code, current_name, resolved_eq_code, new_name, set_cost))
                               found = True
                       if not found:
                           problem_lines.append("Could not find the length(%s) price for %s:%s, %s:%s" % (eq_used_code, current_name, resolved_eq_code, new_name))
           else:
               # Calculate the cost normally here, update
               units = eq_used[eq_used_code]['units']
               divisor = 1
               if units in [None,'']:
                   units = 'items' 
               if units == 'items':
                   units = 'hr'
               if units == 'mb':
                   units == 'gb'
                   divisor = .01
               if current_name in ['Signiant','Aspera','Transporter','Aspera-Enterprise','Aspera-Faspex','San Storage','SmartJog']:
                   units = 'gb'
               actual_quant = expected_quant = eq_used[eq_used_code]['expected_quantity']
               expected_dur = eq_used[eq_used_code]['expected_duration']
               if expected_dur in [None,'',0,'0']:
                   expected_dur = 1
               actual_dur = eq_used[eq_used_code]['actual_duration']
               if actual_dur in [None,'',0,'0']:
                   actual_dur = 0
               expected_dur = float(expected_dur)
               actual_dur = float(actual_dur)
               if expected_quant in [None,'','0',0]:
                   actual_quant = expected_quant = 1 
                   out_lines.append("update equipment_used set actual_quantity = 1, expected_quantity = 1 where code = '%s';" % eq_used_code)
               actual_quant = expected_quant = float(expected_quant)
               found = False
               for eck in eq_costs.keys():
                   if eq_costs[eck]['equipment_code'] == resolved_eq_code and eq_costs[eck]['unit'] == units:
                       cost = eq_costs[eck]['cost']
                       if cost in [None,'']:
                           cost = 0
                       cost = float(cost)
                       actual_cost = 0
                       expected_cost = 0
                       if units in ['hr','items']:
                           expected_cost = float(expected_dur * expected_quant * cost)
                           actual_cost = float(actual_dur * actual_quant * cost)
                       else:
                           expected_cost = float(expected_quant * expected_dur * divisor * cost)
                           actual_cost = expected_cost
                       out_lines.append("update equipment_used set expected_cost = '%s' where code = '%s';" % (expected_cost, eq_used_code))
                       out_lines.append("update equipment_used set actual_cost = '%s' where code = '%s';" % (actual_cost, eq_used_code))
                       found = True
               if not found:
                   problem_lines.append("Couldn't find cost for %s:%s, %s:%s, units: %s" % (eq_used_code, current_name, resolved_eq_code, new_name, units))  
       else:
           problem_lines.append('Deleted Equipment_code for %s, %s: %s' % (eq_used_code, current_name, resolved_eq_code))
   else:
       problem_lines.append('No Equipment_code for %s, %s' % (eq_used_code, current_name))     
       if current_name not in lost_names:
           lost_names.append(current_name)
   
   # Now need to update eq_templs eq_codes and names
for et in eq_templs.keys():
    #FIGURE OUT THE RESOLVED EQ CODE FROM LOOKUP LIST
    #IF CODE IS NOT IN LOOKUP LIST, KEEP THE CODE AND DO THE SAME THING BELOW 
    eq_templ_code = et
    #print '%s: %s' % (et, eq_templs[et])
    current_name = eq_templs[et]['name']
    current_eq_code = eq_templs[et]['equipment_code']
    if current_eq_code in [None,'']:
        if current_name in name_lookup.keys():
            current_eq_code = name_lookup[current_name]
    if current_eq_code not in [None,'']:
        resolved_eq_code = current_eq_code
        if current_eq_code in lookup_codes.keys():
            resolved_eq_code = lookup_codes[current_eq_code] 
        if resolved_eq_code in eq.keys():
            #GET NAME FROM EQ LIST AND SET NAME AND CODE TO RESOLVED NAME
            new_name = eq[resolved_eq_code]['name']
            out_lines.append("update equipment_used_templ set name = '%s' where code = '%s';" % (new_name, eq_templ_code))
            out_lines.append("update equipment_used_templ set equipment_code = '%s' where code = '%s';" % (resolved_eq_code, eq_templ_code))
        else:
            problem_lines.append("Deleted Equipment_code for %s, %s: %s" % (eq_templ_code, current_name, resolved_eq_code))
    else:
        problem_lines.append('No Equipment_code for %s, %s' % (eq_templ_code, current_name)) 

problem_file = open('EqUpdateProblems', 'w')
for pl in problem_lines:
    problem_file.write('%s\n' % pl)
problem_file.close()
update_file = open('EqUpdateGoods', 'w')
for ol in out_lines:
    update_file.write('%s\n' % ol)
update_file.close()
lost_file = open('EqUpdateLost', 'w')
for ln in lost_names:
    lost_file.write('%s\n' % ln)
lost_file.close()
   # Also need to make sure you have all of the equipment in the list now


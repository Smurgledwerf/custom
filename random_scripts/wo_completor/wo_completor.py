import os, sys, math, hashlib, getopt, tacticenv, time
from tactic_client_lib import TacticServerStub
server = TacticServerStub.get()

def make_data_dict(file_name):
    the_file = open(file_name, 'r')
    data_dict = {}
    wos = []
    for line in the_file:
        line = line.rstrip('\r\n')
        wo_code = line
        #print wo_code
        this_wo = {'code': wo_code, 'order': None, 'work_hours': None, 'task': None, 'work_order': None}
        wo_expr = "@SOBJECT(twog/work_order['code','%s'])" % wo_code
        work_order = server.eval(wo_expr)
        if work_order:
            work_order = work_order[0]
            this_wo['work_order'] = work_order
            #if work_order.get('work_group') == 'qc':
            #    print work_order.get('process')
        no_send = False
        task_expr = "@SOBJECT(sthpw/task['lookup_code','%s'])" % wo_code
        task = server.eval(task_expr)
        if task:
            task = task[0]
            this_wo['task'] = task
            work_hours_expr = "@SOBJECT(sthpw/work_hour['task_code','%s'])" % task.get('code')
            work_hours = server.eval(work_hours_expr)
            this_wo['work_hours'] = work_hours
        else:
            no_send = True
        order_expr = "@SOBJECT(twog/work_order['code','%s'].twog/proj.twog/title.twog/order)" % wo_code   
        order = server.eval(order_expr)
        if order:
            order = order[0]
            this_wo['order'] = order
        else:
            no_send = True
        title_expr = "@SOBJECT(twog/work_order['code','%s'].twog/proj.twog/title)" % wo_code   
        title = server.eval(title_expr)
        if title:
            title = title[0]
            this_wo['title'] = title
        else:
            no_send = True
        if wo_code not in data_dict.keys() and wo_code not in [None,''] and not no_send:
            data_dict[wo_code] = this_wo 
            wos.append(wo_code)
        if no_send:
            print 'NO SEND: %s' % wo_code
    the_file.close()
    return [data_dict, wos]

def make_assignors(assignors):
    assign_chunks = assignors.split('][')
    assign_chunks[0] = assign_chunks[0][1:]
    assign_chunks[len(assign_chunks) - 1] = assign_chunks[len(assign_chunks) - 1][0:len(assign_chunks[len(assign_chunks) - 1]) - 1]
    assign_dict = {}
    for a in assign_chunks:
        chunk = {}
        group = ''
        details = a.split(',')
        for d in details:
            kv = d.split('=')
            chunk[kv[0]] = kv[1]
            if kv[0] in ['Group','group']:
                group = kv[1]

        if group not in assign_dict.keys():
            assign_dict[group] = []
        assign_dict[group].append(chunk)
    return assign_dict

if len(sys.argv) != 3:
    print len(sys.argv)
    print "python wo_completor.py wo_code_list_file '[Group=qc,Process=Spot QC,Status_from=Ready,Status=Completed,Hour_min=.25,Assign_to=luis.barajas;tiagio.jacinto;chelsea.spirito,Force_assignment=Yes][Group=machine_room,Classification=Completed,Hour_add=1]'"
    print "\nThis would only affect the work orders in the 'wo_code_list_file', and only to the work orders that fit the various assignment blocks."
    print "\nThe first assignment block would find all work orders in the list that belong to qc, have the process name of 'Spot QC' and a status of 'Ready'."
    print "Then it would check to see that these work hours have at least .25 hours added to them. If they don't, work hours will be added to the work_order, ascribing the hours to people randomly in the Assign_to list."
    print "Then, if no one is assigned to the work_order, it will also add the selected work hour person as the assigned person. If no hours were added and 'Force_assignment' is 'Yes', it will assign someone to the task, as long as no one else is currently assigned."
    print "Lastly, it will update the status to 'Completed' for the selected work orders not filtered out by the assignment."
    print "\nThe second block will simply find all work orders in the list that are in the machine_room work group, and that are under an order whose classification is 'Completed', and add 1 hour to all of them." 
else:
    opts, wo_list_file = getopt.getopt(sys.argv[1], '-m')
    print "wo_list_file = %s" % wo_list_file
    opts, assignors = getopt.getopt(sys.argv[2], '-m')
    print "assignors = %s" % assignors
    assign_dict = make_assignors(assignors)
    data_dicts = make_data_dict(wo_list_file)
    data_dict = data_dicts[0]
    wos = data_dicts[1]
    wos.sort()
    akeys = assign_dict.keys()
    break_here = []
    total_hours_added = 0.0
    total_altered_statuses = 0
    total_count = 0
    total_assignment_made = 0
    for group in akeys:
        print "GROUP: %s" % group
        group_exists = server.eval("@SOBJECT(sthpw/login_group['login_group','%s'])" % group)
        group_hours = 0.0
        altered_statuses = 0
        assignment_made = 0
        count = 0
        if group_exists:
            for assignment in assign_dict[group]:
                print "Group = %s" % group
                assign_to = []
                assign_to_count = 0
                assign_to_last = 0
                if 'Assign_to' in assignment.keys():
                    assign_tos = assignment.get('Assign_to')
                    ats = assign_tos.split(';')
                    for zat in ats:
                        login_exists = server.eval("@SOBJECT(sthpw/login['login','%s'])" % zat)
                        if login_exists:
                            assign_to_count = assign_to_count + 1
                            assign_to.append(zat)
                        else:
                            break_here.append('%s in %s is not a valid user' % (zat, assignment))
                if len(break_here) < 1:
                    for wo in wos:
                        package = data_dict[wo]
                        #print "PACKAGE = %s" % package
                        if group == package['task']['assigned_login_group']:
                            selected = True
                            if 'Process' in assignment.keys():
                                if assignment['Process'] != package['task']['process']:
                                    selected = False
                            if 'Status_from' in assignment.keys():
                                if assignment['Status_from'] != package['task']['status']:
                                    selected = False
                            if 'Classification' in assignment.keys():
                                if assignment['Classification'] != package['order']['classification']:
                                    selected = False
                            if selected:
                                #Do the stuff to the stuff
                                count = count + 1
                                check_assignment = False
                                assign_to_person = ''
                                if 'Hour_min' in assignment.keys():
                                    hour_min = float(assignment.get('Hour_min'))
                                    hours = package['work_hours']
                                    hour_count = 0.0
                                    
                                    for h in hours:
                                        hc = float(h.get('straight_time'))
                                        hour_count = hour_count + hc    
                                    hour_diff = 0
                                    if hour_count < hour_min:
                                        hour_diff = hour_min - hour_count
                                        assign_to_person = assign_to[assign_to_last]
                                        assign_to_last = assign_to_last + 1
                                        if assign_to_last == assign_to_count:
                                            assign_to_last = 0
                                    if hour_diff > 0:
                                        #server.insert('sthpw/work_hour', {'task_code': package['task']['code'], 'project_code': 'twog', 'description': 'Added with wo_completor.py', 'login': assign_to_person, 'process': package['task']['process'], 'straight_time': hour_diff, 'search_id': package['task']['id'], 'search_type': 'sthpw/task', 'is_billable': True, 'scheduler': package['order']['login'], 'client_code': package['order']['client_code'], 'client_name': package['order']['client_name'], 'order_code': package['order']['code'], 'title_code': package['title']['code']}) 
                                        group_hours = group_hours + hour_diff
                                        check_assignment = True
                                elif 'Hour_add' in assignment.keys():
                                    hour_add = float(assignment.get('Hour_add'))
                                    assign_to_person = assign_to[assign_to_last]
                                    assign_to_last = assign_to_last + 1
                                    if assign_to_last == assign_to_count:
                                        assign_to_last = 0
                                    #server.insert('sthpw/work_hour', {'task_code': package['task']['code'], 'project_code': 'twog', 'description': 'Added with wo_completor.py', 'login': assign_to_person, 'process': package['task']['process'], 'straight_time': hour_add, 'search_id': package['task']['id'], 'search_type': 'sthpw/task', 'is_billable': True, 'scheduler': package['order']['login'], 'client_code': package['order']['client_code'], 'client_name': package['order']['client_name'], 'order_code': package['order']['code'], 'title_code': package['title']['code']}) 
                                    group_hours = group_hours + hour_add
                                    check_assignment = True
                                if 'Force_assignment' in assignment.keys():
                                    if assignment.get('Force_assignment') == 'Yes':
                                        check_assignment = True
                                if check_assignment:
                                    if package['task']['assigned'] in [None,'']:
                                        #server.update(server.build_search_key('sthpw/task', package['task']['code']), {'assigned': assign_to_person})
                                        assignment_made = assignment_made + 1
                                if 'Status' in assignment.keys(): 
                                    status = assignment.get('Status')
                                    #server.update(server.build_search_key('sthpw/task', package['task']['code']), {'status': status})    
                                    altered_statuses = altered_statuses + 1
        else:
            break_here.append('%s is not a valid group' % group)

        total_assignment_made = total_assignment_made + assignment_made
        total_count = total_count + count
        total_hours_added = total_hours_added + group_hours
        total_altered_statuses = total_altered_statuses + altered_statuses
        print "%s => Count: %s, Hours: %s, Altered Statuses: %s, Assignments Made: %s" % (group, count, group_hours, altered_statuses, assignment_made)                         

    print "Total Count: %s, Total Hours: %s, Total Altered Statuses: %s, Total Assignments Made: %s" % (total_count, total_hours_added, total_altered_statuses, total_assignment_made)                         
    if len(break_here) > 0:
        for breaks in break_here:
            print "%s\n" % breaks
                                
                        


































"""
This file was generated automatically from a custom script found in Project -> Script Editor.
The custom script was moved to a file so that it could be integrated with GitHub.
"""

__author__ = 'Topher.Hughes'
__date__ = '04/08/2015'

import traceback


def main(server=None, input=None):
    """
    The main function of the custom script. The entire script was copied
    and pasted into the body of the try statement in order to add some
    error handling. It's all legacy code, so edit with caution.

    :param server: the TacticServerStub object
    :param input: a dict with data like like search_key, search_type, sobject, and update_data
    :return: None
    """
    if not input:
        input = {}

    try:
        # CUSTOM_SCRIPT00019
        #
        # Created by Matthew Misenhimer
        #
        def make_timestamp():
            #Makes a Timestamp for postgres
            import datetime
            now = datetime.datetime.now()
            return now.strftime("%Y-%m-%d %H:%M:%S")
        
        def are_no_hackpipes_preceding(sob, ignore_code):
            #Checks to see if there are any manually inserted/non-pipeline Projects or Work Orders that lead in to the sob that are not completed yet
            #If there are incompleted hackpipe work orders or projs that precede the sob, then this will return false.
            #Ignore code is usually the code of the task just completed. We don't care about looking at it's status in determining this. 
            boolio = True
            matcher = '' #This is the type of sob (PROJ or WORK_ORDER) that we care about looking at
            if 'PROJ' in sob.get('code'):
                matcher = 'PROJ'
            elif 'WORK_ORDER' in sob.get('code'):
                matcher = 'WORK_ORDER'
            pre_hacks_expr = "@SOBJECT(twog/hackpipe_out['out_to','%s'])" % sob.get('code') #See what hackpipes lead in to this sob
            pre_hacks = server.eval(pre_hacks_expr)
            for ph in pre_hacks:
                if matcher in ph.get('lookup_code') and ignore_code not in ph.get('lookup_code'): #If it's the type we care about and it isn't the main sob
                    ph_task = server.eval("@SOBJECT(sthpw/task['lookup_code','%s'])" % ph.get('lookup_code'))
                    if ph_task:
                        ph_task = ph_task[0]
                        if ph_task.get('status') != 'Completed': #If it hasn't been completed, then there is an incomplete hackpipe preceding sob, so return false
                            boolio = False
            return boolio
        
        def block_manual_status_adjust_for_inactive_hackup(sob, task):
            #This was created because people used to be able to change the status of inactive work orders
            #I think this is prevented in other ways now, but I am keeping it in just in case it is still needed.
            from pyasm.common import TacticException
            good = True
            if sob.get('creation_type') == 'hackup':
                if task.get('active') not in [True,'true','t',1,'1']:
                    raise TacticException('This needs to be active in order to change the status')
            return good
        
        from pyasm.common import TacticException, Environment
        # input and server are assumed variables
        # define some contants here
        #print "\n\nIN KICKOFF"
        COMPLETE = 'Completed'
        READY = 'Ready'
        PENDING = 'Pending'
        sobj = input.get('sobject')
        this_process = sobj.get('process')
        this_lookup = sobj.get('lookup_code')
        sk = input.get('search_key')
        task_code = sobj.get('code')
        update_data = input.get('update_data') #These are the new values
        prev_data = {}
        old_status = ''
        if 'prev_data' in input.keys():
            prev_data = input.get('prev_data') #These are the old values
            if 'status' in prev_data.keys():
                old_status = prev_data.get('status')
        new_status = update_data.get('status')
        login = Environment.get_login()
        user_name = login.get_login()
        assigned_login_group = sobj.get('assigned_login_group')
        parent_obj = None
        title = None
        order = None
        if 'PROJ' in this_lookup:
            parent_obj = server.eval("@SOBJECT(twog/proj['code','%s'])" % this_lookup)[0] #Parent Obj is the Proj attached to the task
            proj = parent_obj
            title = server.eval("@SOBJECT(twog/title['code','%s'])" % parent_obj.get('title_code'))[0]
            order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))[0] 
        elif 'WORK_ORDER' in this_lookup:
            parent_obj = server.eval("@SOBJECT(twog/work_order['code','%s'])" % this_lookup)[0] #Parent Obj is the Work Order attached to the task
            work_order = parent_obj
            proj = server.eval("@SOBJECT(twog/proj['code','%s'])" % work_order.get('proj_code'))[0]
            title = server.eval("@SOBJECT(twog/proj['code','%s'].twog/title)" % parent_obj.get('proj_code'))[0] 
            order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))[0] 
        
        if 'PROJ' in this_lookup and title.get('priority_triggers') != 'No':
            #If the new status for this Proj is ready, then grab the priority attached to he proj and give it to the Title
            #This is to control priority order per department
            if new_status == 'Ready':
                server.update(title.get('__search_key__'), {'priority': parent_obj.get('priority')}, triggers=False)
        elif 'WORK_ORDER' in this_lookup:
            t_wo_completed = title.get('wo_completed') #This is for the completion ratio on title
            o_wo_completed = order.get('wo_completed') #This is for the completion ratio on order
            if new_status == COMPLETE:
                title_str = title.get('title') #This is for a potential alert/exception
                if title.get('episode') not in [None,'']:
                    title_str = '%s: %s' % (title_str, title.get('episode'))
                #Block QC and Edel from completing their work orders if the TRT or TRT w/Textless are not filled in
                if 'qc' in assigned_login_group or 'edeliveries' in assigned_login_group:
                    total_program_runtime = title.get('total_program_runtime')
                    total_runtime_w_textless = title.get('total_runtime_w_textless')
                    say_str = ''
                    say_str2 = ''
                    if total_program_runtime in [None,''] or total_runtime_w_textless in [None,'']:
                        if total_program_runtime in [None,'']:
                            say_str = 'Total Program Runtime has' 
                        if total_runtime_w_textless in [None,'']:
                            if say_str == '': 
                                say_str = 'Total Runtime With Textless has'
                            else:
                                say_str = '%s and Total Runtime With Textless have' % (say_str[:-4])  
                        say_str2 = "%s (%s)'s %s not been filled. You must enter this data before trying to complete this work order." % (title_str, title.get('code'), say_str)
                    if 'qc' in assigned_login_group:
                        if total_program_runtime in [None,''] or total_runtime_w_textless in [None,'']:
                            raise TacticException(say_str2)
                        else:
                            #They were filled in, so finish completing the task and send a note
                            from pyasm.biz import Note
                            from pyasm.search import Search
                            title_obj2 = Search.get_by_search_key(title.get('__search_key__')) #This is the type of object required for Note creation
                            note_text = '%s (%s) has been Passed and Completed by %s in QC' % (sobj.get('process'), this_lookup, user_name)
                            note = Note.create(title_obj2, note_text, context='QC Completed', process='QC Completed')
                    elif 'edeliveries' in assigned_login_group and (total_program_runtime in [None,''] or total_runtime_w_textless in [None,'']):
                        raise TacticException(say_str2)
                #This section is turned off due to logistical problems with it. 
                #It intended to block machine room, edit, and compression from completing a work order unless the pulled_blacks had been filled out.
                #if 'machine_room' in assigned_login_group or 'edit' in assigned_login_group or 'compression' in assigned_login_group:
                #    pulled_blacks = title.get('pulled_blacks')
                #    if pulled_blacks in [None,'','0']:
                #        raise TacticException("%s (%s)'s pulled_blacks has not been filled, or is still '0'." % (title_str, title.get('code'))) 
                t_wo_completed = t_wo_completed + 1
                o_wo_completed = o_wo_completed + 1
                #Update the completion ratios attached, since there were no blocking exceptions 
                server.update(title.get('__search_key__'), {'wo_completed': t_wo_completed})
                server.update(order.get('__search_key__'), {'wo_completed': o_wo_completed})
            elif old_status == COMPLETE:
                t_wo_completed = t_wo_completed - 1
                o_wo_completed = o_wo_completed - 1
                #Reduce the completion ratio, since it was completed but has now been taken off that status
                server.update(title.get('__search_key__'), {'wo_completed': t_wo_completed})
                server.update(order.get('__search_key__'), {'wo_completed': o_wo_completed})
        #Still doing this, but don't know if it's neccessary anymore        
        mmkay = block_manual_status_adjust_for_inactive_hackup(parent_obj, sobj)
        if new_status == COMPLETE and 'PROJ' not in this_lookup:
            #Make sure they have set the assigned person to the work order.
            if sobj.get('assigned') in [None,'']:
                task_assigned_expr = "@GET(sthpw/task['code','%s'].assigned)" % sobj.get('code') #MTM: Do I need to retrieve the task again, or can I just use the sobj's "assigned"? 
                task_assigned = server.eval(task_assigned_expr)
                if task_assigned:
                    task_assigned = task_assigned[0]
                if task_assigned in [None,'']:
                    raise TacticException('Before completing a work order, someone must be assigned to it.')
            #Make sure they have added work hours. If not, error out.
            whs_expr = "@SOBJECT(sthpw/work_hour['task_code','%s'])" % task_code
            whs = server.eval(whs_expr)
            sum = 0
            for wh in whs:
                straight_time = wh.get('straight_time')
                if straight_time in [None,'']:
                    straight_time = 0
                else:
                    straight_time = float(straight_time)
                sum = float(sum) + straight_time
                sum = str(sum)
            if sum in ['0','',0,0.0]:
                raise TacticException('You need to save the hours you worked on this before you can set the status to "Completed".')
        
        now_timestamp = make_timestamp() 
        #Since there have been no blocking exceptions, record the status change
        server.insert('twog/status_log', {'login': user_name, 'timestamp': now_timestamp, 'from_status': old_status, 'status': new_status, 'task_code': task_code, 'lookup_code': this_lookup, 'order_code': sobj.get('order_code'), 'title_code': sobj.get('title_code'), 'process': this_process})
        if new_status == COMPLETE:
            #Record the completion date on the work order, and take it off the BigBoard
            import datetime
            now = datetime.datetime.now()
            timestamp_str = '%s-%s-%s %s:%s:%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
            updict = {'actual_end_date': timestamp_str}
            if 'WORK_ORDER' in this_lookup:
                updict['bigboard'] = False
            server.update(sk, updict)
        elif new_status not in ['Pending','Ready','Completed'] and 'WORK_ORDER' in this_lookup:
            server.update(server.build_search_key('sthpw/task', proj.get('task_code')), {'status': new_status})        #NEW
        if 'PROJ' in sobj.get('lookup_code'):
            #MTM: This annoying section is for passing Proj's their task's status.
            #I don't know if this is needed at all anymore. Will have to check other triggers and reports.
            #The "tripwire" stuff was just to keep it from infinitely passing statuses from proj to task, task to proj
            do_it = True
            if 'tripwire' in update_data.keys():
                if update_data.get('tripwire') == 'No Send Back': #?
                    do_it = False
                    server.update(input.get('search_key'), {'tripwire': ''}, triggers=False) #Empty the tripwire and do nothing
                    server.update(proj.get('__search_key__'), {'tripwire': '', 'status': sobj.get('status')}, triggers=False) #?
            if do_it:
                if proj:
                    server.update(proj.get('__search_key__'), {'status': new_status})
        if title.get('priority_triggers') != 'No':
            #Update Title Priority for On Hold Status, or having that status removed -- BEGIN
            if sobj.get('status') in ['On_Hold','On Hold']:
                title_priority = title.get('priority')
                server.update(title.get('__search_key__'), {'saved_priority': title_priority, 'priority': 200}, triggers=False)    
            else:
                if old_status in ['On_Hold','On Hold']:
                    saved_priority = title.get('saved_priority')
                    server.update(title.get('__search_key__'), {'priority': saved_priority}, triggers=False)    
            #Update Title Priority for On Hold Status, or having that status removed -- END
        
            #Update Title Priority for Client Response Status, or having that status removed -- BEGIN
            if sobj.get('status') == 'Client Response':
                title_priority = title.get('priority')
                crc = title.get('client_response_count')
                crc_num = 0
                if crc not in [None,'']:
                    crc_num = int(crc)
                crc_num = crc_num + 1        
                server.update(title.get('__search_key__'), {'saved_priority': title_priority, 'priority': 300, 'client_response_count': crc_num}, triggers=False)    
            else:
                if old_status == 'Client Response':
                    saved_priority = title.get('saved_priority')
                    crc = title.get('client_response_count')
                    crc_num = 0
                    if crc not in [None,'']:
                        crc_num = int(crc)
                    if crc_num > 0:
                        crc_num = crc_num - 1        
                    server.update(title.get('__search_key__'), {'priority': saved_priority, 'client_response_count': crc_num}, triggers=False)    
            #Update Title Priority for Client Response Status, or having that status removed -- END
                 
        if sobj.get('status') in ['In_Progress','In Progress','DR In_Progress','DR In Progress', 'Amberfin01_In_Progress', 'Amberfin01 In Progress', 'Amberfin02_In_Progress', 'Amberfin02 In Progress','BATON In_Progress','BATON In Progress','Export In_Progress','Export In Progress','Buddy Check In_Progress','Buddy Check In Progress','Need Buddy Check','Completed'] and old_status not in ['In_Progress','DR In_Progress','DR In Progress','Amberfin01_In_Progress','Amberfin01 In Progress', 'Amberfin02_In_Progress','Amberfin02 In Progress','BATON In_Progress','BATON In Progress','Export In_Progress','Export In Progress','Buddy Check In_Progress','Buddy Check In Progress','Need Buddy Check','In Progress']:
            #Update the actual start date if they just set the status to 'In Progress'
            if sobj.get('actual_start_date') in ['',None]:
                now_timestamp = make_timestamp() 
                server.update(sk, {'actual_start_date': now_timestamp})
        if sobj.get('status') in ['Ready','In_Progress','In Progress'] and 'WORK_ORDER' in sobj.get('lookup_code'):
            if title.get('client_status') != 'In Production':
                server.update(title.get('__search_key__'), {'client_status': 'In Production', 'status': 'In Production'})
        elif sobj.get('status') in ['Rejected','Fix Needed'] and 'WORK_ORDER' in sobj.get('lookup_code'):
            from pyasm.biz import Note
            from pyasm.search import Search
            server.insert('twog/production_error', {'error_type': sobj.get('status'), 'process': sobj.get('process'), 'work_order_code': sobj.get('lookup_code'), 'title': title.get('title'), 'episode': title.get('episode'), 'title_code': title.get('code'), 'order_code': order.get('code'), 'order_name': order.get('name'), 'po_number': order.get('po_number'), 'proj_code': proj.get('code'), 'scheduler_login': sobj.get('creator_login'), 'operator_login': user_name, 'login': user_name}) 
            if sobj.get('status') == 'Rejected':
                server.update(title.get('__search_key__'), {'client_status': 'QC Rejected'})
                if title.get('priority_triggers') != 'No':
                    server.update(title.get('__search_key__'), {'priority': 90}, triggers=False)
                title_obj2 = Search.get_by_search_key(title.get('__search_key__'))   #This is the type of object required for Note creation
                note_text = '%s (%s) has been Rejected, as marked by %s' % (sobj.get('process'), this_lookup, user_name)
                note = Note.create(title_obj2, note_text, context='QC Rejected', process='QC Rejected')
        
        if sobj.get('status') == COMPLETE and title.get('status_triggers') != 'No':
            # Now we need to set the next task(s) statuses to 'Ready'
            parent = server.get_parent(sk)
            # Get all process information from the pipeline regarding processes linked to this process in the normal pipeline
            info = server.get_pipeline_processes_info(parent.get('__search_key__'), related_process=this_process)
            input_processes = info.get('input_processes')
            output_processes = info.get('output_processes')
            # this combines all other input_processes and this process
            # including this_process in case this process has more than 1 task
            ready = False
            if input_processes:
                input_processes.append(this_process)
                ready = True
                input_tasks = server.query('sthpw/task', filters = [('search_type', sobj.get('search_type')), ('search_id', sobj.get('search_id')), ('process', input_processes), ('title_code',sobj.get('title_code'))])
                for task in input_tasks:
                    if task.get('status') != COMPLETE:
                        ready = False
            else:
                ready = True
            #Now we need to check the manually entered work orders and projs 
            #This section may be replaced with the are_no_hackpipes_preceding function, but for the sake of stability, I won't do it until I test it again
            hack_outs_expr = "@SOBJECT(twog/hackpipe_out['out_to','%s'])" % sobj.get('lookup_code')
            hack_outs = server.eval(hack_outs_expr)
            stype = ''
            stype_st = ''
            if 'PROJ' in sobj.get('lookup_code'):
                stype = 'PROJ'
                stype_st = 'twog/proj'
            elif 'WORK_ORDER' in sobj.get('lookup_code'):
                stype = 'WORK_ORDER'
                stype_st = 'twog/work_order'
            for ho in hack_outs:
                lookup_code = ho.get('lookup_code')
                if stype in lookup_code:
                    hacktasks = server.eval("@SOBJECT(sthpw/task['lookup_code','%s'])" % lookup_code)
                    for hacktask in hacktasks:
                        if hacktask.get('status') != COMPLETE:
                            ready = False
               
            # make the next process ready
            if ready == True:
                output_tasks = server.query('sthpw/task', filters = [('search_type', sobj.get('search_type')), ('search_id', sobj.get('search_id')), ('process', output_processes), ('title_code',sobj.get('title_code'))])
                update_data = {}
           
                for task in output_tasks:
                    if task.get('lookup_code') not in [None,'']:
                        if task.get('status') == 'Pending':
                            #Need to make sure other tasks leading into this one (an output task for the triggered task) are also complete - both ways, with pipeline and hackpipe - before allowing this status update 
                            
                            out_info = server.get_pipeline_processes_info(parent.get('__search_key__'), related_process=task.get('process'))
                            input_to_out = out_info.get('input_processes') 
                            if this_process in input_to_out:
                               prc_idx = input_to_out.index(this_process)
                               input_to_out.pop(prc_idx)
                            ready2 = False
                            if input_to_out:
                                #input_to_out.append(task.get('process'))
                                ts_st = ''
                                if 'PROJ' in task.get('lookup_code'):
                                    ts_st = 'twog/proj'
                                elif 'WORK_ORDER' in task.get('lookup_code'):
                                    ts_st = 'twog/work_order'
                                tsob = server.eval("@SOBJECT(%s['code','%s'])" % (ts_st, task.get('lookup_code')))[0] 
                                ready2 = are_no_hackpipes_preceding(tsob, sobj.get('lookup_code'))
                                into_out_tasks = server.query('sthpw/task', filters = [('search_type', task.get('search_type')), ('search_id', task.get('search_id')), ('process', input_to_out)])
                                for iotask in into_out_tasks:
                                    # If preceding tasks have not yet been set to 'Completed', do not change the next task's status
                                    if iotask.get('status') != COMPLETE:
                                        ready2 = False
                            else:
                                ready2 = True
                            hacks_expr = "@SOBJECT(twog/hackpipe_out['out_to','%s'])" % task.get('lookup_code')
                            hacks = server.eval(hacks_expr)
                            for hack in hacks:
                                lu_code = hack.get('lookup_code') 
                                hacktasks = server.eval("@SOBJECT(sthpw/task['lookup_code','%s'])" % lu_code)
                                for hacktask in hacktasks:
                                    if hacktask.get('status') != COMPLETE:
                                        ready2 = False
                            if ready2 == True:
                                update_data[task.get('__search_key__')] = { 'status': READY }
                                if 'PROJ' in task.get('lookup_code'):
                                    get_proj_expr = "@SOBJECT(twog/proj['code','%s'])" % task.get('lookup_code')
                                    proj = server.eval(get_proj_expr)[0]
                                    # FIND ALL NON HACK WOS
                                    wos = server.eval("@SOBJECT(twog/work_order['proj_code','%s'])" % proj.get('code'))
                                    for wo in wos: 
                                        if wo.get('creation_type') not in ['hackpipe','hackup']:
                                            this_processer = wo.get('process')
                                            info2 = server.get_pipeline_processes_info(proj.get('__search_key__'), related_process=this_processer)
                                            input_processes2 = info2.get('input_processes')
                                            okayed = are_no_hackpipes_preceding(wo, sobj.get('lookup_code'))
                                            len_proc = 0
                                            if input_processes2 not in ['',{},[],None]:
                                                len_proc = len(input_processes2)
                                            if len_proc < 1 and okayed:
                                                task2 = server.eval("@SOBJECT(sthpw/task['code','%s'])" % wo.get('task_code')) 
                                                if task2:
                                                    task2 = task2[0]
                                                    if task2.get('status') == 'Pending':
                                                        server.update(task2.get('__search_key__'), {'status': READY}) #?
                                    # FIND ALL HACK WOS HERE.........
                                    hack_dudes = server.eval("@SOBJECT(twog/hackpipe_out['lookup_code','%s'])" % proj.get('code'))
                                    for ho in hack_dudes:
                                        ready3 = True
                                        out_to = ho.get('out_to')
                                        label = ''
                                        if 'PROJ' in out_to:
                                            label = 'twog/proj'
                                        elif 'WORK_ORDER' in out_to:
                                            label = 'twog/work_order'
                                        sob_guy = server.eval("@SOBJECT(%s['code','%s'])" % (label, out_to))
                                        for sobby in sob_guy:
                                            ready3 = are_no_hackpipes_preceding(sobby, sobj.get('lookup_code'))
                                        if ready3:
                                            htask = server.eval("@SOBJECT(sthpw/task['lookup_code','%s'])" % out_to)
                                            if htask:
                                                htask = htask[0]
                                                if htask.get('status') == 'Pending':
                                                    server.update(htask.get('__search_key__'), {'status': READY})
                                    
                hackers = server.eval("@SOBJECT(twog/hackpipe_out['lookup_code','%s'])" % sobj.get('lookup_code'))
                for hack in hackers:
                    if stype in hack.get('out_to'):
                        out_to = hack.get('out_to')
                        out_sob = server.eval("@SOBJECT(%s['code','%s'])" % (stype_st, out_to))
                        if out_sob:
                            out_sob = out_sob[0] 
                            ready4 = are_no_hackpipes_preceding(out_sob, sobj.get('lookup_code'))
                            if ready4:
                                tasker = server.eval("@SOBJECT(sthpw/task['code','%s'])" % out_sob.get('task_code'))
                                if tasker:
                                    tasker = tasker[0]
                                    if tasker.get('status') == 'Pending':
                                        server.update(tasker.get('__search_key__'), {'status': READY})
                                        if stype == 'PROJ':
                                            # Need to do the same thing here, looking at pipeline and hackpipe
                                            hack_wos = server.eval("@SOBJECT(twog/hackpipe_out['lookup_code','%s'])" % out_to)
                                            for hos in hack_wos:
                                                if 'PROJ' not in hos.get('out_to'):
                                                    ho_wo = server.eval("@SOBJECT(twog/work_order['code','%s'])" % hos.get('out_to'))
                                                    if ho_wo:
                                                        ho_wo = ho_wo[0]
                                                        ready5 = are_no_hackpipes_preceding(ho_wo, out_sob.get('code'))
                                                        if ready5:
                                                            ho_wo_task_sk = server.build_search_key('sthpw/task', ho_wo.get('task_code'))
                                                            #7/10/2014 --- WAIT. WTF. THERE IS NO STATUS ON WOS, JUST THE TASK..... MTMMTMMTM!!!
                                                            if ho_wo.get('status') == 'Pending':
                                                                server.update(ho_wo_task_sk, {'status': READY})
                                            # NEED TO LOOK AT PROJ PIPELINE NOW
                                            proj_sk = server.build_search_key('twog/proj', out_to)
                                            pipe_wos = server.eval("@SOBJECT(twog/work_order['proj_code','%s'])" % out_to)
                                            for pwos in pipe_wos:
                                                if pwos.get('creation_type') not in ['hackpipe','hackup']:
                                                    info2 = server.get_pipeline_processes_info(proj_sk, related_process=pwos.get('process'))
                                                    if 'input_processes' in info2.keys():
                                                        input_processes2 = info2.get('input_processes')
                                                        whack_says = are_no_hackpipes_preceding(pwos, out_to)
                                                        # If there are no input processes, it must be a work order that should also be set to ready - as long as hackpipe says it's ok
                                                        len_proc2 = 0
                                                        if input_processes2 not in ['',{},[],None]:
                                                            len_proc2 = len(input_processes2)
                                                        if len_proc2 < 1 and whack_says:
                                                            wtask_code = pwos.get('task_code')
                                                            # Get the task sobject associated with this work order
                                                            wtask = server.eval("@SOBJECT(sthpw/task['code','%s'])" % wtask_code)
                                                            if wtask:
                                                                wtask = wtask[0]
                                                                # If the task's status has not been touched yet ('Pending') and active is set to true, update the status with 'Ready'
                                                                if wtask.get('status') == 'Pending':
                                                                    wdata = {}
                                                                    wdata['status'] = 'Ready'
                                                                    if wtask.get('status') == 'Pending':
                                                                        server.update(wtask.get('__search_key__'), wdata)
                                                
                            
                          
                #
                # HERE NEED TO FIND ANY OTHER TASKS THIS GOES 'OUT_TO' and make sure they don't also depend on another task's status (if so, make sure it is completed)
                #
                        
                # this is optional, for simplicity, turn off triggers for these updates
                if update_data != {} and title.get('priority_triggers') != 'No':
                    #make title priority the proj priority, if proj is becoming "Ready"
                    for tkey in update_data.keys():
                        record = update_data.get(tkey)
                        tkcode = tkey.split('code=')[1]
                        if 'status' in record.keys():
                            if record.get('status') == 'Ready':
                                ttt = server.eval("@GET(sthpw/task['code','%s'].lookup_code)" % tkcode)[0]
                                if 'PROJ' in ttt:
                                    pjj = server.eval("@SOBJECT(twog/proj['code','%s'])" % ttt)[0]
                                    proj_title_code = pjj.get('title_code')
                                    proj_prio = pjj.get('priority')
                                    server.update(server.build_search_key('twog/title',proj_title_code), {'priority': proj_prio}, triggers=False)
                    server.update_multiple(update_data, triggers=False) #? Should triggers=False?
            
        
        # Now see if all wos under proj or all projs under title are completed. If so, make their parent's status completed
        all_wos_completed = False
        all_wos_pending = False
        prj = None
        if new_status in [COMPLETE,PENDING]: 
            if 'WORK_ORDER' in this_lookup:
                wo = server.eval("@SOBJECT(twog/work_order['code','%s'])" % sobj.get('lookup_code'))
                wo = wo[0]
                other_wotasks_expr = "@SOBJECT(twog/proj['code','%s'].twog/work_order.WT:sthpw/task)" % wo.get('proj_code')
                other_wo_tasks = server.eval(other_wotasks_expr)
                all_wos_completed = True
                all_wos_pending = True
                if new_status == PENDING:
                    all_wos_completed = False
                else:
                    all_wos_pending = False
                for owt in other_wo_tasks:
                    if owt.get('lookup_code') != wo.get('code'):
                        if owt.get('status') != COMPLETE:
                            all_wos_completed = False
                        if owt.get('status') != PENDING:
                            all_wos_pending = False
                prj = server.eval("@SOBJECT(twog/proj['code','%s'])" % wo.get('proj_code'))
                if len(prj) > 0:
                    prj = prj[0]
                else:
                    prj = None
                if (all_wos_completed or all_wos_pending) and prj not in [None,'']:
                    if title.get('status_triggers') != 'No' or all_wos_pending == True:
                        prj_task = server.eval("@SOBJECT(sthpw/task['lookup_code','%s'])" % prj.get('code'))
                        if prj_task:
                            prj_task = prj_task[0]
                            server.update(prj_task.get('__search_key__'), {'status': new_status})
            elif 'PROJ' in this_lookup:
                prj = server.eval("@SOBJECT(twog/proj['code','%s'])" % this_lookup)
                if prj:
                    prj = prj[0]
                else:
                    prj = None
        
            all_projs_completed = True
            all_projs_pending = True
            all_titles_completed = False
            all_titles_pending = False
            if prj not in [None,'']:
                title_proj_tasks = server.eval("@SOBJECT(twog/title['code','%s'].twog/proj.PT:sthpw/task)" % prj.get('title_code'))
                for tpt in title_proj_tasks:
                    if tpt.get('status') != COMPLETE:
                        all_projs_completed = False
                    if tpt.get('status') != PENDING:
                        all_projs_pending = False
                title_updated = False
                if all_projs_completed:
                    title_sk = server.build_search_key('twog/title', prj.get('title_code'))
                    if title.get('priority_triggers') != 'No' and title.get('status_triggers') != 'No':
                        server.update(title_sk, {'status': COMPLETE, 'bigboard': False, 'priority': 5000})
                        titles_completed = order.get('titles_completed')
                        title_codes_completed = order.get('title_codes_completed')
                        if title.get('code') not in title_codes_completed:
                            if titles_completed in [None,'']:
                                titles_completed = 0
                            else:
                                titles_completed = int(titles_completed)
                            titles_completed = titles_completed + 1
                            if title_codes_completed == '':
                                title_codes_completed = title.get('code')
                            else:
                                title_codes_completed = '%s,%s' % (title_codes_completed, title.get('code'))
                            server.update(order.get('__search_key__'), {'titles_completed': titles_completed, 'title_codes_completed': title_codes_completed}) 
                        title_updated = True
                    all_titles_completed = True
                    title = server.eval("@SOBJECT(twog/title['code','%s'])" % prj.get('title_code'))
                    if title and title_updated:
                        title = title[0]
                        other_titles = server.eval("@SOBJECT(twog/order['code','%s'].twog/title)" % title.get('order_code'))
                        for ot in other_titles:
                            if title.get('code') != ot.get('code'):
                                if ot.get('status') != COMPLETE:
                                    all_titles_completed = False
                    else:
                        all_titles_completed = False
                if all_projs_pending:
                    title_sk = server.build_search_key('twog/title', prj.get('title_code'))
                    if title.get('priority_triggers') != 'No' and title.get('status_triggers') != 'No':
                        server.update(title_sk, {'status': '', 'bigboard': False})
                        title_codes_completed = order.get('title_codes_completed')
                        if title.get('code') in title_codes_completed:
                            title_codes_completed = title_codes_completed.replace(',%s'  % title.get('code'),'').replace('%s,'  % title.get('code'),'').replace('%s'  % title.get('code'),'')
                            titles_completed = order.get('titles_completed')
                            if titles_completed in [None,'']:
                                titles_completed = 0
                            else:
                                titles_completed = int(titles_completed) - 1
                            server.update(order.get('__search_key__'), {'titles_completed': titles_completed, 'title_codes_completed': title_codes_completed})
                        title_updated = True
                    all_titles_pending = True
                    title = server.eval("@SOBJECT(twog/title['code','%s'])" % prj.get('title_code'))
                    if title and title_updated:
                        title = title[0]
                        other_titles = server.eval("@SOBJECT(twog/order['code','%s'].twog/title)" % title.get('order_code'))
                        for ot in other_titles:
                            if title.get('code') != ot.get('code'):
                                if ot.get('status') != '':
                                    all_titles_pending = False
                    else:
                        all_titles_pending = False
            if all_titles_pending:
                server.update(server.build_search_key('twog/order', title.get('order_code')), {'needs_completion_review': False}) 
            if all_titles_completed:
                server.update(server.build_search_key('twog/order', title.get('order_code')), {'needs_completion_review': True}) 
                    
        #print "LEAVING KICKOFF"
    except AttributeError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the server object does not exist.'
        raise e
    except KeyError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the input dictionary does not exist.'
        raise e
    except Exception as e:
        traceback.print_exc()
        print str(e)
        raise e


if __name__ == '__main__':
    main()

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
        # CUSTOM_SCRIPT00020
        def make_timestamp():
            import datetime
            now = datetime.datetime.now()
            return now.strftime("%Y-%m-%d %H:%M:%S")
        
        def are_no_hackpipes_preceding(sob):
            boolio = True
            matcher = ''
            if 'PROJ' in sob.get('code'):
                matcher = 'PROJ'
            elif 'WORK_ORDER' in sob.get('code'):
                matcher = 'WORK_ORDER'
            pre_hacks_expr = "@SOBJECT(twog/hackpipe_out['out_to','%s'])" % sob.get('code')
            pre_hacks = server.eval(pre_hacks_expr)
            for ph in pre_hacks:
                if matcher in ph.get('lookup_code'):
                    ph_task = server.eval("@SOBJECT(sthpw/task['lookup_code','%s'])" % ph.get('lookup_code'))
                    if ph_task:
                        ph_task = ph_task[0]
                        if ph_task.get('status') != 'Completed':
                            boolio = False
            return boolio
        
        def do_wo_loop(proj, bool):
            # Get all work orders under the proj so we can determine which one of them should be turned on (set to ready)
            wos = server.eval("@SOBJECT(twog/work_order['proj_code','%s'])" % proj.get('code'))
            updated_wo_count = 0
            for wo in wos:
                if wo.get('creation_type') not in ['hackpipe','hackup']:
                    # Get the process information surrounding this wo's process from the project's pipeline
                    info2 = server.get_pipeline_processes_info(proj.get('__search_key__'), related_process=wo.get('process'))
                    if 'input_processes' in info2.keys():
                        input_processes2 = info2.get('input_processes', [])
                        # WHACKER
                        whack_says = are_no_hackpipes_preceding(wo)
                        # END WHACKER
                        # If there are no input_processes, this must be one of the work orders to set to ready (unless hackpipe says otherwise)
                        if len(input_processes2) < 1 and whack_says:
                            wtask_code = wo.get('task_code')
                            # Get the task associated with the work order
                            wtask = server.eval("@SOBJECT(sthpw/task['code','%s'])" % wtask_code)
                            if wtask:
                                wtask = wtask[0]
                                wdata = {'active': bool}
                                # If the task has not been raised above 'Pending' yet, and if active should be true, update the status to 'Ready'
                                if wtask.get('status') == 'Pending' and bool:
                                    wdata['status'] = 'Ready'
                                server.update(wtask.get('__search_key__'), wdata, triggers=False)
                                updated_wo_count = updated_wo_count + 1
            # Get all the hack work orders stemming directly off of the proj
            hwos_expr = "@SOBJECT(twog/hackpipe_out['lookup_code','%s'])" % proj.get('code')
            hack_wos = server.eval(hwos_expr)
            for how in hack_wos:
                #If this is a work order, continue. If not, don't
                if 'WORK' in how.get('out_to'):
                    wo = server.eval("@SOBJECT(twog/work_order['code','%s'])" % how.get('out_to'))
                    if wo:
                        wo = wo[0]
                        wtask = server.eval("@SOBJECT(sthpw/task['code','%s'])" % wo.get('task_code'))
                        if wtask:
                            wtask = wtask[0]  
                            wdata = {'active': bool}
                            if wtask.get('status') == 'Pending' and bool:
                                wdata['status'] = 'Ready'
                            server.update(wtask.get('__search_key__'), wdata, triggers=False)
                            updated_wo_count = updated_wo_count + 1
            if updated_wo_count == 0:
                wo_dict = {}
                for wo in wos:
                    if wo.get('creation_type') not in ['hackpipe','hackup']:
                        info = server.get_pipeline_processes_info(server.build_search_key('twog/proj', proj.get('code')), related_process=wo.get('process'))
                        input_processes = info.get('input_processes')
                        if wo.get('code') not in wo_dict.keys():
                            wo_dict[wo.get('code')] = 0
                        for in_p in input_processes:
                            wo_alive_expr = "@SOBJECT(twog/work_order['proj_code','%s']['process','%s'])" % (proj.get('code'), in_p)
                            wo_alive = server.eval(wo_alive_expr)
                            wo_dict[wo.get('code')] = wo_dict[wo.get('code')] + len(wo_alive)
                for pd in wo_dict.keys():
                    if wo_dict[pd] == 0:
                        wtask = server.eval("@SOBJECT(sthpw/task['lookup_code','%s']['status','Pending'])" % pd)
                        if wtask:
                            wtask = wtask[0]
                            server.update(wtask.get('__search_key__'), {'status': 'Ready'}, triggers=False)
        
        def loop_innerds(proj, hack, bool):
            got_one = False
            # Get the object representing the proj's title
            parent = server.get_parent(proj.get('__search_key__'))
            # Get the pipeline information about which processes lead into and out of the proj process
            input_processes = []
            if not hack:
                info = server.get_pipeline_processes_info(parent.get('__search_key__'), related_process=proj.get('process'))
                input_processes = info.get('input_processes', [])
                output_processes = info.get('output_processes')
            else:
                hack_rez = are_no_hackpipes_preceding(proj)
                if not hack_rez:
                    input_processes.append("TRIPWIRE")
            # If there are no input processes for this, it must be one of the proj's that should be set to 'Ready' (but we'll need to check hackpipe first)
            if len(input_processes) < 1:
                ptask_code = proj.get('task_code')
                # Get the actual task associated with the proj
                ptask = server.eval("@SOBJECT(sthpw/task['code','%s'])" % ptask_code)
                if ptask:
                    ptask = ptask[0]
                    # We'll be setting active to on or off anyway...
                    pdata = {'active': bool}
                    # PHACKER
                    phack_says = are_no_hackpipes_preceding(proj)
                    # END PHACKER
                    if ptask.get('status') == 'Pending' and bool and phack_says:
                        pdata['status'] = 'Ready'
                        got_one = True
                        server.update(ptask.get('__search_key__'), pdata, triggers=False)
                        do_wo_loop(proj, bool)
            return got_one
        
        from pyasm.common import TacticException 
        from pyasm.common import SPTDate
        #print "IN SET TASKS ACTIVE TRUE"
        update_data = input.get('update_data')
        prev_data = input.get('prev_data')
        old_classification = prev_data.get('classification')
        classification = update_data.get('classification')
        sob = input.get('sobject')
        sob_code = sob.get('code')
        bool = False
        errors_bool = False
        error_count = {}
        order_sk = ''
        titles = []
        # Need to disallow going to 'completed' from anything other than 'in_production'
        if classification in ['completed','Completed'] and old_classification not in ['in_production','In Production']:
            raise TacticException("You can only select 'Completed' if your order's current classification is 'in_production'.")
        elif classification in ['completed','Completed'] and old_classification in ['in_production','In Production']:
            server.update(input.get('search_key'), {'completion_date': SPTDate.convert_to_local(make_timestamp()), 'needs_completion_review': False})
        # Need to force the order checker to check if going into in_production from anything other than 'completed'  
        if classification in ['in_production','In Production']:
            bool = True 
            wo_under = server.eval("@GET(twog/title['order_code','%s'].twog/proj.twog/work_order.code)" % sob_code)
            if len(wo_under) < 1:
                raise TacticException("You have to build your order before you can put it into production.") 
            #elif sob.get('imdb_url') in [None,'']:
            #    raise TacticException("You have to associate the Order with an IMDb entry before you can put it into production.") 
            else:
                order_sk = server.build_search_key('twog/order', sob_code)
                titles = server.eval("@SOBJECT(twog/title['order_code','%s'])" % sob_code)
                total_order_wos = 0
                total_order_completed = 0
                for title in titles:
                    title_code = title.get('code')
                    tasks_total = server.eval("@COUNT(sthpw/task['title_code','%s']['lookup_code','~','WORK_ORDER'])" % title_code) 
                    tasks_completed = server.eval("@COUNT(sthpw/task['title_code','%s']['lookup_code','~','WORK_ORDER']['status','Completed'])" % title_code) 
                    if tasks_total in ['',None]:
                        tasks_total = 0
                    if tasks_completed in ['',None]:
                        tasks_completed = 0
                    server.update(title.get('__search_key__'), {'wo_count': tasks_total, 'wo_completed': tasks_completed})
                    total_order_wos = total_order_wos + tasks_total
                    total_order_completed = total_order_completed + tasks_completed
                server.update(order_sk, {'wo_count': total_order_wos, 'wo_completed': total_order_completed})
         
            if old_classification not in ['completed','Completed']:
                from order_builder import OrderCheckerWdg
                ocw = OrderCheckerWdg(sk=input.get('search_key'))
                error_count = ocw.return_error_count_dict()
                if error_count['Critical'] > 0:
                    errors_bool = True
        #GET ALL TITLE CODES ATTACHED THE THE SOBJ (The Order)
        title_codes = server.eval("@GET(twog/title['order_code','%s'].code)" % sob_code)
        if bool and not errors_bool:
            for tcode in title_codes:
                # Get all projs attached to each title
                projs_expr = "@SOBJECT(twog/proj['title_code','%s'])" % tcode
                projs = server.eval(projs_expr)
                good_projs = 0
                for proj in projs:
                    got_one = False
                    if proj.get('creation_type') not in ['hackpipe','hackup']:
                        got_one = loop_innerds(proj, False, bool)
                    else:
                        got_one = loop_innerds(proj, True, bool)
                    if got_one:
                        good_projs = good_projs + 1
                if good_projs == 0:
                    proj_dict = {}
                    for proj in projs:
                        if proj.get('creation_type') not in ['hackpipe','hackup']:
                            info = server.get_pipeline_processes_info(server.build_search_key('twog/title', tcode), related_process=proj.get('process'))
                            input_processes = info.get('input_processes')
                            if proj.get('code') not in proj_dict.keys():
                                proj_dict[proj.get('code')] = 0
                            for in_p in input_processes:
                                proj_alive_expr = "@SOBJECT(twog/proj['title_code','%s']['process','%s'])" % (tcode, in_p)
                                proj_alive = server.eval(proj_alive_expr)
                                proj_dict[proj.get('code')] = proj_dict[proj.get('code')] + len(proj_alive)
                    for pd in proj_dict.keys():
                        if proj_dict[pd] == 0:
                            ptask = server.eval("@SOBJECT(sthpw/task['lookup_code','%s']['status','Pending'])" % pd)
                            if ptask:
                                ptask = ptask[0]
                                server.update(ptask.get('__search_key__'), {'status': 'Ready'}, triggers=False)
                                for proj in projs:
                                    if proj.get('code') == ptask.get('lookup_code'):
                                        do_wo_loop(proj, bool)
                             
                    
        
        if errors_bool:
            raise TacticException('You still have %s critical errors with your order. You may put this into production once you fix the errors.' % error_count['Critical'])
        else:
            # now make sure that all tasks under this order are set to active or off active
            for tcode in title_codes:
                projs = server.eval("@SOBJECT(twog/proj['title_code','%s'])" % tcode)
                for proj in projs:
                    ptask = server.eval("@SOBJECT(sthpw/task['code','%s'])" % proj.get('task_code'))
                    if ptask:
                        ptask = ptask[0]
                        server.update(ptask.get('__search_key__'), {'active': bool}, triggers=False)
                    wos = server.eval("@SOBJECT(twog/work_order['proj_code','%s'])" % proj.get('code'))
                    for wo in wos:
                        wtask = server.eval("@SOBJECT(sthpw/task['code','%s'])" % wo.get('task_code'))
                        if wtask:
                            wtask = wtask[0]
                            server.update(wtask.get('__search_key__'), {'active': bool}, triggers=False)
            if classification in ['in_production','In Production']:
                from pyasm.common import Environment
                from cost_builder.cost_calculator import CostCalculator
                login = Environment.get_login()
                user = login.get_login()
                ccw = CostCalculator(order_code=sob_code,user=user) 
                cost_arr = ccw.update_costs()
                # Update actual start dates for the order and titles
                server.update(order_sk, {'actual_start_date': SPTDate.convert_to_local(make_timestamp())})
                for title in titles:
                    server.update(title.get('__search_key__'), {'actual_start_date': SPTDate.convert_to_local(make_timestamp())})
            
                                         
                
        #print "LEAVING SET TASKS ACTIVE TRUE"
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

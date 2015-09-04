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
        # CUSTOM_SCRIPT00009
        # THIS IS MAKE_KIDS_MATCH_PIPE2
        from pyasm.common import Environment
        from pyasm.common import SPTDate
        login = Environment.get_login()
        user_name = login.get_login()
        sk = input.get('search_key')
        st = sk.split('?')[0]
        st2 = '%s?project=twog' % st
        sobb = input.get('sobject')
        new_pipe = sobb.get('pipeline_code')
        sob_code = sobb.get('code')
        order_code = sobb.get('order_code')
        pipe_create_method = sobb.get('pipe_create_method')
        the_order = server.eval("@SOBJECT(twog/order['code','%s'])" % order_code)[0]
        client_code = ''
        client_name = ''
        title_code = ''
        client = server.eval("@SOBJECT(twog/client['code','%s'])" % the_order.get('client_code'))
        client_hold_str = 'no problems'
        if client:
            client = client[0]
            client_code = client.get('code')
            client_name = client.get('name')
            client_hold = client.get('billing_status')
            if 'Do Not Ship' in client_hold:
                client_hold_str = 'noship'
            elif 'Do Not Book' in client_hold:
                client_hold_str = 'nobook'
            
        if st == 'twog/title':
            title_code = sobb.get('code')
        elif st == 'twog/proj':
            title_code = sobb.get('title_code')
        sob_id = sobb.get('id')
        my_id = sob_id
        deps = {}
        saved_task_info = {}
        found = []
        is_master = False
        if st in ['twog/title','twog/proj']:
            if sobb.get('trigger_me') == 'pipe_update':
                if st == 'twog/proj':
                    parent_expr = "@SOBJECT(twog/title['code','%s'])" % sobb.get('title_code')
                    poss_parents = server.eval(parent_expr)
                    if poss_parents:
                        par = poss_parents[0]
                        client_pipe_expr = "@SOBJECT(twog/client_pipes['pipeline_code','%s']['process_name','%s'])" % (par.get('pipeline_code'),sobb.get('process'))
                        client_pipes = server.eval(client_pipe_expr)
                        order = server.eval("@SOBJECT(twog/order['code','%s'])" % par.get('order_code'))[0]
                        order_classification = order.get("classification")
                        if order_classification in ['master','Master']:
                            is_master = True
                        if is_master:
                            if client_pipes:
                                client_pipe = client_pipes[0]
                                server.update(client_pipe.get('__search_key__'), {'pipe_to_assign': new_pipe})
                            else:
                                server.insert('twog/client_pipes',{'pipeline_code': par.get('pipeline_code'), 'client_code': par.get('client_code'), 'process_name': sobb.get('process'), 'pipe_to_assign': new_pipe})  
        
                spt_processes = server.eval("@SOBJECT(config/process['pipeline_code','%s'])"%(new_pipe))
                kids_expr = ''
                kids = []
                if st == 'twog/title':
                    kids_expr = "@SOBJECT(twog/proj['title_code','%s'])" % sob_code
                elif st == 'twog/proj':
                    kids_expr = "@SOBJECT(twog/work_order['proj_code','%s'])" % sob_code
                kids = server.eval(kids_expr)
                if pipe_create_method != 'append':
                    future_retires = {}
                    for p in spt_processes:
                        pr = p.get('process')
                        for kid in kids:
                            if p.get('process') == kid.get('process') and p.get('description') == kid.get('description'):
                                found.append(p.get('process'))
                                deps_expr = ''
                                if st == 'twog/title':
                                    deps_expr = "@SOBJECT(twog/work_order['proj_code','%s'])" % kid.get('code')
                                    dep_list = server.eval(deps_expr)
                                    for dep in dep_list:
                                        if p.get('process') not in deps.keys():
                                            deps[p.get('process')] = []
                                        deps[p.get('process')].append(dep)
                                future_retires[pr] = kid.get('__search_key__')
                                #server.retire_sobject(kid.get('__search_key__')) # Comment this back out
                    for kid in kids:                                           #MTM JUST ADDED
                        if kid.get('process') not in future_retires.keys():    #MTM JUST ADDED
                            server.retire_sobject(kid.get('__search_key__'))   #MTM JUST ADDED
        
        
                    tasks_expr = "@SOBJECT(sthpw/task['search_id','%s'])" % my_id
                    tasks = server.eval(tasks_expr)
                    for task in tasks:
                        if task.get('process') in found:
                            if task.get('process') not in saved_task_info.keys():
                                saved_task_info[task.get('process')] = task
                        server.retire_sobject(task.get('__search_key__'))
                        if task.get('process') in future_retires.keys():
                            server.retire_sobject(future_retires[task.get('process')])
                    if tasks == []:
                        the_set = future_retires.keys()
                        for prc in the_set:
                            server.retire_sobject(future_retires[prc])
                new_tasks = {}
                for p in spt_processes:
                    mr_t = ''
                    pr = p.get('process')
                    if p.get('process') in saved_task_info.keys():
                        mr_t_data = {
                                  'assigned': saved_task_info[pr].get('assigned'),
                                  'description': saved_task_info[pr].get('description'),
                                  'status': saved_task_info[pr].get('status'),
                                  'bid_duration': saved_task_info[pr].get('bid_duration'),
                                  'search_type': saved_task_info[pr].get('search_type'),
                                  'search_id': saved_task_info[pr].get('search_id'),
                                  'timestamp': 'now()',
                                  's_status': saved_task_info[pr].get('s_status'),
                                  'process': saved_task_info[pr].get('process'),
                                  'context': saved_task_info[pr].get('context'),
                                  'milestone_code': saved_task_info[pr].get('milestone_code'),
                                  'pipeline_code': new_pipe,
                                  'order_code': the_order.get('code'),
                                  'title_code': title_code,
                                  'client_code': client_code,
                                  'client_name': client_name,
                                  'client_hold': client_hold_str,
                                  'parent_id': saved_task_info[pr].get('parent_id'),
                                  'sort_order': saved_task_info[pr].get('sort_order'),
                                  'depend_id': saved_task_info[pr].get('depend_id'),
                                  'project_code': saved_task_info[pr].get('project_code'),
                                  'supervisor': saved_task_info[pr].get('supervisor'),
                                  'completion': saved_task_info[pr].get('completion'),
                                  'transfer_wo': saved_task_info[pr].get('lookup_code')
                                  }
                        if saved_task_info[pr].get('bid_start_date') not in [None,'']:
                            mr_t_data['bid_start_date'] = SPTDate.convert_to_local(saved_task_info[pr].get('bid_start_date'))
                        if saved_task_info[pr].get('bid_end_date') not in [None,'']:
                            mr_t_data['bid_end_date'] = SPTDate.convert_to_local(saved_task_info[pr].get('bid_end_date'))
                        elif sobb.get('due_date') not in [None,'']:
                            mr_t_data['bid_end_date'] = SPTDate.convert_to_local(sobb.get('due_date'))
                        if saved_task_info[pr].get('actual_start_date') not in [None,'']:
                            mr_t_data['actual_start_date'] = SPTDate.convert_to_local(saved_task_info[pr].get('actual_start_date'))
                        if saved_task_info[pr].get('actual_end_date') not in [None,'']:
                            mr_t_data['actual_end_date'] = SPTDate.convert_to_local(saved_task_info[pr].get('actual_end_date'))
                        if the_order.get('classification') in ['in_production','In Production']:
                            mr_t_data['active'] = True
                        mr_t = server.insert('sthpw/task', mr_t_data) 
                    else:
                        in_data = {
                                  'description': p.get('description'),
                                  'status': 'Pending',
                                  'search_type': st2,
                                  'search_id': my_id,
                                  'timestamp': 'now()',
                                  'order_code': the_order.get('code'),
                                  'title_code': title_code,
                                  'client_code': client_code,
                                  'client_name': client_name,
                                  'client_hold': client_hold_str,
                                  'process': pr,
                                  'context': pr,
                                  'pipeline_code': new_pipe,
                                  'project_code': 'twog'
                                  }
                        if sobb.get('due_date') not in [None,'']:
                            in_data['bid_end_date'] = SPTDate.convert_to_local(sobb.get('due_date'))
                        if the_order.get('classification') in ['in_production','In Production']:
                            in_data['active'] = True
                        mr_t = server.insert('sthpw/task', in_data)  
                    new_tasks[p.get('process')] = mr_t.get('code')
              
                if st == 'twog/title':
                    if pipe_create_method != 'append':
                        for kid in kids:
                            if kid.get('process') not in saved_task_info.keys(): 
                                kid['s_status'] = 'retired'
                                server.retire_sobject(kid.get('__search_key__'))
                            else:
                                server.update(kid.get('__search_key__'), {'task_code': new_tasks[kid.get('process')]})
        
                        new_kids_expr = ''
                        new_kids = []
                        new_kids_expr = "@SOBJECT(twog/proj['title_code','%s'])" % sob_code
                        new_kids = server.eval(new_kids_expr)
                        for nkid in new_kids:
                            if nkid.get('process') in deps.keys():
                                for dep in deps[nkid.get('process')]:
                                    if st == 'twog/title':
                                        server.update(dep.get('__search_key__'), {'proj_code': nkid.get('code')})
        
                        title_prereq_expr = "@SOBJECT(twog/title_prereq['title_code','%s'])" % (sob_code)
                        title_prereqs = server.eval(title_prereq_expr)
                        for tp in title_prereqs:
                            server.retire_sobject(tp.get('__search_key__'))
                    if new_pipe not in ['',None]:
                        if new_pipe.find('NOTHINGXsXNOTHING') == -1:
                            pipe_prereq_expr = "@SOBJECT(twog/pipeline_prereq['pipeline_code','%s'])" % new_pipe
                            pipe_prereqs = server.eval(pipe_prereq_expr)
                            for p in pipe_prereqs:
                                server.insert('twog/title_prereq',{'title_code': sob_code, 'pipeline_code': new_pipe, 'prereq': p.get('prereq'), 'satisfied': False})
                            # Now do the same for the work orders
                            wos = server.eval("@SOBJECT(twog/title['code','%s'].twog/proj.twog/work_order)" % sob_code)
                            for wo in wos:
                                for p in pipe_prereqs:
                                    server.insert('twog/work_order_prereq', {'work_order_code': wo.get('code'), 'prereq': p.get('prereq'), 'satisfied': False, 'from_title': True}, triggers=False)
                    if pipe_create_method != 'append':
                        title_deliverable_expr = "@SOBJECT(twog/deliverable['title_code','%s'])" % (sob_code)
                        title_deliverables = server.eval(title_deliverable_expr)
                        for tp in title_deliverables:
                            server.retire_sobject(tp.get('__search_key__'))
                    if new_pipe not in ['',None]:
                        pipe_deliverable_expr = "@SOBJECT(twog/deliverable_templ['pipeline_code','%s'])" % new_pipe
                        pipe_deliverables = server.eval(pipe_deliverable_expr)
                        for p in pipe_deliverables:
                            p_keys = p.keys()
                            p_data = {}
                            p_data['title_code'] = sob_code
                            for k in p_keys:
                                if k not in ['code','id','__search_key__','search_key','search_type','login','notes','timestamp','s_status','pipeline_code']:
                                    p_data[k] = p[k]
                            server.insert('twog/deliverable', p_data)
        
                server.update(sk, {'trigger_me': ''})
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

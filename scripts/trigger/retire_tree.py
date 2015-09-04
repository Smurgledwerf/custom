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
        # CUSTOM_SCRIPT00007
        ### NEED TO UPDATE COSTS ABOVE SOBJECT WITH THIS SCRIPT
        #print "IN RETIRE TREE NEW"
        def hackpipe_it(data):
            deld_code = data.get('code')
            peer_type = ''
            parent_type_code = ''
            parent_exists = True
            if 'PROJ' in deld_code:
                peer_type = 'proj'
                parent_type_code = 'title_code'
                exist_check = server.eval("@SOBJECT(twog/title['code','%s'])" % data.get('title_code'))
                if len(exist_check) < 1:
                    parent_exists = False
            elif 'WORK_ORDER' in deld_code:
                peer_type = 'work_order'
                parent_type_code = 'proj_code' 
                exist_check = server.eval("@SOBJECT(twog/proj['code','%s'])" % data.get('proj_code'))
                if len(exist_check) < 1:
                    parent_exists = False 
            deld_sk = server.build_search_key('twog/%s' % peer_type, deld_code)
            hack_as_out = server.eval("@SOBJECT(twog/hackpipe_out['out_to','%s'])" % deld_code)
            as_out = []
            for hao in hack_as_out:
                as_out.append(hao.get('lookup_code'))
                server.delete_sobject(hao.get('__search_key__'))
            hack_as_lookup = server.eval("@SOBJECT(twog/hackpipe_out['lookup_code','%s'])" % deld_code)
            as_lookup = []
            for hal in hack_as_lookup:
                as_lookup.append(hal.get('out_to'))
                server.delete_sobject(hal.get('__search_key__'))
            # DO I NEED TO BLOCK PROJs IT IS CONNECTED TO? SAME FOR TITLES IN PROJ HACKS...
            for ao in as_out:
                for al in as_lookup:
                    server.insert('twog/hackpipe_out', {'lookup_code': ao, 'out_to': al})
            if parent_exists:
                parent = server.get_parent(deld_sk)
                parent_sk = parent.get('__search_key__')
                parent_code = parent_sk.split('code=')[1]
                # Get all process information from the pipeline regarding processes linked to this process in the normal pipeline
                info = server.get_pipeline_processes_info(parent.get('__search_key__'), related_process=data.get('process'))
                input_processes = info.get('input_processes')
                real_inputs = {}
                real_input_keys = []
                output_processes = info.get('output_processes')
                if output_processes and input_processes:
                    real_outputs = {}
                    real_out_keys = []
                    if len(input_processes) < 1:
                        real_inputs['parent'] = parent_code
                        real_input_keys.append('parent')
                    for ip in input_processes:
                        rez = server.eval("@SOBJECT(twog/%s['process','%s']['%s','%s'])" % (peer_type, ip, parent_type_code, parent_code))
                        if rez:
                            real_inputs[ip] = rez[0].get('code')
                            real_input_keys.append(ip)
                    for op in output_processes:
                        rez = server.eval("@SOBJECT(twog/%s['process','%s']['%s','%s'])" % (peer_type, op, parent_type_code, parent_code))
                        if rez:
                            real_outputs[op] = rez[0].get('code')
                            real_out_keys.append(op)
                    for ri in real_input_keys:
                        if ri not in as_out and ri not in as_lookup:
                            for ro in real_out_keys:
                                if ro not in as_out and ro not in as_lookup:
                                    server.insert('twog/hackpipe_out', {'lookup_code': real_inputs[ri], 'out_to': real_outputs[ro]})
        
        def floatify(num_str):
            float_return = 0.0
            if num_str not in [None,'']:
                float_return = float(num_str)
            return float_return
        
        import os, time
        from pyasm.common import Environment
        from pyasm.common import SPTDate
        login = Environment.get_login()
        user_name = login.get_login()
        data = input.get('data')
        my_actual = floatify(data.get('actual_cost'))
        my_expected = floatify(data.get('expected_cost'))
        code = data.get('code')
        inorder = ['twog/order','twog/title','twog/proj','twog/work_order']
        fk = ['order_code','title_code','proj_code','work_order_code']
        st = input.get('search_key').split('?')[0]
        idx = inorder.index(st)
        st_code = fk[idx]
        last_deletion_time = 0
        new_time = int(round(time.time() * 1000))
        do_hackpipe = True
        do_cost_reduction = True
        del_time_path = '/var/www/html/user_del_times/%s.time' % user_name
        if os.path.exists(del_time_path):
            f = open(del_time_path, 'r')
            for line in f:
                line = line.rstrip('\r\n')
                if line not in [None,'','\n']:
                    last_deletion_time = int(line)
            f.close()
            os.system('rm -rf %s' % del_time_path)
        f = open(del_time_path, 'w')
        f.write(str(new_time))
        f.close()
        if last_deletion_time == 0:
            last_deletion_time = new_time
        
        # The last_deletion_time will tell us whether or not we should do the hackpipe stuff. In a long deletion from a proj or title or order, we won't want to do the hackpipe stuff. 
        if (new_time - last_deletion_time) < 5000:
            do_hackpipe = False
            do_cost_reduction = False
            
        if st != 'twog/work_order':
            if st == 'twog/proj':
                insert_data = {
                               'login': user_name,
                               'proj_code': data.get('code')
                              }
                for j in data.keys():
                    if j in ['description','keywords','name','actual_markup_pct','actual_overhead_pct','adjusted_price','automated_estimate','bid_offer_price','charged_amount','client_status','cost_margin','flat_pricing','is_billable','pipeline_code','post_order_price','process','projected_markup_pct','rate_card_price','specs','title_code','client_code','proj_templ_code','proj_code','used','projected_overhead_pct','expected_cost','actual_cost','creation_type','title','order_name','priority','po_number','territory','episode','status','tripwire','title_id_number','platform','order_code']:
                        if data[j] not in [None,'']:
                            insert_data[j] = data[j]
                if data.get('completion_date'):
                    insert_data['completion_date'] = SPTDate.convert_to_local(data.get('completion_date'))
                if data.get('due_date'):
                    insert_data['due_date'] = SPTDate.convert_to_local(data.get('due_date'))
                if data.get('start_date'):
                    insert_data['start_date'] = SPTDate.convert_to_local(data.get('start_date'))
                server.insert('twog/proj_transfer', insert_data)
        
            fk_st = inorder[idx + 1]
            expr = "@SOBJECT(%s['%s','%s'])" % (fk_st, st_code, code)
            sobs = server.eval(expr)
            for sob in sobs:
                if fk_st in ['twog/title', 'twog/proj','twog/work_order']:
                    task_code = sob.get('task_code')
                    expr = "@SOBJECT(sthpw/task['code','%s'])" % task_code
                    task = server.eval(expr)
                    if len(task) > 0:
                        task = task[0] 
                        server.retire_sobject(task.get('__search_key__'))
                server.retire_sobject(sob.get('__search_key__'))
            if st == 'twog/proj':
                proj_task = server.eval("@SOBJECT(sthpw/task['code','%s'])" % data.get('task_code'))
                if proj_task:
                    server.retire_sobject(proj_task[0].get('__search_key__')) 
            if do_hackpipe and st == 'twog/proj':
                hackpipe_it(data)
        
        elif st == 'twog/work_order':
            insert_data = {'login': user_name, 'work_order_code': data.get('code')}
            for j in data.keys():
                if j in ['description','keywords','name','work_order_code','work_order_templ_code','proj_code','instructions','process','client_code','work_group','estimated_work_hours','used','actual_cost','expected_cost','creation_type','po_number','order_name','due_date','title','episode','priority','territory','title_id_number','platform','eq_info','order_code','title_code']:
                    if data[j] not in [None,'']:
                        insert_data[j] = data[j]
            server.insert('twog/work_order_transfer', insert_data)
            task_code = data.get('task_code')
            expr = "@SOBJECT(sthpw/task['code','%s'])" % task_code
            task = server.eval(expr)
            if len(task) > 0:
                task = task[0] 
                server.retire_sobject(task.get('__search_key__'))
            if do_hackpipe:
                hackpipe_it(data)
        
        
        # COST UPDATING
        if do_cost_reduction:
            if st == 'twog/title':
                order_code = data.get('order_code')
                the_order = server.eval("@SOBJECT(twog/order['code','%s'])" % order_code)
                if the_order:
                    the_order = the_order[0]
                    order_actual = floatify(the_order.get('actual_cost'))
                    order_expected = floatify(the_order.get('expected_cost'))
                    new_actual = order_actual - my_actual
                    new_expected = order_expected - my_expected
                    server.update(the_order.get('__search_key__'), {'actual_cost': new_actual, 'expected_cost': new_expected})
            elif st == 'twog/proj':
                title_code = data.get('title_code')
                the_title = server.eval("@SOBJECT(twog/title['code','%s'])" % title_code)
                if the_title:
                    the_title = the_title[0]
                    title_actual = floatify(the_title.get('actual_cost'))
                    title_expected = floatify(the_title.get('expected_cost'))
                    new_title_actual = title_actual - my_actual
                    new_title_expected = title_expected - my_expected
                    server.update(the_title.get('__search_key__'), {'actual_cost': new_title_actual, 'expected_cost': new_title_expected})
                    the_order = server.eval("@SOBJECT(twog/order['code','%s'])" % the_title.get('order_code'))
                    if the_order:
                        the_order = the_order[0]
                        order_actual = floatify(the_order.get('actual_cost'))
                        order_expected = floatify(the_order.get('expected_cost'))
                        new_order_actual = order_actual - my_actual
                        new_order_expected = order_expected - my_expected
                        server.update(the_order.get('__search_key__'), {'actual_cost': new_order_actual, 'expected_cost': new_order_expected})
            elif st == 'twog/work_order':
                proj_code = data.get('proj_code')
                the_proj = server.eval("@SOBJECT(twog/proj['code','%s'])" % proj_code)
                if the_proj:
                    the_proj = the_proj[0]
                    proj_actual = floatify(the_proj.get('actual_cost')) 
                    proj_expected = floatify(the_proj.get('expected_cost')) 
                    new_proj_actual = proj_actual - my_actual
                    new_proj_expected = proj_expected - my_expected
                    server.update(the_proj.get('__search_key__'), {'actual_cost': new_proj_actual, 'expected_cost': new_proj_expected})
                    title_code = the_proj.get('title_code')
                    the_title = server.eval("@SOBJECT(twog/title['code','%s'])" % title_code)
                    if the_title:
                        the_title = the_title[0]
                        title_actual = floatify(the_title.get('actual_cost'))
                        title_expected = floatify(the_title.get('expected_cost'))
                        new_title_actual = title_actual - my_actual
                        new_title_expected = title_expected - my_expected
                        server.update(the_title.get('__search_key__'), {'actual_cost': new_title_actual, 'expected_cost': new_title_expected})
                        the_order = server.eval("@SOBJECT(twog/order['code','%s'])" % the_title.get('order_code'))
                        if the_order:
                            the_order = the_order[0]
                            order_actual = floatify(the_order.get('actual_cost'))
                            order_expected = floatify(the_order.get('expected_cost'))
                            new_order_actual = order_actual - my_actual
                            new_order_expected = order_expected - my_expected
                            server.update(the_order.get('__search_key__'), {'actual_cost': new_order_actual, 'expected_cost': new_order_expected})
        #print "LEAVING RETIRE TREE NEW"
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

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
        # CUSTOM_SCRIPT00003
        # Matthew Tyler Misenhimer
        # This is run when a task is added. Tasks are added when a pipeline is attached to a title or project.
        # This will take info from the task and create either a work order or proj
        # THIS IS ADD_WO_OR_PROJ
        # sobj is a task sobject
        from pyasm.common import Environment
        from pyasm.common import SPTDate
        sobj = input.get('sobject')
        # If it wasn't manually inserted, then it is a normally added task (from pipeline attachment)
        if 'Manually Inserted' not in sobj.get('pipeline_code'):
            sobj_sk = server.build_search_key('sthpw/task', sobj.get('code'))
            proj = None
            order = None
            is_master = False
            mr_title = None
            title_title = ''
            title_code = ''
            title_episode = ''
            title_territory = ''
            title_platform = ''
            title_id_number = ''
            client_name = ''
            login = Environment.get_login()
            user_name = login.get_login()
            #This sees if the sobject was being cloned or not. If so, then set the templ_me field to true
            cloning_expr = "@SOBJECT(twog/action_tracker['login','%s']['action','cloning'])" % (user_name)
            cloning = server.eval(cloning_expr);
            templ_me = False
            title_due_date = None
            if len(cloning) > 0:
                templ_me = True
            if 'twog/proj' in sobj.get('search_type'):
                prexpr = "@SOBJECT(twog/proj['id','%s'])" % sobj.get('search_id')
                proj = server.eval(prexpr)[0]
                killed_task = False
                if proj:
                    mr_title_expr = "@SOBJECT(twog/title['code','%s'])" % proj.get('title_code')
                    mr_title = server.eval(mr_title_expr)
                    if mr_title:
                        mr_title = mr_title[0]
                    if mr_title:
                        title_code = mr_title.get('code')
                        title_title = mr_title.get('title')
                        title_due_date = SPTDate.convert_to_local(mr_title.get('due_date'))
                        title_episode = mr_title.get('episode')
                        title_territory = mr_title.get('territory')
                        title_platform = mr_title.get('platform')
                        title_id_number = mr_title.get('title_id_number')
                        client_code = mr_title.get('client_code')
                        client_names = server.eval("@GET(twog/client['code','%s'].name)" % client_code)
                        if len(client_names) > 0:
                            client_name = client_names[0]
                    if mr_title:
                        order = server.eval("@SOBJECT(twog/order['code','%s'])" % mr_title.get('order_code'))[0]
                        order_classification = order.get('classification')
                        #If it is a master, kill the task so it won't show up in operator views
                        if order_classification in ['master','Master']: 
                            is_master = True
                            if is_master:
                                server.retire_sobject(sobj_sk)
                                killed_task = true
                                server.update(proj.get('__search_key__'), {'task_code': ''})
                pipeline_code = proj.get('pipeline_code')
                spt_processes = server.eval("@SOBJECT(config/process['pipeline_code','%s']['process','%s'])"%(pipeline_code, sobj.get('process')))
                # take the first one, we dont expect duplicates
                spt_process = spt_processes[0]  
                
                # query if it exists
                work_order  = server.query('twog/work_order', filters=[('process',sobj.get('process')), ('proj_code', proj.get('code')), ('description', spt_process.get('description')), ('parent_pipe', pipeline_code)])
                
                if not work_order:
                    # find work order template
                    desc = spt_process.get('description')
                    if not desc:
                        desc = '' 
                    wot_expr = "@SOBJECT(twog/work_order_templ['process','%s']['parent_pipe','%s'])" % (sobj.get('process'), pipeline_code)
                    work_order_template = server.eval(wot_expr)
                    if work_order_template:
                        work_order_template = work_order_template[0]
                    instructions = ''
                    estimated_work_hours = ''
                    work_group = ''
                    wo_templ_code = ''
                    if work_order_template:
                        instructions = work_order_template.get('instructions')
                        work_group = work_order_template.get('work_group')
                        estimated_work_hours = work_order_template.get('estimated_work_hours')
                        wo_templ_code = work_order_template.get('code')
                    wo_data = {
                        'process': sobj.get('process'), 
                        'proj_code': proj.get('code'),
                        'description': spt_process.get('description'),
                        'client_code': proj.get('client_code'),
                        'instructions': instructions,
                        'parent_pipe': pipeline_code,
                        'work_group': work_group,
                        'estimated_work_hours': estimated_work_hours,
                        'order_name': order.get('name'),
                        'order_code': order.get('code'),
                        'title_code': proj.get('title_code'),
                        'po_number': order.get('po_number'),
                        'work_order_templ_code': wo_templ_code
                        }
                    if not is_master:
                        wo_data['task_code'] = sobj.get('code')
                    if title_title not in[None,'']:
                        wo_data['title'] = title_title
                    if title_due_date not in[None,'']:
                        wo_data['due_date'] = title_due_date
                    if title_episode not in [None,'']:
                        wo_data['episode'] = title_episode
                    if title_territory not in [None,'']:
                        wo_data['territory'] = title_territory
                    if title_platform not in [None,'']:
                        wo_data['platform'] = title_platform
                    if title_id_number not in [None,'']:
                        wo_data['title_id_number'] = title_id_number
                    # Create the work order
                    wo_insert = server.insert('twog/work_order', wo_data)
                    if templ_me:
                       #If this is the going to be the standard/template for a work order in a pipeline, then we need to remember that this is the one to re-template if changed. 
                       server.update(wo_insert.get('__search_key__'), {'templ_me': templ_me}) 
                    if not killed_task:
                        task_data = {}
                        task_data['lookup_code'] = wo_insert.get('code')
                        task_data['order_name'] = order.get('name')
                        task_data['proj_code'] = proj.get('code')
                        task_data['title_code'] = proj.get('title_code')
                        task_data['order_code'] = order.get('code')
                        if title_due_date:
                            task_data['bid_end_date'] = title_due_date
                        if user_name not in ['',None]:
                            task_data['creator_login'] = user_name
                        if work_order_template.get('assigned_login_group') not in ['',None]:
                            task_data['assigned_login_group'] = work_order_template.get('assigned_login_group')
                        if client_name not in ['',None]:
                            task_data['client_name'] = client_name
                        if title_title not in ['',None]:
                            task_data['title'] = title_title
                        if title_episode not in ['',None]:
                            task_data['episode'] = title_episode
                        if title_territory not in ['',None]:
                            task_data['territory'] = title_territory
                        if title_platform not in ['',None]:
                            task_data['platform'] = title_platform
                        if title_id_number not in ['',None]:
                            task_data['title_id_number'] = title_id_number
                        if order:
                            if order.get('classification') in ['in_production','In Production']:
                                task_data['active'] = True
                            task_data['po_number'] = order.get('po_number')
                        if work_group not in [None,'']:
                            task_data['assigned_login_group'] = work_group
                        #Make sure the wo and task have matching data
                        task_update = server.update(sobj_sk, task_data)
            
                    #Transfers are for deleted/retired work orders - if the same name is coming through from a different pipeline, switch out the info from the deleted one and give to new one
                    #We may want to turn this off at some point... People may write over info they want, or carry over info they don't want  
                    transfer_expr = "@SOBJECT(twog/work_order_transfer['login','%s'])" % (user_name)
                    transfers = server.eval(transfer_expr)
                    #transfers = transfers[::-1]
                    transfer = None
                    if len(transfers) > 0:
                        #transfer = transfers[len(transfers) - 1]
                        do_it = True
                        for tran in transfers:
                            if tran.get('used') == False:
                                if do_it:
                                    if wo_insert.get('process') == tran.get('process') and tran.get('used') == False:
                                        transfer = tran
                                        server.update(tran.get('__search_key__'), {'used': True})
                                        do_it = False
                                    else:
                                        tr = server.eval("@SOBJECT(twog/work_order_transfer['code','%s'])" % tran.get('code'))
                                        if len(tr) > 0 and len(cloning) > 0: 
                                            server.retire_sobject(tran.get('__search_key__'))              
                    if not transfer:
                        # Attach the templated equipment_used's
                        wot_eus_expr = "@SOBJECT(twog/equipment_used_templ['work_order_templ_code','%s'])" % wo_templ_code
                        wot_eus = server.eval(wot_eus_expr)
                        for eu in wot_eus:
                            name = eu.get('name')
                            equipment_code = eu.get('equipment_code')
                            description = eu.get('description')
                            expected_cost = eu.get('expected_cost')
                            expected_duration = eu.get('expected_duration')
                            expected_quantity = eu.get('expected_quantity')
                            eq_templ_code = eu.get('code')
                            units = eu.get('units')
                            ins_data = {'name': name, 'work_order_code': wo_insert.get('code'), 'equipment_code': equipment_code, 'description': description, 'expected_cost': expected_cost, 'expected_duration': expected_duration, 'expected_quantity': expected_quantity, 'units': units}
                            if eq_templ_code not in ['',None]:
                                ins_data['equipment_used_templ_code'] = eq_templ_code
                            server.insert('twog/equipment_used', ins_data)
                        # Attach the templated prereqs
                        wot_prereqs_expr = "@SOBJECT(twog/work_order_prereq_templ['work_order_templ_code','%s'])" % wo_templ_code
                        wot_prereqs = server.eval(wot_prereqs_expr)
                        for wp in wot_prereqs:
                           prereq = wp.get('prereq')
                           server.insert('twog/work_order_prereq', {'work_order_code': wo_insert.get('code'), 'prereq': prereq, 'from_title': False})
                       
                        # Attach the templated work_order_intermediates
                        # Don't create a new entry if the code had already been used
                        all_other_wos_expr = "@SOBJECT(twog/work_order['proj_code','%s']['process','!=','%s'])" % (wo_insert.get('proj_code'), wo_insert.get('process'))
                        all_other_wos = server.eval(all_other_wos_expr)
                        all_other_interms = {}
                        wods = []
                        for other in all_other_wos:
                            other_reals_expr = "@SOBJECT(twog/work_order_intermediate['work_order_code','%s'])" % other.get('code')
                            other_reals = server.eval(other_reals_expr)
                            for otr in other_reals:
                                intermediate_file_code = otr.get('intermediate_file_code')
                                intermediate_file = server.eval("@SOBJECT(twog/intermediate_file['code','%s'])" % intermediate_file_code)[0]
                                iftc = intermediate_file.get('intermediate_file_templ_code')
                                if iftc not in [None,'']:
                                    if iftc not in all_other_interms.keys():
                                        all_other_interms[iftc] = [intermediate_file.get('code'), otr.get('code')]
                            wods_expr = "@SOBJECT(twog/work_order_deliverables['work_order_code','%s'])" % other.get('code')
                            my_wods = server.eval(wods_expr)
                            for wod in my_wods:
                                wods.append(wod)
                        #Intermediates aren't used at all by scheduling, we may want to get rid of these lines
                        int_f_templ_codes_str = work_order_template.get('intermediate_file_templ_codes')
                        int_f_templ_codes = work_order_template.get('intermediate_file_templ_codes').split(',')
                        if int_f_templ_codes_str not in [None,'']:
                            for tc in int_f_templ_codes:
                                if tc not in all_other_interms.keys():
                                    intm_templ = server.eval("@SOBJECT(twog/intermediate_file_templ['code','%s'])" % tc)[0]
                                    intm_title = intm_templ.get('title')
                                    intm_description = intm_templ.get('description')
                                    int_insert = server.insert('twog/intermediate_file', {'title': intm_title, 'description': intm_description, 'intermediate_file_templ_code': intm_templ.get('code')})
                                    server.insert('twog/work_order_intermediate', {'work_order_code': wo_insert.get('code'), 'intermediate_file_code': int_insert.get('code')})
                                else:
                                    int_file_code = all_other_interms[tc]
                                    server.insert('twog/work_order_intermediate', {'work_order_code': wo_insert.get('code'), 'intermediate_file_code': int_file_code})
                       
                
                
                        # Attach the templated deliverables
                        all_delivs_expr = "@SOBJECT(twog/deliverable_templ['work_order_templ_code','%s'])" % wo_templ_code
                        all_delivs = server.eval(all_delivs_expr)
                        for ad in all_delivs:
                            new_deliv_data = {}
                            for k in ad.keys():
                                if k not in ['code','id','login','timestamp','attn','name','deliver_to','keywords','s_status','pipeline_code','work_order_deliverables_code','work_order_templ_code','__search_key__','search_type']:
                                    new_deliv_data[k] = ad.get(k)
                
                        
                            # NEED TO CREATE BARCODE HERE
                            new_bc = 'XsXsXsXsX'
                            repeat = True
                            while repeat:
                                last_bc_expr = "@SOBJECT(twog/barcode['name','The only entry'])"
                                last_bc = server.eval(last_bc_expr)[0]
                                last_num = int(last_bc.get('number'))
                                new_num = last_num + 1
                                server.update(last_bc.get('__search_key__'), {'number': new_num})
                                new_bc = "2GV%s" % new_num
                                bc_sources = server.eval("@SOBJECT(twog/source['barcode','%s'])" % new_bc)
                                if len(bc_sources) < 2:
                                   repeat = False
                            new_deliv_data['barcode'] = new_bc
                            new_deliv_data['client_code'] = mr_title.get('client_code')
                            new_deliv_data['source_for'] = '%s,%s,%s' % (mr_title.get('code'), proj.get('code'), wo_insert.get('code'))
                            new_deliv = server.insert('twog/source', new_deliv_data)
                            server.insert('twog/work_order_deliverables', {'attn': ad.get('attn'), 'name': ad.get('name'), 'deliver_to': ad.get('deliver_to'), 'deliverable_source_code': new_deliv.get('code'), 'title_code': mr_title.get('code'), 'work_order_code': wo_insert.get('code'), 'deliverable_templ_code': ad.get('code')})
                                
                        # NEED TO ATTACH PASS-ALONG INTERMS HERE AS WELL AS PASS-ALONG DELIVS       
                        all_other_delivs = {}
                        for wod in wods:
                            wod_dtc = wod.get('deliverable_templ_code')
                            if wod_dtc not in [None,'']:
                                if wod_dtc not in all_other_delivs.keys():
                                    all_other_delivs[wod_dtc] = [wod.get('deliverable_source_code'), wod.get('code')]
                
                        #People haven't been using the passin templs, we might want to remove these lines, if they'll never use them...
                        passin_templs = server.eval("@SOBJECT(twog/work_order_passin_templ['work_order_templ_code','%s'])" % wo_templ_code)
                        for passin_templ in passin_templs:
                            int_templ_code = passin_templ.get('intermediate_file_templ_code')
                            del_templ_code = passin_templ.get('deliverable_templ_code')
                            if int_templ_code not in [None,'']:
                                if int_templ_code in all_other_interms.keys():
                                    server.insert('twog/work_order_passin', {'work_order_code': wo_insert.get('code'), 'intermediate_file_code': all_other_interms[int_templ_code][0], 'work_order_intermediate_code': all_other_interms[int_templ_code][1], 'passin_templ_code': passin_templ.get('code')})
                            elif del_templ_code not in [None,'']:
                                if del_templ_code in all_other_delivs.keys():
                                    server.insert('twog/work_order_passin', {'work_order_code': wo_insert.get('code'), 'deliverable_source_code': all_other_delivs[del_templ_code][0], 'work_order_deliverables_code': all_other_delivs[del_templ_code][1], 'passin_templ_code': passin_templ.get('code')})
                    else:
                        transfer_wo = transfer.get('work_order_code')
                        #transfer_wo = server.eval("@SOBJECT(twog/work_order_transfer['work_oder_code','%s'])" % sobj.get('transfer_wo'))[0]    
                        wo_upd = {
                                  'description': transfer.get('description'),
                                  'keywords': transfer.get('keywords'),
                                  'instructions': transfer.get('instructions'),
                                  'process': transfer.get('process'),
                                  'client_code': transfer.get('client_code'),
                                  'work_group': transfer.get('work_group'),
                                  'templ_me': templ_me,
                                  'estimated_work_hours': transfer.get('estimated_work_hours')
                                  }
                        server.update(wo_insert.get('__search_key__'), wo_upd)
                        all_eqs = server.eval("@SOBJECT(twog/equipment_used['work_order_code','%s'])" % transfer_wo)
                        all_wods = server.eval("@SOBJECT(twog/work_order_deliverables['work_order_code','%s'])" % transfer_wo)
                        all_wois = server.eval("@SOBJECT(twog/work_order_intermediate['work_order_code','%s'])" % transfer_wo)
                        all_wops = server.eval("@SOBJECT(twog/work_order_passin['work_order_code','%s'])" % transfer_wo)
                        all_woprs = server.eval("@SOBJECT(twog/work_order_prereq['work_order_code','%s'])" % transfer_wo)
                        all_woss = server.eval("@SOBJECT(twog/work_order_sources['work_order_code','%s'])" % transfer_wo)
                        #Attach these objects to the work order
                        for guy in all_eqs:
                            server.update(guy.get('__search_key__'), {'work_order_code': wo_insert.get('code')})
                        for guy in all_wods:
                            server.update(guy.get('__search_key__'), {'work_order_code': wo_insert.get('code')})
                        for guy in all_wois:
                            server.update(guy.get('__search_key__'), {'work_order_code': wo_insert.get('code')})
                        for guy in all_wops:
                            server.update(guy.get('__search_key__'), {'work_order_code': wo_insert.get('code')})
                        for guy in all_woprs:
                            server.update(guy.get('__search_key__'), {'work_order_code': wo_insert.get('code')})
                        for guy in all_woss:
                            server.update(guy.get('__search_key__'), {'work_order_code': wo_insert.get('code')})
                        tr = server.eval("@SOBJECT(twog/work_order_transfer['code','%s'])" % transfer.get('code'))
                        if len(tr) > 0:
                            server.retire_sobject(transfer.get('__search_key__'))
            if 'twog/title' in sobj.get('search_type'):
                #The resulting object will be a proj
                title = server.eval("@SOBJECT(twog/title['code','%s'])" % sobj.get('title_code'))[0]
                title_code = title.get('code')
                title_title = title.get('title')
                title_episode = title.get('episode')
                title_territory = title.get('territory')
                title_platform = title.get('platform')
                title_id_number = title.get('title_id_number')
                new_expr = "@SOBJECT(twog/order['code','%s'])" % title.get('order_code')
                order = server.eval(new_expr)[0]
                client_code = title.get('client_code')
                client_names = server.eval("@GET(twog/client['code','%s'].name)" % client_code)
                if len(client_names) > 0:
                    client_name = client_names[0]
                pipeline_code = title.get('pipeline_code')
                pipe_for_expr = pipeline_code
                spt_processes = server.eval("@SOBJECT(config/process['pipeline_code','%s']['process','%s'])" % (pipeline_code, sobj.get('process')))
                # take the first one, we dont expect duplicates
                spt_process = spt_processes[0]  
                
                # query if it exists
                proj = server.query('twog/proj', filters=[('process',sobj.get('process')), ('title_code', title.get('code')), ('description', spt_process.get('description')),('parent_pipe',pipeline_code)])
                if not proj:
                    desc = spt_process.get('description')
                    if not desc:
                        desc = '' 
                    pj_expr = "@SOBJECT(twog/proj_templ['process','%s']['parent_pipe','%s'])" % (sobj.get('process'), pipeline_code)
                    proj_template = server.eval(pj_expr)
                    if proj_template:
                        proj_template = proj_template[0]
                    is_billable = True
                    flat_pricing = False
                    rate_card_price = 0
                    specs = ''
                    projected_markup_pct = 0.0
                    projected_overhead_pct = 0.0
                    assign_pipe_code = ''
                    proj_templ_code = ''
                    if proj_template:
                        proj_templ_code = proj_template.get('code')
                        is_billable = proj_template.get('is_billable')
                        flat_pricing = proj_template.get('flat_pricing')
                        rate_card_price = proj_template.get('rate_card_price')
                        specs = proj_template.get('specs')
                        projected_markup_pct = proj_template.get('projected_markup_pct')
                        projected_overhead_pct = proj_template.get('projected_overhead_pct')
                        combo_expr = "@SOBJECT(twog/client_pipes['process_name','%s']['pipeline_code','%s'])" % (proj_template.get('process'), pipe_for_expr)
                        combos = server.eval(combo_expr)
                        if len(combos) > 0:
                            assign_pipe_code = combos[0].get('pipe_to_assign')
                    proj_ins_data = { 
                        'process': sobj.get('process'), 
                        'title_code': title.get('code'),
                        'description': spt_process.get('description'),
                        'task_code': sobj.get('code'),
                        'is_billable': is_billable, 
                        'flat_pricing': flat_pricing,
                        'rate_card_price': rate_card_price,
                        'specs': specs,
                        'priority': 100,
                        'projected_markup_pct': projected_markup_pct,
                        'projected_overhead_pct': projected_overhead_pct,
                        'client_code': title.get('client_code'),
                        'pipeline_code': 'No Pipeline Assigned',
                        'parent_pipe': pipeline_code,
                        'order_name': order.get('name'),
                        'po_number': order.get('po_number'),
                        'status': sobj.get('status'),
                        'proj_templ_code': proj_templ_code,
                        'order_code': order.get('code')
                    }
                    if title_title not in [None,'']:
                        proj_ins_data['title'] = title_title
                    if title_due_date not in [None,'']:
                        proj_ins_data['due_date'] = title_due_date
                    if title_episode not in [None,'']:
                        proj_ins_data['episode'] = title_episode
                    if title_territory not in [None,'']:
                        proj_ins_data['territory'] = title_territory
                    if title_platform not in [None,'']:
                        proj_ins_data['platform'] = title_platform
                    if title_id_number not in [None,'']:
                        proj_ins_data['title_id_number'] = title_id_number
                    proj = server.insert('twog/proj', proj_ins_data)
                    if templ_me:
                        server.update(proj.get('__search_key__'), {'templ_me': templ_me})
                    killed_task = False
                    if proj:
                        mr_title2_expr = "@SOBJECT(twog/title['code','%s'])" % proj.get('title_code')
                        mr_title = server.eval(mr_title2_expr)[0]
                        if mr_title:
                            order2_expr = "@SOBJECT(twog/order['code','%s'])" % mr_title.get('order_code')
                            order = server.eval(order2_expr)[0]
                            order_classification = order.get('classification')
                            if order_classification in ['master','Master']: 
                                is_master = True
                                if is_master:
                                    server.retire_sobject(sobj_sk)
                                    killed_task = True
                                    server.update(proj.get('__search_key__'), {'task_code': ''})
                    if not killed_task:
                        task_data = {}
                        task_data['lookup_code'] = proj.get('code')
                        task_data['proj_code'] = proj.get('code')
                        task_data['order_name'] = order.get('name')
                        task_data['po_number'] = order.get('po_number')
                        task_data['order_code'] = order.get('code')
                        task_data['title_code'] = proj.get('title_code')
                        if title_due_date:
                            task_data['bid_end_date'] = title_due_date 
                        if user_name not in ['',None]:
                            task_data['creator_login'] = user_name
                        if client_name not in ['',None]:
                            task_data['client_name'] = client_name
                        if title_title not in ['',None]:
                            task_data['title'] = title_title
                        if title_episode not in ['',None]:
                            task_data['episode'] = title_episode
                        if title_territory not in ['',None]:
                            task_data['territory'] = title_territory
                        if title_platform not in ['',None]:
                            task_data['platform'] = title_platform
                        if title_id_number not in ['',None]:
                            task_data['title_id_number'] = title_id_number
                        if order.get('classification') in ['in_production','In Production']:
                            task_data['active'] = True
                        server.update(sobj_sk, task_data)
                    if assign_pipe_code not in  [None,'']:
                        server.update(proj.get('__search_key__'), {'pipeline_code': assign_pipe_code, 'priority': 100})
            
                    transfer_expr = "@SOBJECT(twog/proj_transfer['login','%s'])" % (user_name)
                    transfers = server.eval(transfer_expr)
                    transfer = None
                    if len(transfers) > 0:
                        do_it = True
                        for tran in transfers:
                            if tran.get('used') == False:
                                if do_it:
                                    if proj.get('process') == tran.get('process'):
                                        transfer = tran
                                        server.update(tran.get('__search_key__'), {'used': True})
                                        do_it = False
                                    else:
                                        tr = server.eval("@SOBJECT(twog/proj_transfer['code','%s'])" % tran.get('code'))
                                        if len(tr) > 0 and len(cloning) > 0: 
                                            server.retire_sobject(tran.get('__search_key__'))              
                    if transfer:
                        transfer_proj = transfer.get('proj_code')
                        proj_upd = {
                                  # Fill in fields here. Do a second update for the pipeline code
                                       'actual_markup_pct': transfer.get('actual_markup_pct'),
                                       'actual_overhead_pct': transfer.get('actual_overhead_pct'),
                                       'adjusted_price': transfer.get('adjusted_price'),
                                       'automated_estimate': transfer.get('automated_estimate'),
                                       'bid_offer_price': transfer.get('bid_offer_price'),
                                       'charged_amount': transfer.get('charged_amount'),
                                       'client_status': transfer.get('client_status'),
                                       'cost_margin': transfer.get('cost_margin'),
                                       'flat_pricing': transfer.get('flat_pricing'),
                                       'is_billable': transfer.get('is_billable'),
                                       'pipeline_code': transfer.get('pipeline_code'),
                                       'post_order_price': transfer.get('post_order_price'),
                                       'projected_markup_pct': transfer.get('projected_markup_pct'),
                                       'rate_card_price': transfer.get('rate_card_price'),
                                       'specs': transfer.get('specs'),
                                       'description': transfer.get('description'),
                                       'keywords': transfer.get('keywords'),
                                       'proj_templ_code': transfer.get('proj_templ_code'),
                                       'title_code': transfer.get('title_code'),
                                       'process': transfer.get('process'),
                                       'client_code': transfer.get('client_code'),
                                       'templ_me': templ_me,
                                       'login': user_name
                                  }
                        if transfer.get('completion_date') not in [None,'']:
                            proj_upd['completion_date'] = SPTDate.convert_to_local(transfer.get('completion_date'))
                        if transfer.get('start_date') not in [None,'']:
                            proj_upd['start_date'] = SPTDate.convert_to_local(transfer.get('start_date'))
                        if transfer.get('due_date') not in [None,'']:
                            proj_upd['due_date'] = SPTDate.convert_to_local(transfer.get('due_date'))
                        proj_again = server.update(proj.get('__search_key__'), proj_upd)
                        tr = server.eval("@SOBJECT(twog/proj_transfer['code','%s'])" % transfer.get('code'))
                        if len(tr) > 0: 
                            server.retire_sobject(transfer.get('__search_key__'))
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

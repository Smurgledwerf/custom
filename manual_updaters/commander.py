__all__ = ["ShrinkPrioritiesCmd","ClientBillingTaskVisibilityCmd","DBDirectCmd","TitleClonerCmd","ClipboardAddCmd","ClipboardMovementMakerCmd","ClipboardEmptySearchTypeCmd","CreateTitlesCmd","NormalPipeToHackPipeCmd","UpdateNotesSeenByCmd"]
import os, time
from pyasm.command import Command, CommandException

class ShrinkPrioritiesCmd(Command): 
    def execute(my):
        os.system('python /opt/spt/custom/manual_updaters/update_priorities.py > /tmp/prio_adj')

class ClientBillingTaskVisibilityCmd(Command): 
    def init(my):
        my.client_code = ''
        my.new_task_str = ''
    def execute(my):
        my.client_code = my.kwargs.get('client_code')
        my.new_task_str = my.kwargs.get('new_task_str')
        os.system('''python /opt/spt/custom/manual_updaters/update_task_client_hold.py '%s' '%s' > /tmp/task_adj''' % (my.client_code, my.new_task_str))

class DBDirectCmd(Command):
    def init(my):
        my.cmnd = ''
        my.which_db = ''

    def make_timestamp(my):
        #Makes a Timestamp for postgres
        #NEED TO GET RID OF THIS AND USE A PASSIN FROM KWARGS INSTEAD
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%Y_%m_%d_%H_%M_%S")

    def execute(my):
        my.cmnd = my.kwargs.get('cmnd')
        my.which_db = my.kwargs.get('which_db')
        print "MY COMMAND = %s" % my.cmnd
        print "WHICH DB = %s" % my.which_db
        if my.cmnd not in [None,''] and my.which_db not in [None,'']:
            #NEED TO GET RID OF THIS AND USE A PASSIN FROM KWARGS INSTEAD
            #This is for avoiding collisions
            timestamp = my.make_timestamp()
            path_prefix = '/var/www/html/user_reports_tables/'
            the_file = '%sdb_direct_cmd_%s' % (path_prefix, timestamp)
            rez_file = '%sdb_direct_cmd_result_%s' % (path_prefix, timestamp)
            if os.path.exists(the_file):
                os.system('rm -rf %s' % the_file)
            new_guy = open(the_file, 'w')
            new_guy.write('%s\n' % my.cmnd)
            new_guy.close()
            print "GOT TO THE ACTION PART"
            os.system('''psql -U postgres %s < %s > %s''' % (my.which_db, the_file, rez_file))

class TitleClonerCmd(Command):

    def __init__(my, **kwargs):
        from client.tactic_client_lib import TacticServerStub
        super(TitleClonerCmd, my).__init__(**kwargs)
        my.titles_str = str(kwargs.get('titles'))
        my.order_codes = str(kwargs.get('order_code')).split(',')
        
        my.user_name = str(kwargs.get('user_name'))
        my.redo = str(kwargs.get('redo'))
        my.no_charge = str(kwargs.get('no_charge'))
        my.copy_attributes_str = str(kwargs.get('copy_attributes'))
        my.copy_attributes = False
        if my.copy_attributes_str == 'true':
            my.copy_attributes = True
        my.server = TacticServerStub.get()

    def clone_dict(my, dict, extra_dict, filter):
        filter.append('code')
        filter.append('__search_key__')
        filter.append('__search_type__')
        filter.append('id')
        filter.append('keywords')
        filter.append('timestamp')
        filter.append('s_status')
        filter.append('login')
        keys = dict.keys()
        new_dict = {}
        for k in keys:
            if '_date' not in k and '_month' not in k:
                if k not in filter:
                        if dict[k] != None:
                            new_dict[k] = dict[k]
        ekeys = extra_dict.keys()
        for e in ekeys:
            if extra_dict[e] != None:
                new_dict[e] = extra_dict[e]
        return new_dict

    def check(my):
        return True
    
    def execute(my):   
        from pyasm.common import SPTDate
        for ord_code in my.order_codes:
            order = my.server.eval("@SOBJECT(twog/order['code','%s'])" % ord_code)[0]
            new_title_count = 0
            old_title_count = order.get('titles_total')
            if old_title_count in [None,'']:
                old_title_count = 0
            else:
                old_title_count = int(old_title_count)
            titles = my.titles_str.split(',')
            exchange = {}
            #Need to fill in wo_count on title after you find all the work orders and tally them up 
            o_wo_count = 0
            for tsss in titles:
                times = tsss.split('[')
                t = times[0]
                repeats = int(times[1].replace(']',''))
                for dr_count in range(0,repeats):
                    t_wo_count = 0
                    title = my.server.eval("@SOBJECT(twog/title['code','%s'])" % t)
                    if len(title) > 0:
                        title = title[0]
                        tclient = my.server.eval("@SOBJECT(twog/client['code','%s'])" % title.get('client_code'))
                        billing_str = 'no problems'
                        client_name = ''
                        client_code = ''
                        if len(tclient) > 0:
                            tclient = tclient[0]
                            client_name = tclient.get('name')
                            client_code = tclient.get('code')
                            billing_status = tclient.get('billing_status')
                            if 'Do Not Ship' in billing_status:
                                billing_str = 'noship'
                            elif 'Do Not Book' in billing_status:
                                billing_str = 'nobook'
                        tdict = my.clone_dict(title, {'order_code': ord_code, 'order_name': order.get('name'), 'login': my.user_name, 'po_number': order.get('po_number'), 'pulled_blacks': '0', 'priority': 100, 'wo_completed': 0}, ['trigger_me','client_status','status','closed','actual_cost','trt_pricing','title_id_number','price','rejection_description','numeric_client_status','saved_priority','resets','bigboard','wo_count','file_size','status_triggers','priority_triggers'])
                        tdict['no_charge'] = my.no_charge
                        tdict['redo'] = my.redo
                        if my.no_charge not in [False,'False','false','f',None] and my.redo not in [False,'False','false','f',None]:
                            tdict['priority'] = .0001
                            tdict['audio_priority'] = .0001
                            tdict['compression_priority'] = .0001
                            tdict['edeliveries_priority'] = .0001
                            tdict['edit_priority'] = .0001
                            tdict['machine_room_priority'] = .0001
                            tdict['media_vault_priority'] = .0001
                            tdict['qc_priority'] = .0001
                            tdict['vault_priority'] = .0001
                            tdict['price'] = 0
                            tdict['expected_price'] = 0
                            tdict['bigboard'] = True
                        elif my.copy_attributes: # Then copy the title priorities and bigboard stuff
                            tdict['priority'] = title.get('priority')
                            tdict['audio_priority'] =  title.get('audio_priority')
                            tdict['compression_priority'] =  title.get('compression_priority')
                            tdict['edeliveries_priority'] =  title.get('edeliveries_priority')
                            tdict['edit_priority'] =  title.get('edit_priority')
                            tdict['machine_room_priority'] =  title.get('machine_room_priority')
                            tdict['media_vault_priority'] =  title.get('media_vault_priority')
                            tdict['qc_priority'] =  title.get('qc_priority')
                            tdict['vault_priority'] =  title.get('vault_priority')
                            tdict['bigboard'] = title.get('bigboard')
                        else:
                            tdict['priority'] = 100 
                            tdict['audio_priority'] =  100
                            tdict['compression_priority'] =  100
                            tdict['edeliveries_priority'] =  100
                            tdict['edit_priority'] =  100
                            tdict['machine_room_priority'] =  100
                            tdict['media_vault_priority'] =  100
                            tdict['qc_priority'] =  100
                            tdict['vault_priority'] =  100
                            tdict['bigboard'] = False
                        if order.get('due_date') not in [None,'']:
                            tdict['due_date'] = SPTDate.convert_to_local(order.get('due_date'))
                        if order.get('start_date') not in [None,'']:
                            tdict['start_date'] = SPTDate.convert_to_local(order.get('start_date'))
                        if order.get('expected_revenue_month') not in [None,'']:
                            tdict['expected_revenue_month'] = SPTDate.convert_to_local(order.get('expected_revenue_month'))
                        if order.get('expected_delivery_date') not in [None,'']:
                            tdict['expected_delivery_date'] = SPTDate.convert_to_local(order.get('expected_delivery_date'))
                        tdict['is_external_rejection'] = 'false'
                        new_title = my.server.insert('twog/title', tdict, triggers=False)
                        new_title_count = new_title_count + 1
                        exchange[t] = new_title.get('code')
                        projs = my.server.eval("@SOBJECT(twog/proj['title_code','%s'])" % t)
                        for proj in projs:
                            ptask = my.server.eval("@SOBJECT(sthpw/task['lookup_code','%s'])" % proj.get('code'))
                            new_ptask = None
                            if len(ptask) > 0:
                                ptask = ptask[0]
                                pt_dict = my.clone_dict(ptask, {'login': my.user_name, 'creator_login': my.user_name, 'order_code': ord_code, 'title_code': new_title.get('code'), 'po_number': order.get('po_number'), 'client_name': client_name, 'title_id_number': new_title.get('title_id_number'),'search_id': title.get('id'), 'title': new_title.get('title'), 'episode': new_title.get('episode'), 'status': 'Pending', 'po_number': order.get('po_number'), 'client_hold': billing_str, 'order_name': order.get('name')}, ['assigned','discussion','bid_duration','milestone_code','parent_id','sort_order','depend_id','supervisor','completion','lookup_code','active','proj_code','supervisor','actual_duration','tripwire','closed','transfer_wo'])
                                new_ptask = my.server.insert('sthpw/task', pt_dict, triggers=False) 
                            pdict = my.clone_dict(proj, {'status': 'Pending', 'priority': 100, 'order_code': ord_code, 'order_name': order.get('name'), 'title_code': new_title.get('code'), 'parent_pipe': new_title.get('pipeline_code'), 'client_name': client_name, 'client_code': client_code, 'title': new_title.get('title'), 'episode': new_title.get('episode'), 'po_number': new_title.get('po_number'), 'title_id_number': new_title.get('title_id_number')}, ['cost_margin','client_status','bid_offer_price','automated_estimate','adjusted_price','charged_amount','is_billable','flat_pricing','projected_overhead_pct','actual_overhead_pct','projected_markup_pct','actual_markup_pct','trigger_me','templ_me','actual_cost','tripwire','post_order_price','price','actual_cost','closed','task_code'])
                            if new_ptask:
                                pdict['task_code'] = new_ptask.get('code')
                            new_proj = my.server.insert('twog/proj', pdict, triggers=False)
                            exchange[proj.get('code')] = new_proj.get('code')
                            #Make sure to link the task and project together both ways - lookup_code, task_code & proj_code
                            if new_ptask:
                                my.server.update(new_ptask.get('__search_key__'), {'lookup_code': new_proj.get('code'), 'proj_code': new_proj.get('code')}, triggers=False)
                            wos = my.server.eval("@SOBJECT(twog/work_order['proj_code','%s'])" % proj.get('code'))
                            for wo in wos:
                                wtask = my.server.eval("@SOBJECT(sthpw/task['lookup_code','%s'])" % wo.get('code'))
                                new_wtask = None
                                if len(wtask) > 0:
                                    wtask = wtask[0]
                                    wt_dict = my.clone_dict(wtask, {'login': my.user_name, 'creator_login': my.user_name, 'order_code': ord_code, 'title_code': new_title.get('code'), 'po_number': order.get('po_number'), 'client_name': client_name, 'proj_code': new_proj.get('code'), 'title_id_number': new_title.get('title_id_number'),'search_id': new_proj.get('id'), 'title': new_title.get('title'), 'episode': new_title.get('episode'), 'status': 'Pending', 'po_number': order.get('po_number'), 'client_hold': billing_str, 'order_name': order.get('name')}, ['assigned','discussion','bid_duration','milestone_code','parent_id','sort_order','depend_id','supervisor','completion','lookup_code','active','supervisor','actual_duration','tripwire','closed','transfer_wo'])
                                    if tdict['bigboard'] in [True,'true','t',1]:
                                        wt_dict['bigboard'] = True
                                    else:
                                        wt_dict['bigboard'] = False 
                                    new_wtask = my.server.insert('sthpw/task', wt_dict, triggers=False) 
                                wo_dict = my.clone_dict(wo, {'order_code': ord_code, 'title_code': new_title.get('code'), 'proj_code': new_proj.get('code'), 'client_code': client_code, 'client_name': client_name, 'order_name': order.get('name'), 'title_id_number': new_title.get('title_id_number'), 'po_number': order.get('po_number')}, ['task_code','templ_me','closed','actual_cost','assigned','eq_info','status','priority'])
                                if new_wtask:
                                    wo_dict['task_code'] = new_wtask.get('code')
                                new_wo = my.server.insert('twog/work_order', wo_dict, triggers=False)
                                t_wo_count = t_wo_count + 1
                                exchange[wo.get('code')] = new_wo.get('code')
                                if new_wtask:
                                    my.server.update(new_wtask.get('__search_key__'), {'lookup_code': new_wo.get('code')}, triggers=False)
                                #Make sure to link the task and work order together both ways
                                eqs = my.server.eval("@SOBJECT(twog/equipment_used['work_order_code','%s'])" % wo.get('code'))
                                eq_info = ''
                                for eq in eqs:
                                    eq_dict = my.clone_dict(eq, {'work_order_code': new_wo.get('code'), 'client_code': client_code}, ['code','keywords','work_order_code','actual_cost','actual_duration','pipeline_code'])
                                    new_eq = my.server.insert('twog/equipment_used', eq_dict, triggers=False)
                                    if eq_info == '':
                                        eq_info = '%sX|X%sX|X%sX|X' % (new_eq.get('code'), new_eq.get('name'), new_eq.get('units').upper())
                                    else: 
                                        eq_info = '%sZ,Z%sX|X%sX|X%sX|X' % (eq_info, new_eq.get('code'), new_eq.get('name'), new_eq.get('units').upper())
                                #When done with eq, create the eq_info string to put on the work_order
                                my.server.update(new_wo.get('__search_key__'), {'eq_info': eq_info})
                        my.server.update(new_title.get('__search_key__'), {'wo_count': t_wo_count}, triggers=False)         
                        o_wo_count = o_wo_count + t_wo_count                      
            now_title_count = old_title_count + new_title_count
            my.server.update(order.get('__search_key__'), {'wo_count': o_wo_count, 'titles_total': now_title_count}, triggers=False)         
        #When done with WOS, create the wo hackups, if there are any
        #When done with Projs, create the proj hackups, if there are any
        exkeys = exchange.keys()
        long_str = ''
        for ecode in exkeys:
            if long_str == '':
                long_str = ecode
            else:
                long_str = '%s|%s' % (long_str, ecode)
        hackups = my.server.eval("@SOBJECT(twog/hackpipe_out['out_to','in','%s'])" % long_str)
        for h in hackups:
            lookup_code = h.get('lookup_code')
            out_to = h.get('out_to')
            new_lookup = ''
            new_out = ''
            if lookup_code in exkeys:  
                new_lookup = exchange[lookup_code]
            if out_to in exkeys:
                new_out = exchange[out_to]
            if new_lookup != '' and new_out != '':
                my.server.insert('twog/hackpipe_out',{'lookup_code': new_lookup, 'out_to': new_out})
        return ''


    def check_security(my):
        '''give the command a callback that allows it to check security'''
        return True

    def get_title(my):
        return "Make Note"
        
         

class ClipboardAddCmd(Command):

    def __init__(my, **kwargs):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        super(ClipboardAddCmd, my).__init__(**kwargs)
        my.code = str(kwargs.get('code'))
        my.st = str(kwargs.get('st')).split('?')[0]
        my.login = Environment.get_login()
        my.user_name = my.login.get_login() 
        my.server = TacticServerStub.get()

    def check(my):
        return True
    
    def execute(my):   
       
        login = my.server.eval("@SOBJECT(sthpw/login['login','%s']['location','internal'])" % my.user_name)[0]
        chunk_st = '[%s]' % my.st
        clipboard = login.get('clipboard')
        new_clippie = ''
        stopit = False
        if chunk_st in clipboard:
            cut1 = clipboard.split(chunk_st)
            cut2 = cut1[1].split('[')
            cut2_sec = cut2[0]
            new_text = ''
            if cut2_sec in [None,'']:
                cut2_sec = my.code
            elif my.code in cut2_sec:
                stopit = True
            else:
                cut2_sec = '%s|%s' % (cut2_sec, my.code)
            if not stopit:
                new_text = cut2_sec
                if len(cut2) > 1:
                    new_clippie = '%s%s%s[%s' % (cut1[0],chunk_st,new_text,cut2[1:])
                else:
                    new_clippie = '%s%s%s' % (cut1[0],chunk_st,new_text)
        else:
            new_clippie = '%s%s%s' % (clipboard, chunk_st, my.code)
        if not stopit:
            my.server.update(login.get('__search_key__'), {'clipboard': new_clippie}) 
            
        return ''


    def check_security(my):
        '''give the command a callback that allows it to check security'''
        return True

    def get_title(my):
        return "Clipboard Add"
        
         

class ClipboardMovementMakerCmd(Command):

    def __init__(my, **kwargs):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        super(ClipboardMovementMakerCmd, my).__init__(**kwargs)
        my.login = Environment.get_login()
        my.user_name = my.login.get_login() 
        my.server = TacticServerStub.get()
        my.movement_code = str(kwargs.get('movement_code'))

    def check(my):
        return True
    
    def execute(my):   
       
        login = my.server.eval("@SOBJECT(sthpw/login['login','%s']['location','internal'])" % my.user_name)[0]
        chunk_st = '[twog/source]'
        clipboard = login.get('clipboard')
        new_clippie = ''
        source_codes = []
        if chunk_st in clipboard:
            cut1 = clipboard.split(chunk_st)
            cut2 = cut1[1].split('[')
            cut2_sec = cut2[0]
            source_codes = cut2_sec.split('|')
        for scode in source_codes:
            source_barcode = my.server.eval("@GET(twog/source['code','%s'].barcode)" % scode)[0]
            my.server.insert('twog/asset_to_movement', {'movement_code': my.movement_code, 'source_code': scode, 'barcode': source_barcode})           
        return ''


    def check_security(my):
        '''give the command a callback that allows it to check security'''
        return True

    def get_title(my):
        return "Clipboard Add"
        
         
class ClipboardEmptySearchTypeCmd(Command):

    def __init__(my, **kwargs):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        super(ClipboardEmptySearchTypeCmd, my).__init__(**kwargs)
        my.login = Environment.get_login()
        my.user_name = my.login.get_login() 
        my.server = TacticServerStub.get()
        my.search_type = str(kwargs.get('search_type'))

    def check(my):
        return True
    
    def execute(my):   
       
        login = my.server.eval("@SOBJECT(sthpw/login['login','%s']['location','internal'])" % my.user_name)[0]
        clipboard = login.get('clipboard')
        if my.search_type == 'ALL':
            clipboard = ''
        else:
            finder = '[%s]' % my.search_type
            if finder in clipboard:
                chunks = clipboard.split(finder)
                pre = chunks[0]
                post_split = chunks[1].split('[')
                post = ''
                if len(post_split) > 1:
                    ct = 0
                    for ps in post_split:
                        if ct > 0:
                            post = '%s[%s' % (post, ps) 
                        ct = ct + 1
                clipboard = '%s%s' % (pre, post)
               
        my.server.update(login.get('__search_key__'), {'clipboard': clipboard})
        
        return ''


    def check_security(my):
        '''give the command a callback that allows it to check security'''
        return True

    def get_title(my):
        return "Clipboard Add"

class CreateTitlesCmd(Command):
    def __init__(my, **kwargs):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        super(CreateTitlesCmd, my).__init__(**kwargs)
        my.login = Environment.get_login()
        my.user_name = my.login.get_login() 
        my.server = TacticServerStub.get()
        my.data = kwargs.get('data')
        my.episodes = kwargs.get('episodes')
        

    def check(my):
        return True
    
    def execute(my):   
        #THIS IS MAKE KIDS MATCH PIPE
        #begin_time = time.time()
        from pyasm.common import Environment
        pipeline_code = my.data.get('pipeline_code')
        order_code = my.data.get('order_code')
        order = my.server.eval("@SOBJECT(twog/order['code','%s'])" % order_code)[0]
        client_code = ''
        client_name = ''
        client = my.server.eval("@SOBJECT(twog/client['code','%s'])" % order.get('client_code'))
        client_hold_str = 'no problems'
        pipe_dict = {'TITLE': {'processes': [], 'tasks': {}, 'projs': {}, 'prereq': []}}
        if client:
            client = client[0]
            client_code = client.get('code')
            client_name = client.get('name')
            client_hold = client.get('billing_status')
            if 'Do Not Ship' in client_hold:
                client_hold_str = 'noship'
            elif 'Do Not Book' in client_hold:
                client_hold_str = 'nobook'
        pipe_prereq_expr = "@SOBJECT(twog/pipeline_prereq['pipeline_code','%s'])" % pipeline_code
        pipe_prereqs = my.server.eval(pipe_prereq_expr)
        for p in pipe_prereqs:
            tprereq = {'pipeline_code': pipeline_code, 'prereq': p.get('prereq'), 'satisfied': False}
            pipe_dict['TITLE']['prereq'].append(tprereq)


        title_id_number = my.data.get('title_id_number')
        if title_id_number in [None,'']:
            title_id_number = '' 

        spt_processes_expr = "@SOBJECT(config/process['pipeline_code','%s'])" % (pipeline_code)
        spt_processes = my.server.eval(spt_processes_expr)
        for pro in spt_processes:
            pj_expr = "@SOBJECT(twog/proj_templ['process','%s']['parent_pipe','%s'])" % (pro.get('process'), pipeline_code)
            pts = my.server.eval(pj_expr)
            for pt in pts:
                is_billable = True
                flat_pricing = False
                rate_card_price = 0
                specs = ''
                projected_markup_pct = 0.0
                projected_overhead_pct = 0.0
                assign_pipe_code = ''
                proj_templ_code = ''
                if pt:
                    proj_templ_code = pt.get('code')
                    is_billable = pt.get('is_billable')
                    flat_pricing = pt.get('flat_pricing')
                    rate_card_price = pt.get('rate_card_price')
                    specs = pt.get('specs')
                    projected_markup_pct = pt.get('projected_markup_pct')
                    projected_overhead_pct = pt.get('projected_overhead_pct')
                    combo_expr = "@SOBJECT(twog/client_pipes['process_name','%s']['pipeline_code','%s'])" % (pt.get('process'), pipeline_code)
                    combos = my.server.eval(combo_expr)
                    if len(combos) > 0:
                        assign_pipe_code = combos[0].get('pipe_to_assign')
                start_date = my.data.get('start_date')
                if start_date in [None,'']:
                    start_date = order.get('timestamp')
                due_date = my.data.get('due_date')
                if due_date not in [None,'']:
                    due_date = order.get('due_date')
                platform = ''
                if my.data.get('platform') not in [None,'']:
                    platform = my.data.get('platform')
                territory = ''
                if my.data.get('territory') not in [None,'']:
                    territory = my.data.get('territory')
                title_id_number = '' 
                if my.data.get('title_id_number') not in [None,'']:
                    title_id_number = my.data.get('title_id_number')
                my.data['start_date'] = start_date
                my.data['due_date'] = due_date
                proj_ins_data = { 
                    'process': pro.get('process'), 
                    'description': pro.get('description'),
                    'is_billable': is_billable, 
                    'flat_pricing': flat_pricing,
                    'rate_card_price': rate_card_price,
                    'specs': specs,
                    'priority': 100,
                    'projected_markup_pct': projected_markup_pct,
                    'projected_overhead_pct': projected_overhead_pct,
                    'client_code': client_code,
                    'client_name': client_name,
                    'parent_pipe': pipeline_code,
                    'order_name': order.get('name'),
                    'po_number': order.get('po_number'),
                    'status': 'Pending',
                    'proj_templ_code': proj_templ_code,
                    'order_code': order.get('code'),
                    'title_id_number': title_id_number, 
                    'due_date': due_date,
                    'territory': territory,
                    'platform': platform,
                    'pipeline_code': assign_pipe_code
                }
                pipe_dict['TITLE']['processes'].append(pro.get('process'))
                pipe_dict['TITLE']['projs'][pro.get('process')] = {'data': proj_ins_data, 'processes': [], 'tasks': {}, 'work_orders': {}}
                task_ins_data = { 
                              'description': pro.get('description'),
                              'status': 'Pending',
                              'bid_start_date': start_date,
                              'bid_end_date': due_date,
                              'search_type': 'twog/title?project=twog',
                              'timestamp': 'now()',
                              's_status': '',
                              'process': pro.get('process'),
                              'context': pro.get('process'),
                              'pipeline_code': pipeline_code,
                              'project_code': 'twog',
                              'client_code': client_code,
                              'client_name': client_name,
                              'client_hold': client_hold_str,
                              'creator_login': my.user_name,
                              'order_code': order.get('code'),
                              'title_id_number': title_id_number, 
                              'transfer_wo': ''
                              }
                if order.get('classification') in ['in_production','In Production']:
                    task_ins_data['active'] = True
                pipe_dict['TITLE']['tasks'][pro.get('process')] = task_ins_data
                if proj_ins_data['pipeline_code'] not in [None,'']:
                    proj_pipe = proj_ins_data['pipeline_code']
                    spt_processes_expr2 = "@SOBJECT(config/process['pipeline_code','%s'])" % (proj_pipe)
                    spt_processes2 = my.server.eval(spt_processes_expr2)
                    for wpro in spt_processes2:
                        desc = wpro.get('description')
                        if not desc:
                            desc = '' 
                        pj_expr2 = "@SOBJECT(twog/work_order_templ['process','%s']['parent_pipe','%s'])" % (wpro.get('process'), proj_pipe)
                        wt = my.server.eval(pj_expr2)
                        if wt not in [None,'',[]] and len(wt) > 0:
                            wt = wt[0]
                            instructions = ''
                            estimated_work_hours = ''
                            work_group = ''
                            wo_templ_code = ''
                            if wt:
                                instructions = wt.get('instructions')
                                work_group = wt.get('work_group')
                                estimated_work_hours = wt.get('estimated_work_hours')
                                wo_templ_code = wt.get('code')
                            wo_data = {
                                'process': wpro.get('process'), 
                                'description': desc,
                                'client_code': client_code,
                                'instructions': instructions,
                                'parent_pipe': proj_pipe,
                                'work_group': work_group,
                                'estimated_work_hours': estimated_work_hours,
                                'order_name': order.get('name'),
                                'order_code': order.get('code'),
                                'po_number': order.get('po_number'),
                                'work_order_templ_code': wo_templ_code,
                                'due_date': due_date,
                                'territory': territory,
                                'platform': platform,
                                'title_id_number': title_id_number
                                }
                            task_data = { 
                              'description': desc,
                              'status': 'Pending',
                              'bid_start_date': start_date,
                              'bid_end_date': due_date,
                              'search_type': 'twog/proj?project=twog',
                              'timestamp': 'now()',
                              's_status': '',
                              'process': wpro.get('process'),
                              'context': wpro.get('process'),
                              'pipeline_code': proj_pipe,
                              'project_code': 'twog',
                              'client_code': client_code,
                              'client_name': client_name,
                              'client_hold': client_hold_str,
                              'creator_login': my.user_name,
                              'order_code': order.get('code'),
                              'title_id_number': title_id_number, 
                              'territory': territory, 
                              'platform': platform, 
                              'order_name': order.get('name'),
                              'transfer_wo': ''
                              }
                            if wt.get('assigned_login_group') not in ['',None]:
                                task_data['assigned_login_group'] = wt.get('assigned_login_group')
                            if order:
                                if order.get('classification') in ['in_production','In Production']:
                                    task_data['active'] = True
                                task_data['po_number'] = order.get('po_number')
                            if work_group not in [None,'']:
                                task_data['assigned_login_group'] = work_group
                            pipe_dict['TITLE']['projs'][pro.get('process')]['processes'].append(wpro.get('process'))
                            pipe_dict['TITLE']['projs'][pro.get('process')]['work_orders'][wpro.get('process')] = {'data': wo_data, 'equipment': [], 'prereq': []}
                            pipe_dict['TITLE']['projs'][pro.get('process')]['tasks'][wpro.get('process')] = task_data
 

                            # Attach the templated equipment_used's
                            wot_eus_expr = "@SOBJECT(twog/equipment_used_templ['work_order_templ_code','%s'])" % wo_templ_code
                            wot_eus = my.server.eval(wot_eus_expr)
                            for eu in wot_eus:
                                name = eu.get('name')
                                equipment_code = eu.get('equipment_code')
                                description = eu.get('description')
                                expected_cost = eu.get('expected_cost')
                                expected_duration = eu.get('expected_duration')
                                expected_quantity = eu.get('expected_quantity')
                                eq_templ_code = eu.get('code')
                                units = eu.get('units')
                                ins_data = {'name': name, 'work_order_code': 'NEED TO FILL', 'equipment_code': equipment_code, 'description': description, 'expected_cost': expected_cost, 'expected_duration': expected_duration, 'expected_quantity': expected_quantity, 'units': units}
                                if eq_templ_code not in ['',None]:
                                    ins_data['equipment_used_templ_code'] = eq_templ_code
                                #server.insert('twog/equipment_used', ins_data)
                                pipe_dict['TITLE']['projs'][pro.get('process')]['work_orders'][wpro.get('process')]['equipment'].append(ins_data)
                                
                            # Attach the templated prereqs
                            wot_prereqs_expr = "@SOBJECT(twog/work_order_prereq_templ['work_order_templ_code','%s'])" % wo_templ_code
                            wot_prereqs = my.server.eval(wot_prereqs_expr)
                            for wp in wot_prereqs:
                                prereq = wp.get('prereq')
                                prereq_insert = {'prereq': prereq, 'from_title': False, 'login': my.user_name}
                                pipe_dict['TITLE']['projs'][pro.get('process')]['work_orders'][wpro.get('process')]['prereq'].append(prereq_insert)
                               # server.insert('twog/work_order_prereq', {'work_order_code': wo_insert.get('code'), 'prereq': prereq, 'from_title': False})
        title_codes_return = ''
        new_title_count = 0
        order_wo_count = order.get('wo_count')
        old_title_count = order.get('titles_total')
        if old_title_count in [None,'']:
            old_title_count = 0
        else:
            old_title_count = int(old_title_count)

        if order_wo_count in [None,'']:
            order_wo_count = 0
        else:
            order_wo_count = int(order_wo_count)
        for episode in my.episodes:
            my.data['episode'] = episode
            my.data['client_code'] = client_code
            my.data['client_name'] = client_name
            my.data['login'] = my.user_name
            my.data['is_external_rejection'] = 'false'
            title_obj = my.server.insert('twog/title', my.data, triggers=False)
            new_title_count = new_title_count + 1
            title_code = title_obj.get('code')
            wo_count = 0
            if title_codes_return == '':
                title_codes_return = title_code
            else:
                title_codes_return = '%s,%s' % (title_codes_return, title_code)
            for preq in pipe_dict['TITLE']['prereq']:
                preq['title_code'] = title_code
                preq['login'] = my.user_name
                my.server.insert('twog/title_prereq', preq, triggers=False)
                
            for pprocess in pipe_dict['TITLE']['processes']:
                proj_data = pipe_dict['TITLE']['projs'][pprocess]['data']
                ptask_data = pipe_dict['TITLE']['tasks'][pprocess]
                proj_data['title_code'] = title_code
                proj_data['title'] = title_obj.get('title')
                proj_data['episode'] = title_obj.get('episode')
                proj_data['login'] = my.user_name
                ptask_data['title_code'] = title_code
                ptask_data['title'] = title_obj.get('title')
                ptask_data['episode'] = title_obj.get('episode')
                ptask_data['search_id'] = title_obj.get('id')
                ptask_data['login'] = my.user_name
                proj = my.server.insert('twog/proj', proj_data, triggers=False)
                ptask = my.server.insert('sthpw/task', ptask_data, triggers=False)
                my.server.update(proj.get('__search_key__'), {'task_code': ptask.get('code')}, triggers=False)
                my.server.update(ptask.get('__search_key__'), {'lookup_code': proj.get('code')}, triggers=False)
                for wprocess in pipe_dict['TITLE']['projs'][pprocess]['processes']:
                    wo_data = pipe_dict['TITLE']['projs'][pprocess]['work_orders'][wprocess]['data']
                    wo_data['title_code'] = title_code
                    wo_data['proj_code'] = proj.get('code')
                    wo_data['title'] = title_obj.get('title')
                    wo_data['episode'] = title_obj.get('episode')
                    wo_data['login'] = my.user_name
                    wtask_data = pipe_dict['TITLE']['projs'][pprocess]['tasks'][wprocess]
                    wtask_data['title_code'] = title_code
                    wtask_data['proj_code'] = proj.get('code')
                    wtask_data['title'] = title_obj.get('title')
                    wtask_data['episode'] = title_obj.get('episode')
                    wtask_data['search_id'] = proj.get('id')
                    wtask_data['login'] = my.user_name
                    wo = my.server.insert('twog/work_order', wo_data, triggers=False)
                    wtask = my.server.insert('sthpw/task', wtask_data, triggers=False)
                    my.server.update(wo.get('__search_key__'), {'task_code': wtask.get('code')}, triggers=False)
                    my.server.update(wtask.get('__search_key__'), {'lookup_code': wo.get('code')}, triggers=False)
                    wo_count = wo_count + 1
                    order_wo_count = order_wo_count + 1
                    eq_info = ''
                    for eq in pipe_dict['TITLE']['projs'][pprocess]['work_orders'][wprocess]['equipment']:
                        eq['work_order_code'] = wo.get('code')
                        eq['client_code'] = client_code
                        eq['login'] = my.user_name
                        new_eq = my.server.insert('twog/equipment_used', eq, triggers=False)
                        if eq_info == '':
                            eq_info = '%sX|X%sX|X%sX|X' % (new_eq.get('code'), new_eq.get('name'), new_eq.get('units').upper())
                        else: 
                            eq_info = '%sZ,Z%sX|X%sX|X%sX|X' % (eq_info, new_eq.get('code'), new_eq.get('name'), new_eq.get('units').upper())
                    my.server.update(wo.get('__search_key__'), {'eq_info': eq_info})
                    for preq in pipe_dict['TITLE']['prereq']:
                        wpreq = {}
                        wpreq['work_order_code'] = wo.get('code')
                        wpreq['from_title'] = True 
                        wpreq['prereq'] = preq.get('prereq') 
                        wpreq['login'] = my.user_name
                        my.server.insert('twog/work_order_prereq', wpreq, triggers=False)
                    for pq in pipe_dict['TITLE']['projs'][pprocess]['work_orders'][wprocess]['prereq']:
                        pq['work_order_code'] = wo.get('code')
                        pq['login'] = my.user_name
                        my.server.insert('twog/work_order_prereq', pq, triggers=False)
            my.server.update(title_obj.get('__search_key__'), {'wo_count': wo_count}, triggers=False)
        now_title_count = old_title_count + new_title_count
        my.server.update(order.get('__search_key__'), {'wo_count': order_wo_count, 'titles_total': now_title_count}, triggers=False)
        return title_codes_return            
                    
                   
    #AT THE END, YOU NEED TO RUN SIMPLIFY_PIPES ON EACH TITLE PIPELINE - SEE IF THERE IS A SCRIPT ALREADY TO DO THAT

    def check_security(my):
        '''give the command a callback that allows it to check security'''
        return True

    def get_title(my):
        return "Create Titles"

class NormalPipeToHackPipeCmd(Command):
    def __init__(my, **kwargs):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        super(NormalPipeToHackPipeCmd, my).__init__(**kwargs)
        my.login = Environment.get_login()
        my.user_name = my.login.get_login() 
        my.server = TacticServerStub.get()
        my.sob_sk = kwargs.get('sob_sk')
        my.new_pipe = kwargs.get('new_pipe')
        my.sob_code = my.sob_sk.split('code=')[1]
        

    def check(my):
        return True
    
    def execute(my):   
        from pyasm.common import Common
        kids = []
        is_title = False
        expr = "@SOBJECT(twog/proj['title_code','%s'])" % my.sob_code
        if 'TITLE' in my.sob_sk:
            is_title = True
        elif 'PROJ' in my.sob_sk:
            expr = "@SOBJECT(twog/work_order['proj_code','%s'])" % my.sob_code
        kids1 = my.server.eval(expr)
        for k in kids1:
            if k.get('creation_type') != 'hackup':
                kids.append(k)
        kid_connections = {}
        kid_name_to_code = {}
        for kid in kids:
            kp = kid.get('process')
            kc = kid.get('code')
            if kp not in kid_name_to_code.keys():
                kid_name_to_code[kp] = kc
            kid_connections[kc] = {'out_to': [], 'comes_from': []}
        kid_codes = kid_connections.keys()
        kid_names = kid_name_to_code.keys()
        direct_from_parent = []
        to_next_pipe = []
        for kid in kids:
            kp = kid.get('process')
            kc = kid.get('code')
            info = my.server.get_pipeline_processes_info(my.sob_sk, related_process=kp)
            if 'input_processes' in info.keys():
                input_processes = info.get('input_processes')
                went_input = 0
                for i in input_processes:
                    if i in kid_names:
                        from_code = kid_name_to_code[i]
                        if from_code not in kid_connections[kc]['comes_from']:
                            kid_connections[kc]['comes_from'].append(from_code)    
                            went_input = went_input + 1
                if went_input == 0:
                    direct_from_parent.append(kc)
            else:
                direct_from_parent.append(kc)
            if 'output_processes' in info.keys():
                output_processes = info.get('output_processes')
                went_output = 0
                for i in output_processes:
                    if i in kid_names:
                        to_code = kid_name_to_code[i]
                        if to_code not in kid_connections[kc]['out_to']:
                            kid_connections[kc]['out_to'].append(to_code)    
                            went_output = went_output + 1
                if went_output == 0:
                    to_next_pipe.append(kc)
            else:
                to_next_pipe.append(kc)
        for code in kid_connections:
            connections = kid_connections[code]
            outs = connections['out_to']
            for out in outs:
                my.server.insert("twog/hackpipe_out", {'lookup_code': code, 'out_to': out}, triggers=False)
                if out in kid_connections.keys():
                    out_connections = kid_connections[out]
                    comes_from = out_connections['comes_from']
                    if kc in comes_from:
                        kid_connections[out]['comes_from'].remove(kc)
        for code in direct_from_parent:
            my.server.insert("twog/hackpipe_out", {'lookup_code': my.sob_code, 'out_to': code}, triggers=False)
        for kid in kids:
            kid_task = my.server.eval("@SOBJECT(sthpw/task['lookup_code','%s'])" % kid.get('code'))
            if kid_task:
                my.server.update(kid_task[0].get('__search_key__'), {'pipeline_code': 'Manually Inserted into %s' % my.new_pipe})
            if is_title:
                my.server.update(kid.get('__search_key__'),{'proj_templ_code': '', 'templ_me': False, 'creation_type': 'hackup', 'parent_pipe': 'Manually Inserted into %s' % my.new_pipe}, triggers=False)
            else:
                my.server.update(kid.get('__search_key__'), {'work_order_templ_code': '', 'pipeline_code': '', 'parent_pipe': 'Manually Inserted into %s' % my.new_pipe, 'templ_me': False, 'creation_type': 'hackup'}, triggers=False)
        if len(to_next_pipe) > 0:
            my.server.update(my.sob_sk, {'append_connectors': ','.join(to_next_pipe)}, triggers=False)
        return True
                    
                   
    #AT THE END, YOU NEED TO RUN SIMPLIFY_PIPES ON EACH TITLE PIPELINE - SEE IF THERE IS A SCRIPT ALREADY TO DO THAT

    def check_security(my):
        '''give the command a callback that allows it to check security'''
        return True

    def get_title(my):
        return "Create Titles"

class UpdateNotesSeenByCmd(Command): 
    def execute(my):
        import subprocess
        #os.system('python /opt/spt/custom/reports/dashboard_reports/dashboard_report.py admin 10 20 > /tmp/spitout')
        subprocess.Popen(["python", "/opt/spt/custom/manual_updaters/add_seen_bys.py", "%s" % my.kwargs.get('login'), "%s" % my.kwargs.get('codes_to_update'), "%s" % my.kwargs.get('timestamp')])

































































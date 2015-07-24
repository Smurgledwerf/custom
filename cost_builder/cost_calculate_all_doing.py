import tacticenv, time
from client.tactic_client_lib import TacticServerStub
doing = open('what_have_i_done', 'w')
server = TacticServerStub.get(protocol="xmlrpc")
#server.start('CALCULATING COSTS')
orders = server.eval("@SOBJECT(twog/order['@ORDER_BY','code desc']['id','<','%s'])" % 12044)
#print "orders = %s" % orders
for order in orders:
    id = int(order.get('code').split('ORDER')[1].lstrip('0'))
    sk = ''
    order_code = order.get('code')
    #print "ORDER CODE = %s" % order_code
    doing.write('\t\t\t\t\tORDER CODE: %s\n' % order_code)
    order = server.eval("@SOBJECT(twog/order['code','%s'])" % order_code)[0]
    order_dict = {'actual_cost': 0, 'expected_cost': 0, 'titles':{}}
    #time.sleep(1)
    titles = server.eval("@SOBJECT(twog/title['order_code','%s'])" % order_code)
    for title in titles:
	title_code = title.get('code')
	order_dict['titles'][title_code] = {'actual_cost': 0, 'expected_cost': 0, 'projs': {}}
        #time.sleep(1)
	projs = server.eval("@SOBJECT(twog/proj['title_code','%s'])" % title_code)
	for proj in projs:
	    proj_code = proj.get('code')
	    order_dict['titles'][title_code]['projs'][proj_code] = {'actual_cost': 0, 'expected_cost': 0, 'wos': {}}
            #time.sleep(1)
	    wos = server.eval("@SOBJECT(twog/work_order['proj_code','%s'])" % proj_code)
	    for wo in wos:
		wo_code = wo.get('code')
		estimated_work_hours = wo.get('estimated_work_hours')
		work_group = wo.get('work_group')
		new_expected_cost = 0
		if work_group not in [None,''] and estimated_work_hours not in [None,'',0,'0']:
		    estimated_work_hours = float(estimated_work_hours)
		    group = server.eval("@SOBJECT(sthpw/login_group['login_group','%s'])" % work_group)
		    if group:
			group = group[0]
			group_rate = group.get('hourly_rate')
			if group_rate not in [None,'']:
			    group_rate = float(group_rate)
			    new_expected_cost = float(group_rate * estimated_work_hours)
                            if new_expected_cost < 0:
                                print "NEGATIVE!? WHAT!? [%s] WO_CODE = %s, WORK GROUP = %s, EST_WH = %s, GROUP = %s, GROUP_RATE = %s" % (new_expected_cost, wo_code, estimated_work_hours, group.get('login_group'), group_rate)
		order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code] = {'actual_cost': 0, 'expected_cost': new_expected_cost, 'whs': {}, 'eqs': {}}
		order_dict['titles'][title_code]['projs'][proj_code]['expected_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['expected_cost']) + new_expected_cost
		order_dict['titles'][title_code]['expected_cost'] = float(order_dict['titles'][title_code]['expected_cost']) + new_expected_cost
		order_dict['expected_cost'] = float(order_dict['expected_cost']) + new_expected_cost
		task = server.eval("@SOBJECT(sthpw/task['lookup_code','%s'])" % wo_code)
		if task:
		    task = task[0]
		    task_code = task.get('code')
		    whs = server.eval("@SOBJECT(sthpw/work_hour['task_code','%s'])" % task_code)
		    for wh in whs:
			wh_code = wh.get('code')
			# make cost here
			cost_to_add = 0
			user = wh.get('login')
			straight_time = wh.get('straight_time')
			if straight_time in [None,'']:
			    straight_time = float(0)
			else:
			    straight_time = float(straight_time)
			assigned_login_group = task.get('assigned_login_group')
			user_groups = server.eval("@SOBJECT(sthpw/login_in_group['login','%s']['login_group','not in','client|user|admin'])" % user)
			found = False
			group_rate = 0
			group_chosen = ''
			group_bool = True
			for ug in user_groups:
			    group = server.eval("@SOBJECT(sthpw/login_group['login_group','%s'])" % ug.get('login_group'))
			    if group:
				group = group[0]
			    else:
				group_bool = False
			    if group_bool:
				this_rate = group.get('hourly_rate')
				if this_rate not in [None,'']:
				    this_rate = float(this_rate)
				    if this_rate > group_rate:
					group_rate = this_rate
					group_chosen = ug.get('login_group')
			if group_bool:
			    cost_to_add = float(group_rate * straight_time)
			    doing.write('To %s, adding from work hour cost (%s) %s\n' % (wo_code, wh_code, cost_to_add))
			    order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['whs'][wh_code] = {'actual_cost': cost_to_add}
			    #Force the cost up here
			    order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['actual_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['actual_cost']) + cost_to_add
			    order_dict['titles'][title_code]['projs'][proj_code]['actual_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['actual_cost']) + cost_to_add
			    order_dict['titles'][title_code]['actual_cost'] = float(order_dict['titles'][title_code]['actual_cost']) + cost_to_add
			    order_dict['actual_cost'] = float(order_dict['actual_cost']) + cost_to_add
		    eqs = server.eval("@SOBJECT(twog/equipment_used['work_order_code','%s'])" % wo_code)
		    for equip in eqs:
			eq_u_code = equip.get('code')
			#######
			eq_code = equip.get('equipment_code')
			eq_expr = "@SOBJECT(twog/equipment['code','%s'])" % eq_code
			eq = server.eval(eq_expr)
			throwin_data = {'actual_cost': 0, 'expected_cost': 0}
			if eq:
			    eq = eq[0]
			    lengths = eq.get('lengths')
			    if lengths not in [None,'']:
				if equip.get('length') not in [None,'']:
				    sob_len = equip.get('length')
				    eq_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['length','%s'])" % (eq_code, sob_len)
				    eq_cost = server.eval(eq_cost_expr)
				    if eq_cost:
					eq_cost = eq_cost[0]
					cost = eq_cost.get('cost')
					if cost in [None,'']:
					    cost = 0
					cost = float(cost)
					quant = equip.get('expected_quantity')
					if quant in [None,'',0,'0']:
					    throwin_data['expected_quantity'] = 1
					    quant = 1
					quant = float(quant)
					set_cost = float(cost * quant)
					if set_cost > 0:
					    throwin_data['expected_cost'] = set_cost
					    throwin_data['actual_cost'] = set_cost
			    else:
				units = equip.get('units')
				divisor = 1
				if units in [None,'','items']:
				    units = 'hr'
				    throwin_data['units'] = 'hr'
				if units == 'mb':
				    units == 'gb'
				    divisor = .01
				if ('E_DELIVERY' in equip.get('name') or 'STORAGE' in equip.get('name')) and units in ['hr','items']:
				    units = 'gb'
				    server.update(equip.get('__search_key__'), {'units': 'gb'}, triggers=False)
				    doing.write("Switching %s's units to gb from %s\n" % (equip.get('code'), equip.get('units')))
				    #time.sleep(1)
				actual_quant = expected_quant = equip.get('expected_quantity')
				expected_dur = equip.get('expected_duration')
				if expected_dur in [None,'',0,'0']:
				    expected_dur = 1
				    throwin_data['expected_duration'] = 1
				actual_dur = equip.get('actual_duration')
				if actual_dur in [None,'',0,'0']:
				    actual_dur = 0
				expected_dur = float(expected_dur)
				actual_dur = float(actual_dur)
				if expected_quant in [None,'','0',0]:
				    actual_quant = expected_quant = 1
				    throwin_data['actual_quantity'] = 1
				    throwin_data['expected_quantity'] = 1
				actual_quant = expected_quant = float(expected_quant)
				eq_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['unit','%s'])" % (eq_code, units)
				eq_cost = server.eval(eq_cost_expr)
				if eq_cost:
				    eq_cost = eq_cost[0]
				    cost = eq_cost.get('cost')
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
				    throwin_data['expected_cost'] = expected_cost
				    throwin_data['actual_cost'] = actual_cost
			if throwin_data != {}:
			    server.update(equip.get('__search_key__'), throwin_data, triggers=False)    
			    doing.write('UPDATING COSTS for %s. Expected = %s, Actual = %s\n' % (equip.get('code'), throwin_data['expected_cost'], throwin_data['actual_cost']))
			    #time.sleep(1)
			order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['eqs'][eq_u_code] = {'actual_cost': throwin_data['actual_cost'], 'expected_cost': throwin_data['expected_cost']} 
			if throwin_data['actual_cost'] > 0:
			    order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['actual_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['actual_cost']) + float(throwin_data['actual_cost'])
			    order_dict['titles'][title_code]['projs'][proj_code]['actual_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['actual_cost']) + float(throwin_data['actual_cost'])
			    order_dict['titles'][title_code]['actual_cost'] = float(order_dict['titles'][title_code]['actual_cost']) + float(throwin_data['actual_cost'])
			    order_dict['actual_cost'] = float(order_dict['actual_cost']) + float(throwin_data['actual_cost'])
			if throwin_data['expected_cost'] > 0:
			    order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['expected_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['expected_cost']) + float(throwin_data['expected_cost'])
			    order_dict['titles'][title_code]['projs'][proj_code]['expected_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['expected_cost']) + float(throwin_data['expected_cost'])
			    order_dict['titles'][title_code]['expected_cost'] = float(order_dict['titles'][title_code]['expected_cost']) + float(throwin_data['expected_cost'])
			    order_dict['expected_cost'] = float(order_dict['expected_cost']) + float(throwin_data['expected_cost'])
		#Update the wo costs here
		wo_actual = float(order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['actual_cost'])
		wo_expected = float(order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['expected_cost'])
		server.update(wo.get('__search_key__'), {'expected_cost': wo_expected, 'actual_cost': wo_actual}, triggers=False)
		doing.write('UPDATING %s Costs. Expected = %s, Actual = %s\n' % (wo_code, wo_expected, wo_actual))
		#time.sleep(1)
	    #Update the proj costs here
	    proj_actual = float(order_dict['titles'][title_code]['projs'][proj_code]['actual_cost'])
	    proj_expected = float(order_dict['titles'][title_code]['projs'][proj_code]['expected_cost'])
	    server.update(proj.get('__search_key__'), {'expected_cost': proj_expected, 'actual_cost': proj_actual}, triggers=False)
	    doing.write('UPDATING %s Costs. Expected = %s, Actual = %s\n' % (proj_code, proj_expected, proj_actual))
	    #time.sleep(1)
	#Update the title costs here
	title_actual = float(order_dict['titles'][title_code]['actual_cost'])
	title_expected = float(order_dict['titles'][title_code]['expected_cost'])
	server.update(title.get('__search_key__'), {'expected_cost': title_expected, 'actual_cost': title_actual}, triggers=False)
	doing.write('UPDATING %s Costs. Expected = %s, Actual = %s\n' % (title_code, title_expected, title_actual))
	#time.sleep(1)
    #Update the order costs here            
    order_actual = float(order_dict['actual_cost'])
    order_expected = float(order_dict['expected_cost'])
    server.update(order.get('__search_key__'), {'expected_cost': order_expected, 'actual_cost': order_actual}, triggers=False)
    doing.write('UPDATING %s Costs. Expected = %s, Actual = %s\n' % (order.get('code'), order_expected, order_actual))
    #time.sleep(1)
#server.finish()
doing.close()

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
        # CUSTOM_SCRIPT00090
        #THIS IS RUN WHENEVER A PROJ OR WO IS INSERTED OR DELETED (IN AN ACTIVE ORDER), OR WHEN HACKPIPE_OUTs ARE INSERTED OR DELETED
        def hackpipes_preceding(sob):
            boolio = False
            matcher = ''
            if 'PROJ' in sob.get('code'):
                matcher = 'PROJ'
            elif 'WORK_ORDER' in sob.get('code'):
                matcher = 'WORK_ORDER'
            hacks_expr = "@SOBJECT(twog/hackpipe_out['out_to','%s'])" % sob.get('code')
            hacks = server.eval(hacks_expr)
            lookups = []
            if len(hacks) > 0:
                boolio = True
                for h in hacks:
                    lookup_code = h.get('lookup_code')
                    if matcher in lookup_code:
                        lookups.append(lookup_code)
            return lookups
        
        def kill_nonexistent_dudes(names_arr, info_arr):
            out_arr = []
            for i in info_arr:
                if i in names_arr:
                    out_arr.append(i)
            return out_arr
        
        def recurse_for_nums(proj_outs, proj_nums, code, num):
            proj_num_backup = proj_nums
            try:
                if code in proj_outs.keys():
                    nexts = proj_outs[code].split('|^|')
                    for next in nexts:
                        next = next.split(',')[0].replace('[','').replace(']','')
                        proj_nums[next] = num + 1
                    for next in nexts:
                        next = next.split(',')[0].replace('[','').replace(']','')
                        proj_num_temp = recurse_for_nums(proj_outs, proj_nums, next, num + 1)
                        if not proj_num_temp:
                            return proj_nums
                        else:
                            return proj_num_temp
                else:
                    return proj_nums
            except:
                return proj_num_backup
        
        
        sobject = input.get('sobject')
        sob_code = sobject.get('code')
        title_code = ''
        order_code = ''
        classification = ''
        order = None
        this_is_an_order = False
        titles = []
        projs = []
        do_all = False
        #print "IN SIMPLIFY PIPE"
        #print "SOBJECT = %s" % sobject
        if 'SIMPLIFY_PIPE' in sob_code:
            doAll = sobject.get('do_all')
            if doAll in ['yes','Yes','y','1',1]:
                do_all = True
            temp_sob2 = None
            for k in sobject.keys():
                if k in ['order_code','title_code','proj_code','work_order_code']:
                    if sobject[k] not in [None,'',0]:
                        temp_sob = server.eval("@SOBJECT(twog/%s['code','%s'])" % (k.split('_code')[0], sobject[k]))
                        if temp_sob:
                            temp_sob2 = temp_sob[0]
            if temp_sob2:
                sobject = temp_sob2
                sob_code = sobject.get('code')
        #print "SOB_CODE = %s" % sob_code
        #print "SOB_CODE = %s, SOBJECT = %s" % (sob_code, sobject)
        if 'ORDER' in sob_code and '_' not in sob_code: #THIS MEANS THE WHOLE ORDER WILL BE NEW-PIPED, IF "In Production"
            classification = sobject.get('classification')
            #classification = 'In Production' #remove this line after doing nighttime update
            this_is_an_order = True
        if 'TITLE' in sob_code: #THIS COMES FROM DELETION OF A PROJECT
            titles = [sob_code]
            order = server.eval("@SOBJECT(twog/order['code','%s'])" % sobject.get('order_code'))[0]
            classification = order.get('classification')
            pexpr = "@GET(twog/proj['title_code','%s'].code)" % sob_code
            projs = server.eval(pexpr)
        if 'PROJ' in sob_code or 'WORK_ORDER' in sob_code or classification == 'In Production':
            if classification == '':
                order_code = sobject.get('order_code')
                order = server.eval("@SOBJECT(twog/order['code','%s'])" % order_code)[0]
                classification = order.get('classification')
                titles = [sobject.get('title_code')]
                if 'PROJ' in sob_code and not do_all:
                    projs = [sob_code] 
                elif 'WORK_ORDER' in sob_code:
                    projs = [sobject.get('proj_code')] 
                elif do_all: #THEN WE WANT TO DO ALL OF THE PROJS
                    projs = server.eval("@GET(twog/proj['order_code','%s'].code)" % order_code)
            elif classification == 'In Production' and 'TITLE' not in sob_code:
                order = sobject
                order_code = order.get('code')
                titles = server.eval("@GET(twog/title['order_code','%s'].code)" % order_code)
                projs = server.eval("@GET(twog/proj['order_code','%s'].code)" % order_code)
                
            if classification == 'In Production':
                proj_nums = {}
                if 'PROJ' in sob_code or this_is_an_order or ('TITLE' in sob_code and classification == 'In Production'):
                    if 'PROJ' in sob_code:
                        projs = [sob_code]
                    if len(titles) > 0:
                        for title_code in titles:
                            #print "TITLE CODE = %s" % title_code
                            title = server.eval("@SOBJECT(twog/title['code','%s'])" % title_code)[0]
                            title_sk = title.get('__search_key__')
                            proj_outs = {}
                            proj_ins = {}
                            names = {}
                            task_codes = {}
                            sks = {}
                            proj_nums = {}
                            all_projs = server.eval("@SOBJECT(twog/proj['title_code','%s'])" % title_code)
                            #print "ALL PROJS = %s" % all_projs
                            if len(all_projs) > 0:
                                for p in all_projs:
                                    #print "PROJ = %s" % p
                                    names[p.get('process')] = p.get('code')
                                    task_codes[p.get('code')] = p.get('task_code')
                                    sks[p.get('code')] = p.get('__search_key__')
                                #print "NAMES = %s\nTASK CODES = %s\nSKS = %s" % (names, task_codes, sks)
                                for p in all_projs:
                                    #print "Proj = %s" % p
                                    comes_from = p.get('comes_from')
                                    goes_to = p.get('goes_to')
                                    if p.get('code') not in proj_nums.keys():
                                        proj_nums[p.get('code')] = 1000
                                    info = server.get_pipeline_processes_info(title_sk, related_process=p.get('process'))
                                    input_processes = []
                                    if 'input_processes' in info.keys():
                                        input_processes = kill_nonexistent_dudes(names.keys(), info.get('input_processes'))
                                    output_processes = []
                                    if 'output_processes' in info.keys():
                                        output_processes = kill_nonexistent_dudes(names.keys(), info.get('output_processes'))
                                    for op in output_processes:
                                        if p.get('code') not in proj_outs.keys():
                                            proj_outs[p.get('code')] = '%s,%s' % (names[op], task_codes[names[op]])
                                        else:
                                            if names[op] not in proj_outs[p.get('code')]:
                                                proj_outs[p.get('code')] = '%s|^|%s,%s' % (proj_outs[p.get('code')] ,names[op], task_codes[names[op]])
                                    for ip in input_processes:
                                        if p.get('code') not in proj_ins.keys():
                                            proj_ins[p.get('code')] = '%s,%s' % (names[ip], task_codes[names[ip]])
                                        else:
                                            if names[ip] not in proj_ins[p.get('code')]:
                                                proj_ins[p.get('code')] = '%s|^|%s,%s' % (proj_ins[p.get('code')] ,names[ip], task_codes[names[ip]])
                                    hacks = hackpipes_preceding(p)
                                    for h in hacks:
                                        if h not in proj_outs.keys():
                                            proj_outs[h] = '%s,%s' % (p.get('code'), p.get('task_code'))
                                        else:
                                            if p.get('code') not in proj_outs[h]:
                                                proj_outs[h] = '%s|^|%s,%s' % (proj_outs[h], p.get('code'), p.get('task_code'))
                                        if p.get('code') not in proj_ins.keys():
                                            proj_ins[p.get('code')] = '%s,%s' % (h, task_codes[h])
                                        else:
                                            if h not in proj_ins[p.get('code')]:
                                                proj_ins[p.get('code')] = '%s|^|%s,%s' % (proj_ins[p.get('code')], h, task_codes[h])
                                    if len(input_processes) == 0 and len(hacks) == 0 and comes_from in [None,'']:
                                        proj_nums[p.get('code')] = 0
                                title_lookup_str = ''
                                for pn in proj_nums.keys():
                                    if proj_nums[pn] == 0:
                                        proj_nums = recurse_for_nums(proj_outs, proj_nums, pn, 0)
                                conflicts = {}
                                for pn in proj_nums.keys():
                                    thenum = proj_nums[pn]
                                    if thenum not in conflicts.keys():
                                        conflicts[thenum] = [pn]
                                    else:
                                        conflicts[thenum].append(pn)
                                for c in conflicts.keys():
                                    theset = conflicts[c]
                                    if theset not in [None,'',[]]:
                                        if len(theset) > 1:
                                            for guy in theset:
                                                for dude in theset:
                                                    if guy != dude:
                                                        if guy in proj_ins.keys():
                                                            if dude in proj_ins[guy]:
                                                                proj_nums[dude] = proj_nums[dude] - .1
                                for pn in proj_nums:
                                    proj_nums[pn] = proj_nums[pn] + 1
                                    proj_nums[pn] = proj_nums[pn] * 10
                                for po in proj_nums.keys():
                                    #print "4.. PO = %s" % po
                                    outs = ''
                                    if po in proj_outs.keys():
                                        outs = proj_outs[po]
                                    ins = ''
                                    if po in proj_ins.keys():
                                        ins = proj_ins[po]
                                    #print "SKS = %s" % sks
                                    server.update(sks[po], {'goes_to': outs, 'comes_from': ins, 'order_in_pipe': int(proj_nums[po])}, triggers=False)
                                    try:
                                        server.update(server.build_search_key('sthpw/task', task_codes[po]), {'goes_to': outs, 'comes_from': ins, 'order_in_pipe': int(proj_nums[po])}, triggers=False)
                                    except:
                                        pass
                                    title_lookup_str = '%s[%s]=>%s*END*' % (title_lookup_str, po, outs)
                                server.update(title_sk, {'pipe_str': title_lookup_str}, triggers=False)
                                #WILL NEED HACKPIPE_OUT INSERTION TRIGGER TO READDRESS THE PIPE_STR (Title) and GOES_TO (Proj), so the new pipelines will be complete
                #print "PRE WO"
                if 'WORK_ORDER' in sob_code or this_is_an_order or do_all:
                    if len(projs) > 0:
                        for proj_code in projs:
                            wo_nums = {}
                            wo_outs = {}
                            wo_ins = {}
                            names = {}
                            task_codes = {}
                            sks = {}
                            proj_sk = server.build_search_key('twog/proj', proj_code)
                            all_wos = server.eval("@SOBJECT(twog/work_order['proj_code','%s'])" % proj_code)
                            if len(all_wos) > 0:
                                for w in all_wos:
                                    names[w.get('process')] = w.get('code')
                                    task_codes[w.get('code')] = w.get('task_code')
                                    sks[w.get('code')] = w.get('__search_key__')
                                for w in all_wos:
                                    comes_from = w.get('comes_from')
                                    goes_to = w.get('goes_to')
                                    if w.get('code') not in wo_nums.keys():
                                        wo_nums[w.get('code')] = 1000
                                    info = server.get_pipeline_processes_info(proj_sk, related_process=w.get('process'))
                                    input_processes = []
                                    if 'input_processes' in info.keys():
                                        input_processes = kill_nonexistent_dudes(names.keys(), info.get('input_processes'))
                                    output_processes = []
                                    if 'output_processes' in info.keys():
                                        output_processes = kill_nonexistent_dudes(names.keys(), info.get('output_processes'))
                                    for op in output_processes:
                                        if w.get('code') not in wo_outs.keys():
                                            wo_outs[w.get('code')] = '[%s,%s]' % (names[op], task_codes[names[op]])
                                        else:
                                            if names[op] not in wo_outs[w.get('code')]:
                                                wo_outs[w.get('code')] = '%s|^|[%s,%s]' % (wo_outs[w.get('code')] ,names[op], task_codes[names[op]])
                                    for ip in input_processes:
                                        if w.get('code') not in wo_ins.keys():
                                            wo_ins[w.get('code')] = '[%s,%s]' % (names[ip], task_codes[names[ip]])
                                        else:
                                            if names[ip] not in wo_ins[w.get('code')]:
                                                wo_ins[w.get('code')] = '%s|^|[%s,%s]' % (wo_ins[w.get('code')] ,names[ip], task_codes[names[ip]])
                                    hacks = hackpipes_preceding(w)
                                    for h in hacks:
                                        if h not in wo_outs.keys():
                                            wo_outs[h] = '[%s,%s]' % (w.get('code'), w.get('task_code'))
                                        else:
                                            if w.get('code') not in wo_outs[h]:
                                                wo_outs[h] = '%s|^|[%s,%s]' % (wo_outs[h], w.get('code'), w.get('task_code'))
                                        if w.get('code') not in wo_ins.keys():
                                            tc = ''
                                            if h in task_codes.keys():
                                                tc = task_codes[h]
                                            wo_ins[w.get('code')] = '[%s,%s]' % (h, tc)
                                        else:
                                            if h not in wo_ins[w.get('code')]:
                                                tc = ''
                                                if h in task_codes.keys():
                                                    tc = task_codes[h]
                                                wo_ins[w.get('code')] = '%s|^|[%s,%s]' % (wo_ins[w.get('code')], h, tc)
                                    if len(input_processes) == 0 and len(hacks) == 0 and comes_from in [None,'']:
                                        wo_nums[w.get('code')] = 0
                                proj_lookup_str = ''
                                for wn in wo_nums.keys():
                                    if wo_nums[wn] == 0:
                                        wo_nums = recurse_for_nums(wo_outs, wo_nums, wn, 0)
                                conflicts = {}
                                for wn in wo_nums.keys():
                                    thenum = wo_nums[wn]
                                    if thenum not in conflicts.keys():
                                        conflicts[thenum] = [wn]
                                    else:
                                        conflicts[thenum].append(wn)
                                for c in conflicts.keys():
                                    theset = conflicts[c]
                                    if theset not in [None,'',[]]:
                                        if len(theset) > 1:
                                            for guy in theset:
                                                for dude in theset:
                                                    if guy != dude:
                                                        if guy in wo_ins.keys():
                                                            if dude in wo_ins[guy]:
                                                                wo_nums[dude] = wo_nums[dude] - .1
                                for wn in wo_nums:
                                    wo_nums[wn] = wo_nums[wn] + 1
                                    wo_nums[wn] = wo_nums[wn] * 10
                                for wo in wo_nums.keys():
                                    outs = ''
                                    if wo in wo_outs.keys():
                                        outs = wo_outs[wo]
                                    ins = ''
                                    if wo in wo_ins.keys():
                                        ins = wo_ins[wo]
                                    if proj_code in proj_nums.keys():
                                        scalar = int(proj_nums[proj_code])
                                    else:
                                        scalar = server.eval("@GET(twog/proj['code','%s'].order_in_pipe)" % proj_code)[0]
                                        if scalar in [None,'',0]:
                                            scalar = 1
                                        else:
                                            scalar = int(scalar)
                                    scalar = scalar * 1000
                                    oip = int(int(wo_nums[wo]) + scalar)
                                    server.update(sks[wo], {'goes_to': outs, 'comes_from': ins, 'order_in_pipe': oip}, triggers=False)
                                    try:
                                        server.update(server.build_search_key('sthpw/task', task_codes[wo]), {'goes_to': outs, 'comes_from': ins, 'order_in_pipe': int(wo_nums[wo])}, triggers=False)
                                    except:
                                        pass
                                    proj_lookup_str = '%s[%s]=>%s*END*' % (proj_lookup_str, wo, outs)
                                server.update(proj_sk, {'pipe_str': proj_lookup_str}, triggers=False)
                                #WILL NEED HACKPIPE_OUT INSERTION TRIGGER TO READDRESS THE PIPE_STR (Proj) and GOES_TO (Work Order), so the new pipelines will be complete
            
        #print "LEAVING SIMPLIFY_PIPE"
    except AttributeError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the server object does not exist.'
    except KeyError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the input dictionary does not exist.'
    except Exception as e:
        traceback.print_exc()
        print str(e)


if __name__ == '__main__':
    main()

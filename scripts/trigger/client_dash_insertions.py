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
        # CUSTOM_SCRIPT00088
        #MTM THIS TRIGGER IS NOT USED AT ALL ANYMORE. HASN'T BEEN UPDATED IN A LONG TIME.
        def increment_or_create(obj, code, client_code, client_username, variable_type, variable_suffix, inc_val):
            if obj:
                obj = obj[0]
                parse_vals = obj.get('parse_vals')
                value = obj.get('value')
                if code not in parse_vals:
                    new_parse = ''
                    new_value = 0
                    if parse_vals in [None,'']:
                        new_parse = code
                        if inc_val == 1:
                            new_value = 1
                        else:
                            new_value = 0
                    else:
                        if inc_val == 1:
                            new_parse = '%s,%s' % (parse_vals, code)
                        else:
                            new_parse = parse_vals.replace(',%s' % code,'').replace('%s,' % code, '').replace(code,'')
                        new_value = value + inc_val
                    server.update(obj.get('__search_key__'), {'parse_vals': new_parse, 'value': new_value})
            elif inc_val == 1:
                server.insert('twog/client_rep_dash', {'client_code': client_code, 'login_name': client_username, 'name': '%s_%s' % (variable_type, variable_suffix), 'value': 1, 'parse_vals': code})
        
        sobject = input.get('sobject')
        code = sobject.get('code')
        client_code = sobject.get('client_code')
        stop_it = False
        if client_code not in [None,'']:
            order = None
            variable_type = ''
            if 'TITLE' in code: 
                order = server.eval("@SOBJECT(twog/order['code','%s'])" % sobject.get('order_code'))[0]
                variable_type = 'title'
            elif 'ORDER' in code:
                order = sobject
                variable_type = 'order'
                if order.get('classification').lower() == 'master':
                    stop_it = True
            if 'update_data' in input.keys() and not stop_it:
                switch_client = False
                old_client_code = sobject.get('client_code')
                old_client_username = ''
                if 'update_data' in input.keys():
                    update_data = input.get('update_data') 
                    if 'client_code' in update_data.keys() or 'client_rep' in update_data.keys():
                        switch_client = True
                        prev_data = input.get('prev_data')
                        old_client_code = prev_data.get('client_code')
                        if variable_type == 'order':
                            old_client_rep_p = sobject.get('client_rep')
                            if 'client_rep' in update_data.keys():
                                old_client_rep_p = sobject.get('client_rep')
                                if old_client_rep_p not in [None,'']:
                                    old_client_person = server.eval("@SOBJECT(twog/person['code','%s'])" % old_client_rep_p)[0]
                                    old_client_username = old_client_person.get('login_name') 
                                    switch_client = True
                                else:
                                    switch_client = False
            if not stop_it:
                client_rep = order.get('client_rep')
                client_person = server.eval("@SOBJECT(twog/person['code','%s'])" % client_rep)[0]
                client_username = client_person.get('login_name') 
                if old_client_username in [None,'']:
                    old_client_username = client_username
                if old_client_code in [None,'']:
                    old_client_code = client_code
                if client_username not in [None,'']:
                    #Insert or update of orders/titles needs to add order_code to parse_vals as comma separated string and increment corresponding float value by 1 if not already in parse_vals string
                    total_row = server.eval("@SOBJECT(twog/client_rep_dash['client_code','%s']['login_name','%s']['name','%s_total'])" % (client_code, client_username, variable_type))
                    increment_or_create(total_row, code, client_code, client_username, variable_type, 'total', 1) 
                    if switch_client:
                        increment_or_create(total_row, code, old_client_code, old_client_username, variable_type, 'total', -1) 
                    if variable_type == 'order':  
                        #Do updates for orders regarding classification, "closedness", updates per platform, total $, total_owed
                        classification = sobject.get('classification').lower().replace(' ','_')
                        class_row = server.eval("@SOBJECT(twog/client_rep_dash['client_code','%s']['login_name','%s']['name','%s_classification'])" % (client_code, client_username, classification))
                        increment_or_create(class_row, code, client_code, client_username, variable_type, '%s_classification' % classification, 1) 
                        if switch_client:
                            old_class_row = server.eval("@SOBJECT(twog/client_rep_dash['client_code','%s']['login_name','%s']['name','%s_classification'])" % (old_client_code, old_client_username, classification))
                            increment_or_create(old_class_row, code, old_client_code, old_client_username, variable_type, '%s_classification' % classification, -1) 
                    elif variable_type == 'title':  
                        #Do updates for orders regarding status, updates per platform
                        status = sobject.get('status').lower().replace(' ','_')
                        status_row = server.eval("@SOBJECT(twog/client_rep_dash['client_code','%s']['login_name','%s']['name','%s_status'])" % (client_code, client_username, status))
                        increment_or_create(status_row, code, client_code, client_username, variable_type, '%s_status' % status, 1) 
                        if switch_client:
                            old_status_row = server.eval("@SOBJECT(twog/client_rep_dash['client_code','%s']['login_name','%s']['name','%s_status'])" % (old_client_code, old_client_username, status))
                            increment_or_create(old_status_row, code, old_client_code, old_client_username, variable_type, '%s_status' % status, -1) 
                    
                    platform = sobject.get('platform')
                    if platform not in [None,'']:
                        platform = platform.replace(' ','_')
                        platform_row = server.eval("@SOBJECT(twog/client_rep_dash['client_code','%s']['login_name','%s']['name','%s_platform'])" % (client_code, client_username, platform))
                        increment_or_create(platform_row, code, client_code, client_username, variable_type, '%s_platform' % platform, 1) 
                        if switch_client:
                            old_platform_row = server.eval("@SOBJECT(twog/client_rep_dash['client_code','%s']['login_name','%s']['name','%s_platform'])" % (old_client_code, old_client_username, platform))
                            increment_or_create(old_platform_row, code, old_client_code, old_client_username, variable_type, '%s_platform' % platform, -1)
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

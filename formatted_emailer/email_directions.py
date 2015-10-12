import tacticenv, os
from tactic_client_lib import TacticServerStub
import common_tools.utils as ctu
#This is to collect the correct data for emails and to determine who they should go to
class EmailDirections():
    def __init__(my, *args, **kwargs):
        #Pass in order_code, client_code (optional), client_login (optional), logged_in (optional)
        my.server = TacticServerStub.get()
        my.order = None
        my.client_name = '' 
        my.order_code = kwargs.get('order_code')
        my.order = my.server.eval("@SOBJECT(twog/order['code','%s'])" % my.order_code)[0]
        my.client = None
        my.client_code = None #my.kwargs.get('client_code')
        my.client_name = my.order.get('client_name')
        my.client_email = ''
        if my.client_code in [None,'']:
            my.client_code = my.order.get('client_code')
        if my.client_code not in [None,'']:
            my.client = my.server.eval("@SOBJECT(twog/client['code','%s'])" % my.client_code)[0]
            if my.client_name in [None,'']:
                my.client_name = my.client.get('name')
        my.client_login_obj = None
        my.client_login = '' #my.kwargs.get('client_login')
        if my.client_login in [None,'']:
            my.client_login = my.order.get('client_login')
        my.client_login_obj = my.server.eval("@SOBJECT(sthpw/login['login','%s'])" % my.client_login)
        if my.client_login_obj:
            my.client_login_obj = my.client_login_obj[0]
        else:
            rep_person = my.order.get('client_rep')
            if rep_person not in [None,'']:
                rep = my.server.eval("@SOBJECT(twog/person['code','%s'])" % rep_person)
                if rep:
                    rep = rep[0]
                    rep_login = rep.get('login_name')
                    if rep_login not in [None,'']:
                        my.client_login_obj = my.server.eval("@SOBJECT(sthpw/login['login','%s'])" % rep_login)
                        if my.client_login_obj:
                            my.client_login_obj = my.client_login_obj[0]
        my.client_email = ''
        if my.client_login_obj:
            my.client_email = my.client_login_obj.get('email')
        my.logged_in = None #my.kwargs.get('logged_in')
        if my.logged_in in [None,'']:
            from pyasm.common import Environment
            login = Environment.get_login()
            my.logged_in = login.get_login()
        my.logged_in_login = my.server.eval("@SOBJECT(sthpw/login['login','%s'])" % my.logged_in)[0]
        my.location = my.logged_in_login.get('location')
        if my.client_email in [None,''] and my.location == 'external':
            my.client_email = my.logged_in_login.get('email')
        my.order_name = my.order.get('name')
        my.start_date = my.order.get('start_date')
        my.due_date = my.order.get('due_date')
        my.po_number = my.order.get('po_number')
        my.scheduler = my.order.get('login')
        my.scheduler_email = my.server.eval("@GET(sthpw/login['login','%s']['location','internal']['license_type','user'].email)" % my.scheduler)
        if my.scheduler_email:
            my.scheduler_email = my.scheduler_email[0]
        else:
            my.scheduler_email = ''
        my.from_name = '%s.%s' % (my.logged_in_login.get('first_name'), my.logged_in_login.get('last_name'))
        my.data = {'order_code': my.order_code, 'po_number': my.po_number, 'client_email': my.client_email,
                   'scheduler_email': my.scheduler_email, 'client_name': my.client_name, 'client_code': my.client_code,
                   'client_login': my.client_login, 'order_name': my.order_name, 'start_date': my.start_date,
                   'due_date': my.due_date, 'from_name': my.from_name, 'location': my.location}
    
    def get_external_data(my):
        send_data = {}
        from_email = ''
        if my.client:
            from_email = my.client.get('scheduling_team_email')
        if from_email in [None,'']:
            from_email = 'Strat2GReply@2gdigital.com'
     
        to_email = ''
        client_login_email = ''
        client_rep_email = ''
        login_email = ''
 
        if my.client_login_obj:
            client_login_email = my.client_login_obj.get('email')
       
        client_rep = my.order.get('client_rep')
        if client_rep not in [None,'']:
            client_person = my.server.eval("@SOBJECT(twog/person['code','%s'])" % client_rep)
            if client_person:
                client_person = client_person[0]
                if client_person.get('email') not in [None,'']:
                    client_rep_email = client_person.get('email')
                else:
                    client_rep_email = my.server.eval("@GET(sthpw/login['login','%s'].email)" % client_person.get('login_name'))
                    if client_rep_email:
                        client_rep_email = client_rep_email[0]
                    else:
                        client_rep_email = ''
    
        if my.logged_in_login.get('location') == 'external':
            if my.client_login_obj:
                if my.logged_in_login != my.client_login_obj.get('login'):
                    login_email = my.logged_in_login.get('email')
     
        ext_list = []
        if client_login_email not in [None,'']:
            to_email = client_login_email
        if client_rep_email not in [None,'']:
            if to_email == '':
                to_email = client_rep_email
            else:
                ext_list.append(client_rep_email)  
        if login_email not in [None,'']:
            if to_email == '':
                to_email = login_email
            else:
                ext_list.append(login_email)  
    
        client_email_list = my.order.get('client_email_list')
        if client_email_list not in [None,'']:
            client_email_arr = client_email_list.split(',')
            for email in client_email_arr:
                if email not in ext_list:
                    ext_list.append(email)
        ext_notification_list = ''
        if my.client_login_obj: 
            ext_notification_list = my.client_login_obj.get('external_notification_list')
            if ext_notification_list not in [None,'']:
                ext_notification_arr = ext_notification_list.split(',')
                for email in ext_notification_arr:
                    if email not in ext_list:
                        ext_list.append(email)    
    
        if my.logged_in_login.get('location') == 'external':
            if my.client_login_obj:
                if my.logged_in_login.get('login') != my.client_login_obj.get('login'):
                    lg_list = my.logged_in_login.get('external_notification_list')
                    if lg_list not in [None,'']:
                        lg_arr = lg_list.split(',')
                        for email in lg_arr:
                            if email not in ext_list:
                                ext_list.append(email)
       
        clean_data = {}
        for key, val in my.data.iteritems():
            if key != 'ext_ccs':
                clean_data[key] = val    
        send_data = clean_data
        send_data['from_email'] = from_email
        send_data['to_email'] = to_email
        final_ext_list = []
        for thing in ext_list:
            if thing not in [None,'',[]]:
                final_ext_list.append(thing)
        cc_list = ';'.join(final_ext_list)
        if cc_list not in [None,'']:
            if cc_list[0] == ';':
                cc_list = cc_list[1:]
        send_data['ext_ccs'] = cc_list
        send_data['ccs'] = send_data.get('ext_ccs')
        if my.client not in [None,'']:
            if my.client.get('name') not in ['Fremantle','GRB Entertainment','The Weinstein Company, LLC','Relativity Media']:
                send_data['from_email'] = login_email
                send_data['to_email'] = login_email
                send_data['ext_ccs'] = cc_list
                send_data['ccs'] = cc_list
        else:
            send_data['from_email'] = login_email
            send_data['to_email'] = login_email
            send_data['ext_ccs'] = ''
            send_data['ccs'] = ''
        #Keep track of the emails send to clients
        os.system('''echo "FROM: %s, TO: %s, CCS: %s, EXT_CCS: %s" >> /var/www/html/source_labels/external_outgoing''' % (send_data['from_email'], send_data['to_email'], send_data['ccs'], send_data['ext_ccs']))
        return send_data
    
    def get_internal_data(my):
        login_email = ''
        sched_team = ''
        int_list = []
        
        # Figure out who the email should say it is from
        from_email = ''
        if my.client:
            sched_team = my.client.get('scheduling_team_email')
            if sched_team:
                from_email = sched_team
        if my.scheduler_email not in [None,''] and from_email == '':
            from_email = my.scheduler_email
        if my.logged_in_login.get('location') == 'internal':
            if my.logged_in_login.get('email') not in [None,'']:
                login_email = my.logged_in_login.get('email')
        if from_email == '':
            if login_email not in [None,'']:
                from_email = login_email
        if from_email == '':
            from_email = 'Strat2GReply@2gdigital.com'
       
        #Figure out who we want to send the email to
        to_email = ''
        if sched_team not in [None,'']:
            to_email = sched_team
        if to_email == '' and my.scheduler_email not in [None,'']:
            to_email = my.scheduler_email
        elif my.scheduler_email not in [None,'']:
            int_list.append(my.scheduler_email)
        if my.logged_in_login.get('location') == 'internal':
            if login_email not in [None,'']:
                if to_email == '':
                    to_email = login_email
                else:
                    if login_email not in int_list:
                        int_list.append(login_email)
        if to_email == '':
            to_email = 'Strat2GReply@2gdigital.com'
        
        #If the client has people that they want alerted all the time for their notifications, get those email addresses too - as long as it's not the client themself that's writing the note (or whatever) 
        internal_email_list1 = my.logged_in_login.get('internal_notification_list')
        internal_email_list2 = ''
        if my.client_login_obj:
            if my.client_login_obj.get('internal_notification_list') not in [None,''] and my.client_login_obj.get('login') != my.logged_in_login.get('login'):
                internal_email_list2 = my.client_login_obj.get('internal_notification_list')
        internal_email_list3 = ''
        if my.client:
            if my.client.get('internal_notification_list'):
                internal_email_list3 = my.client.get('internal_notification_list')
        list1_arr = internal_email_list1.split(',')
        list2_arr = internal_email_list2.split(',')
        list3_arr = internal_email_list3.split(',')
        all_lists = list1_arr + list2_arr + list3_arr
        for email in all_lists:
            if email not in int_list:
                int_list.append(email)

        order_builder_url = ctu.get_order_builder_url(my.order_code, my.server)
        href = '<a href="{0}">{1}</a>'
        order_hyperlink = href.format(order_builder_url, my.order_name)

        client_hyperlink = ctu.get_edit_wdg_hyperlink('twog/client', my.client_code,
                                                      sobject_name=my.client_name, server=my.server)

        clean_data = {}
        for key, val in my.data.iteritems():
            if key != 'ext_ccs':
                clean_data[key] = val    
        send_data = clean_data
        send_data['order_hyperlink'] = order_hyperlink
        send_data['client_hyperlink'] = client_hyperlink
        send_data['from_email'] = from_email
        send_data['to_email'] = to_email
        #print "int list = %s" % int_list
        final_int_list = []
        for thing in int_list:
            if thing not in [None,'',[]]:
                final_int_list.append(thing)
        cc_list = ';'.join(final_int_list)
        if cc_list not in [None,'']:
            if cc_list[0] == ';':
                cc_list = cc_list[1:]
        send_data['int_ccs'] = cc_list
        send_data['ccs'] = send_data.get('int_ccs')
        return send_data 
    

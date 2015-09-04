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
        # CUSTOM_SCRIPT00106
        # Matthew Tyler Misenhimer
        # Sends an email when a New Login is inserted
        import os
        internal_template_file = '/opt/spt/custom/formatted_emailer/internal_new_login_template.html'
        
        sobject = input.get('sobject')
        if sobject.get('location') == 'external':
            #Then we need to send the new login to Gary/IT
            subject = 'A New Client Login Account Has Been Created (%s): %s, %s' % (sobject.get('login'), sobject.get('last_name'), sobject.get('first_name'))
            dude = server.eval("@SOBJECT(twog/person['login_name','%s'])" % sobject.get('login'))
            email = sobject.get('email')
            client_name = ''
            if dude:
                dude = dude[0]
                if dude.get('client_code') not in [None,'']:
                    client = server.eval("@SOBJECT(twog/client['code','%s'])" % dude.get('client_code'))
                    if client:
                        client = client[0]
                        client_name = client.get('name')
                        subject = 'A New Client Login Account Has Been Created for "%s" (%s): %s, %s' % (client_name, sobject.get('login'), sobject.get('last_name'), sobject.get('first_name'))
            passwo = 'Password is available in the client list in Tactic, under "portal_pass"'
            split_login = sobject.get('login').split('.')
            if len(split_login) > 1:
                passwo = '2g%s' % split_login[len(split_login) - 1]
            client_portion = ''
            if client_name not in [None,'']:
                client_portion = "<br/>Client: %s" % client_name
            head_message = "Created a Portal Login<br/>Username: <font color='#71cd4c'>%s</font><br/>Password: <font color='#71cd4d'>%s</font><br/>Email: %s%s<br/><br/><a href='http://tactic.2gdigital.com/tactic/twog/client_view' target='_blank'>Link to 2G's Client Portal</a>" % (sobject.get('login'), passwo, email, client_portion)
            head_message = '<table style="font-size: 14px; color: #440000;"><tr><td><b>%s</b></td></tr></table>' % head_message
            
            int_template = open(internal_template_file, 'r')
            filled = ''
            for line in int_template:
                line = line.replace('[MESSAGE]', head_message)
                filled = '%s%s' % (filled, line)
            int_template.close()
            filled_in_email = '/var/www/html/formatted_emails/int_login_inserted_%s.html' % split_login[0]
            filler = open(filled_in_email, 'w')
            filler.write(filled)
            filler.close()
            from_email = 'tacticit@2gdigital.com'
            to_email =  'tacticit@2gdigital.com'
            int_ccs =  'tacticit@2gdigital.com'
            subject = subject.replace(' ','..')
            the_command = "php /opt/spt/custom/formatted_emailer/trusty_emailer.php '''%s''' '''%s''' '''%s''' '''%s''' '''%s''' '''%s'''" % (filled_in_email, to_email, from_email, 'Tactic New Accounts', subject, int_ccs.replace(';','#Xs*'))
            os.system(the_command)
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

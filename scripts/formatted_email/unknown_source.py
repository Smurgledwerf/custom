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
        # CUSTOM_SCRIPT00092
        #Matthew Tyler Misenhimer
        #This sends out an email when a source is scanned, but is found to not be in our system
        
        from pyasm.common import Environment
        delim = '#Xs*'
        login = Environment.get_login()
        user_name = login.get_login()
        sobject = input.get('sobject')
        source_name = sobject.get('source_name')
        #The name "UNKNOWN SOURCE" is set by the location tracker
        if source_name == 'UNKNOWN SOURCE':
            #Recipients 
            all_ccs = '2GArrivals@2gdigital.com'
            email_expr = "@GET(sthpw/login['login','%s']['location','internal']['license_type','user'].email)" % user_name
            email_address = server.eval(email_expr)
            if email_address:
                email_address = email_address[0]
            else:
                email_address = "tacticIT@2gdigital.com"
            barcode = sobject.get('source_barcode')
            location = sobject.get('location_name')
            
            template_path = '/opt/spt/custom/formatted_emailer/unknown_source_msg.html'
            filled_in_path = '/var/www/html/formatted_emails/unknown_source_%s.html' % sobject.get('code')
            #Fill in the template and send it as an email
            template = open(template_path, 'r')
            filled = ''
            for line in template:
                line = line.replace('[LOCATION_NAME]', location)
                line = line.replace('[SOURCE_BARCODE]', barcode)
                filled = '%s%s' % (filled, line)
            
            template.close()
            filler = open(filled_in_path, 'w')
            filler.write(filled)
            filler.close()
            #Create bundled message to send as an email
            server.insert('twog/bundled_message', {'filled_in_path': filled_in_path, 'message': 'AN UNKNOWN SOURCE WAS SCANNED. THIS ELEMENT NEEDS TO BE ENTERED INTO TACTIC AND ITS LOCATION RECORDED AGAIN.', 'from_email': 'TechAlert@2gdigital.com', 'to_email': email_address, 'from_name': '%s SCANNED AN UNKNOWN SOURCE' % user_name, 'subject': 'UNKNOWN SOURCE SCANNED BY %s' % user_name, 'all_ccs': all_ccs, 'object_code': sobject.get('code')})
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

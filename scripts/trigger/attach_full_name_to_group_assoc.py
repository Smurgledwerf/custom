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
        # CUSTOM_SCRIPT00104
        #print "IN ATTACH FULL NAME TO GROUP ASSOC"
        sob = input.get('sobject')
        login = server.eval("@SOBJECT(sthpw/login['login','%s'])" % sob.get('login'))[0]
        
        login_full_name_s = login.get('login').split('.') 
        
        try_fn = login_full_name_s[0] 
        try_fn = '%s%s' % (try_fn[0].upper(), try_fn[1:]) 
        try_ln = '' 
        if len(login_full_name_s) > 1: 
            try_ln = login_full_name_s[1] 
            try_ln = '%s%s' % (try_ln[0].upper(), try_ln[1:]) 
        login_full_name = '%s %s' %  (try_fn, try_ln) 
        
        first_name = login.get('first_name') 
        last_name = login.get('last_name') 
        if first_name not in [None,''] and last_name not in [None,'']: 
            login_full_name = '%s %s' % (first_name, last_name) 
        
        server.update(sob.get('__search_key__'), {'login_full_name': login_full_name}, triggers=False)
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

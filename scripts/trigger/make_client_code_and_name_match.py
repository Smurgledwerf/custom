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
        # CUSTOM_SCRIPT00056
        #print "IN MAKE CC AND NAME MATCH"
        if 'update_data' in input.keys():
            update_data = input.get('update_data') 
            ukeys = update_data.keys()
            sobject = input.get('sobject')
            sob_client_name = sobject.get('client_name')
            sob_client_code = sobject.get('client_code')
            if 'client_name' in ukeys:
                new_name = update_data.get('client_name')
                client_code = server.eval("@GET(twog/client['name','%s'].code)" % new_name)
                if client_code:
                    client_code = client_code[0]
                    if client_code != sob_client_code: 
                        server.update(input.get('search_key'), {'client_code': client_code})
            if 'client_code' in ukeys:
                new_code = update_data.get('client_code')
                client_name = server.eval("@GET(twog/client['code','%s'].name)" % new_code)
                if client_name:
                    client_name = client_name[0]
                    if client_name != sob_client_name:
                        server.update(input.get('search_key'), {'client_name': client_name})
        #print "LEAVING MAKE CC AND NAME MATCH"
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

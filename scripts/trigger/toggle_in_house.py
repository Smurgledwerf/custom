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
        # CUSTOM_SCRIPT00025
        #print "IN TOGGLE IN HOUSE"
        #print "INPUT = %s" % input
        data = input.get('data')
        source_code = data.get('source_code')
        source = server.eval("@SOBJECT(twog/source['code','%s'])" % source_code)
        #print "SOURCE = %s" % source
        if len(source) > 0:
            source = source[0]
            in_house = source.get('in_house')
            #print "IN HOUSE = %s" % in_house
            new_in_house = False
            if in_house in [False,'',None]:
                new_in_house = True
            #print "UPDATIN IN HOUSE TO %s" % new_in_house
            server.update(server.build_search_key('twog/source', source_code), {'in_house': new_in_house})
        #print "LEAVING TOGGLE IN HOUSE"
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

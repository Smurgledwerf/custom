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
        # CUSTOM_SCRIPT00026
        #print "IN UPDATE IN HOUSE"
        sobj = input.get('sobject')
        movement_code = sobj.get('movement_code')
        source_code = sobj.get('source_code')
        
        if movement_code not in [None,''] and source_code not in [None,'']:
            movement = server.eval("@SOBJECT(twog/movement['code','%s'])" % movement_code)[0]
            from_code = movement.get('sending_company_code')
            to_code = movement.get('receiving_company_code')
            if from_code not in [None,''] and to_code not in [None,'']:
                from_comp = server.eval("@SOBJECT(twog/company['code','%s'])" % from_code)[0]
                to_comp = server.eval("@SOBJECT(twog/company['code','%s'])" % to_code)[0]
                in_house = False
                if "2G DIGITAL" in from_comp.get('name').upper():
                    in_house = False
                if "2G DIGITAL" in to_comp.get('name').upper():
                    in_house = True
                server.update(server.build_search_key('twog/source', source_code), {'in_house': in_house})
        if source_code not in [None,'']:
            source = server.eval("@SOBJECT(twog/source['code','%s'])" % source_code)[0]
            server.update(sobj.get('__search_key__'), {'barcode': source.get('barcode')})
        #print "LEAVING UPDATE IN HOUSE"
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

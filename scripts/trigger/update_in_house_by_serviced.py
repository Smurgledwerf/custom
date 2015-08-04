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
        # CUSTOM_SCRIPT00096
        from pyasm.common import TacticException
        #print "IN UPDATE IN HOUSE BY SERVICED"
        movement = input.get('sobject')
        if movement.get('serviced') in [True,'true','t','T',1,'1']:
            movement_code = movement.get('code')
            from_code = movement.get('sending_company_code')
            to_code = movement.get('receiving_company_code')
            in_house = False
            if from_code in [None,''] or to_code in [None,'']:
                raise TacticException('To mark this as serviced, you must select both the Sending and Receiving Companies.')
            else:
                from_comp = server.eval("@SOBJECT(twog/company['code','%s'])" % from_code)[0]
                if "2G DIGITAL" in from_comp.get('name').upper():
                    in_house = False
                to_comp = server.eval("@SOBJECT(twog/company['code','%s'])" % to_code)[0]
                if "2G DIGITAL" in to_comp.get('name').upper():
                    in_house = True
            
            sources = server.eval("@SOBJECT(twog/asset_to_movement['movement_code','%s'])" % movement_code)
            
            for source in sources:
                source_code = source.get('source_code')
                if source_code not in [None,'']:
                    server.update(server.build_search_key('twog/source', source_code), {'in_house': in_house})
        
        #print "LEAVING UPDATE IN HOUSE BY SERVICED"
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

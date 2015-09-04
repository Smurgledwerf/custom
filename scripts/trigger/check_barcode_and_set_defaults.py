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
        # CUSTOM_SCRIPT00043
        #print "IN CHECK BARCODE and set defaults"
        from pyasm.common import TacticException
        sobj = input.get('sobject')
        sk = server.build_search_key('twog/source', sobj.get('code'))
        barcode = sobj.get('barcode')
        #print "BARCODE = %s" % barcode
        if barcode not in [None,'','XXXXXXXXX']:
            others_expr = "@SOBJECT(twog/source['barcode','%s'])" % barcode
            #print "OTHERS_EXPR =%s" % others_expr
            others = server.eval(others_expr)
            if len(others) > 1:
                #print "BARCODE BAD"
                server.update(sk, {'barcode': 'XXXXXXXXX'})
                raise TacticException('This entry cannot have %s as a barcode, as another element is already using it. Please enter a different barcode and make sure to hit "save"!' % barcode);
        next_data = {}
        if sobj.get('in_house') in ['False',False,'false','f','',None]:
            next_data['in_house'] = True
        if sobj.get('strat2g_id') in [None,'']:
            next_data['strat2g_id'] = sobj.get('code')
        if next_data != {}:
            server.update(sk, next_data)
        #print "LEAVING CHECK BARCODE and set defaults"
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

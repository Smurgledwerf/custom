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
        # CUSTOM_SCRIPT00016
        #print "IN SET PROJ TEMPL"
        update_data = input.get('update_data')
        sobb = input.get('sobject')
        sob_code = sobb.get('code')
        sk = sobb.get('__search_key__')
        me = sobb
        if me.get('templ_me') in ['true','True','t',True,1]:
            flat_pricing = me.get('flat_pricing')
            is_billable = me.get('is_billable')
            keywords = me.get('keywords')
            pipeline_code = me.get('pipeline_code')
            projected_markup_pct = me.get('projected_markup_pct')
            projected_overhead_pct = me.get('projected_overhead_pct')
            rate_card_price = me.get('rate_card_price')
            parent_pipe = me.get('parent_pipe')
            specs = me.get('specs')
            templ_obj = server.eval("@SOBJECT(twog/proj_templ['code','%s'])" % me.get('proj_templ_code'))
            if templ_obj:
                server.update(templ_obj[0].get('__search_key__'), {'parent_pipe': parent_pipe, 'flat_pricing': flat_pricing, 'is_billable': is_billable, 'keywords': keywords, 'pipeline_code': pipeline_code, 'projected_markup_pct': projected_markup_pct, 'projected_overhead_pct': projected_overhead_pct, 'rate_card_price': rate_card_price, 'specs': specs}, triggers=False) 
            else:
                new_templ = server.insert('twog/proj_templ', {'parent_pipe': parent_pipe, 'flat_pricing': flat_pricing, 'is_billable': is_billable, 'keywords': keywords, 'pipeline_code': pipeline_code, 'projected_markup_pct': projected_markup_pct, 'projected_overhead_pct': projected_overhead_pct, 'rate_card_price': rate_card_price, 'specs': specs}, triggers=False) 
                server.update(sk, {'proj_templ_code': new_templ.get('code')}, triggers=False)
        #print "LEAVING SET PROJ TEMPL"
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

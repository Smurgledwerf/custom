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
        # CUSTOM_SCRIPT00017
        update_data = input.get('update_data')
        sobb = input.get('sobject')
        sob_code = sobb.get('code')
        me = sobb
        sk = me.get('__search_key__')
        if me.get('templ_me') in ['true','True','t',True,1]:
            go_ahead = False
            fields = ['instructions', 'work_group', 'estimated_work_hours', 'keywords', 'parent_pipe']
            keys = me.keys()
            for field in fields:
                if field in keys:
                    go_ahead = True
            if go_ahead:
                instructions = me.get('instructions')
                keywords = me.get('keywords')
                work_group = me.get('work_group')
                parent_pipe = me.get('parent_pipe')
                estimated_work_hours = me.get('estimated_work_hours')
                templ_expr = "@SOBJECT(twog/work_order_templ['code','%s'])" % me.get('work_order_templ_code')
                templ_obj = server.eval(templ_expr)
                if templ_obj:
                    server.update(templ_obj[0].get('__search_key__'), {'instructions': instructions, 'work_group': work_group, 'estimated_work_hours': estimated_work_hours,'keywords': keywords, 'parent_pipe': parent_pipe}, triggers=False) 
                else:
                    new_templ = server.insert('twog/work_order_templ', {'instructions': instructions, 'work_group': work_group, 'estimated_work_hours': estimated_work_hours,'keywords': keywords, 'parent_pipe': parent_pipe}, triggers=False)
                    server.update(sk, {'work_order_templ_code': new_templ.get('code')}, triggers=False)
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

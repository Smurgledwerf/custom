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
        # CUSTOM_SCRIPT00067
        #print "IN INSERT NOTE"
        sob = input.get('sobject')
        note_sk = input.get('search_key')
        search_type = sob.get('search_type').split('?')[0]
        search_id = sob.get('search_id')
        expr = "@SOBJECT(%s['id','%s'])" % (search_type, search_id)
        parent = server.eval(expr)
        if parent:
            parent = parent[0]
            parent_code = parent.get('code')
            work_order_code = ''
            proj_code = ''
            title_code = ''
            title_name = ''
            title_episode = ''
            title_indicator = ''
            order_code = ''
            post_note = sob.get('note')
            title = None
            if 'WORK_ORDER' in parent_code:
                work_order_code = parent_code
                proj_code = parent.get('proj_code')
                title = server.eval("@SOBJECT(twog/proj['code','%s'].twog/title)" % proj_code)
                if title:
                    title = title[0]
                    title_code = title.get('code')
                    order_code = title.get('order_code')
            elif 'PROJ' in parent_code:
                proj_code = parent_code
                title_code = parent.get('title_code')
                the_order = server.eval("@SOBJECT(twog/title['code','%s'].twog/order)" % title_code)
                if the_order:
                    the_order = the_order[0]
                    order_code = the_order.get('code')
            elif 'TITLE' in parent_code:
                title_code = parent_code
                order_code = parent.get('order_code')
                if sob.get('process') in ['QC Rejected','Failed QC','Rejected']:
                    last_error = server.eval("@SOBJECT(twog/production_error['title_code','%s']['@ORDER_BY','timestamp desc'])" % title_code)
                    if last_error:
                        last_error = last_error[0]
                        prenote = sob.get('note')
                        op_desc = last_error.get('operator_description')
                        post_note = '%s\n%s\n(%s)' % (prenote, op_desc, last_error.get('code'))
                        server.update(note_sk, {'note': post_note})
            elif 'ORDER' in parent_code:
                order_code = parent_code
            upd_data = {'work_order_code': work_order_code, 'proj_code': proj_code, 'title_code': title_code, 'order_code': order_code}
            if title_code not in [None,'']:
                title = server.eval("@SOBJECT(twog/title['code','%s'])" % title_code)[0]
                title_indicator = '(%s) %s' % (title_code, title.get('title'))
                if title.get('episode') not in [None,'']:
                    title_indicator = '%s: %s' % (title_indicator, title.get('episode'))
            if work_order_code not in [None,''] and '(WORK_ORDER' not in post_note:
                post_note = '%s)\n%s' % (work_order_code, post_note)
                if title_code not in [None,'']:
                    post_note = '(%s:%s' % (title_indicator, post_note)
                upd_data['note'] = post_note
            elif title_code not in [None,'']:
                post_note = '(%s)\n%s' % (title_indicator, post_note)
                upd_data['note'] = post_note
            server.update(note_sk, upd_data)
        
        
        #print "LEAVING INSERT NOTE"
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

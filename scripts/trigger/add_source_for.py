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
        # CUSTOM_SCRIPT00031
        # Matthew Tyler Misenhimer
        # This will record on the source the object it is a source for
        # input is a work_order_sources entry
        
        sobj = input.get('sobject')
        sk = input.get('search_key')
        source_code = sobj.get('source_code')
        work_order_code = sobj.get('work_order_code')
        work_order = server.eval("@SOBJECT(twog/work_order['code','%s'])" % work_order_code)[0]
        proj = server.eval("@SOBJECT(twog/proj['code','%s'])" % work_order.get('proj_code'))[0]
        title = server.eval("@SOBJECT(twog/title['code','%s'])" % proj.get('title_code'))[0]
        title_code = title.get('code')
        order_code = title.get('order_code')
        source = server.eval("@SOBJECT(twog/source['code','%s'])" % source_code)[0]
        source_for = source.get('source_for')
        new_str = source_for
        if source_for.find(work_order_code) == -1:
            new_str = '%s,%s' % (new_str, work_order_code)
        if source_for.find(title_code) == -1:
            new_str = '%s,%s' % (new_str, title_code)
        if source_for.find(order_code) == -1:
            new_str = '%s,%s' % (new_str, order_code)
        if new_str[0] == ',':
            new_str = new_str[1:]
        server.update(source.get('__search_key__'), {'source_for': new_str})
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

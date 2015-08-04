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
        # CUSTOM_SCRIPT00101
        def make_timestamp():
            from pyasm.common import SPTDate
            #Makes a Timestamp for postgres
            import datetime
            now = SPTDate.convert_to_local(datetime.datetime.now())
            return now
        
        sobject = input.get('sobject')
        update_data = input.get('update_data')
        sk = sobject.get('__search_key__')
        if 'is_external_rejection' in update_data.keys():
            from pyasm.biz import Note
            from pyasm.search import Search
            title_name = sobject.get('title')
            if sobject.get('episode') not in [None,'']:
                title_name = '%s: %s' % (title_name, sobject.get('episode'))
            title_obj = Search.get_by_search_key(sk) #Need this kind of object to make the note we'll be sending
            is_external_rejection = update_data.get('is_external_rejection')
            if is_external_rejection == 'true':
                non_rejected_titles = server.eval("@SOBJECT(twog/title['bigboard','True']['is_external_rejection','false']['status','!=','Completed']['@ORDER_BY','priority asc'])")
                smaller = .05
                if len(non_rejected_titles) > 0:
                    smallest_prio = non_rejected_titles[0].get('priority')
                    smaller = float(float(smallest_prio)/2) 
                el_timeo = make_timestamp()
                #Set priority to something smaller than all non-externally-rejected titles on the bigboard
                #Set due date and deliver by date to today's date
                #Set bigboard to true and put all WOs on bigboard
                server.update(sk, {'priority': smaller, 'bigboard': True, 'due_date': el_timeo, 'expected_delivery_date': el_timeo})
                all_tasks = server.eval("@SOBJECT(sthpw/task['title_code','%s'])" % sobject.get('code'))
                for task in all_tasks:
                    server.update(task.get('__search_key__'), {'bigboard': True}, triggers=False)
                #Now make the note
                note = "%s (%s) was rejected externally.\nThis title has been put on the bigboard and it's due & expected delivery dates have been set to today.\nPlease do all you can to get this title back out to the client by the end of the day.\n\nReason provided for External Rejection: %s\n\nOrder Code = %s\nTitle Code = %s" % (title_name, sobject.get('code'), sobject.get('external_rejection_reason'), sobject.get('order_code'), sobject.get('code')) 
                note2 = Note.create(title_obj, note, context='Received External Rejection', process='Received External Rejection')
                sources_str = ''
                source_links = server.eval("@SOBJECT(twog/title_origin['title_code','%s'])" % title_obj.get_code())
                for s in source_links:
                    source = server.eval("@SOBJECT(twog/source['code','%s'])" % s.get('source_code'))
                    if source:
                        source = source[0]
                        source_fn = source.get('title')
                        if source.get('episode') not in [None,'']:
                            source_fn = '%s: %s' % (source_fn, source.get('episode'))
                        if sources_str == '':
                            sources_str = '%s (%s) Barcode: %s' % (source.get('code'), source_fn, source.get('barcode'))
                        else:
                            sources_str = '%s\n%s (%s) Barcode: %s' % (sources_str, source.get('code'), source_fn, source.get('barcode'))
                server.insert('twog/external_rejection', {'order_code': title_obj.get_value('order_code'), 'order_name': title_obj.get_value('order_name'), 'status': 'Open', 'reported_issue': sobject.get('external_rejection_reason'), 'title_code': title_obj.get_code(), 'scheduler_reason': sobject.get('external_rejection_reason'), 'title': title_obj.get_value('title'), 'episode': title_obj.get_value('episode'), 'po_number': title_obj.get('po_number'), 'email_list': '', 'sources': sources_str})
            else:
                #DO THE OPPOSITE AS ABOVE
                saved_priority = sobject.get('saved_priority')
                server.update(sk, {'bigboard': False, 'priority': saved_priority})
                note = "%s (%s) had been marked as rejected externally, but this may have been in error. It is no longer marked as rejected externally.\nThis title has been removed from the bigboard, but it's due & expected delivery dates may still be set to today's date (might need to be addressed).\nOrder Code = %s\nTitle Code = %s" % (title_name, sobject.get('code'), sobject.get('order_code'), sobject.get('code')) 
                note2 = Note.create(title_obj, note, context='External Rejection Mark Removed', process='External Rejection Mark Removed')
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

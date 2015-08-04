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
        # CUSTOM_SCRIPT00102
        sobject = input.get('sobject')
        print "SOBJECT = %s" % sobject 
        update_data = input.get('update_data')
        if 'file_path' in update_data.keys():
            file_path = update_data.get('file_path')
            if file_path not in [None,'']:
                fp_s = file_path.split('/')
                if len(fp_s) > 1:
                    file_name = fp_s[len(fp_s) - 1]
                    print "File Name = %s" % file_name
                    server.update(sobject.get('__search_key__'), {'file_name': file_name}, triggers=False)
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

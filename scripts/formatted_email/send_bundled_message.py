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
        # CUSTOM_SCRIPT00062
        #Matthew Tyler Misenhimer
        #This sends emails that are placed in the db as a 'bundled_message' sobject
        
        def fix_note_chars(note):
            if isinstance(note, bool):
                note2 = 'False'
                if note:
                    note2 = 'True'
                note = note2
            else:
                import sys
                from json import dumps as jsondumps
                if note not in [None,'']:
                    if sys.stdout.encoding:
                        note = note.decode(sys.stdout.encoding)
                note = jsondumps(note)
                note = note.replace('||t','&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                note = note.replace('\\\\t','&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                note = note.replace('\\\t','&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                note = note.replace('\\t','&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                note = note.replace('\t','&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                note = note.replace('\\"','"')
                note = note.replace('\"','"')
                note = note.replace('||n','<br/>')
                note = note.replace('\\\\n','<br/>')
                note = note.replace('\\\n','<br/>')
                note = note.replace('\\n','<br/>')
                note = note.replace('\n','<br/>')
            return note
        
        import os
        from pyasm.common import Environment
        bundle = input.get('sobject')
        filled_in_path = bundle.get('filled_in_path')
        message = bundle.get('message')
        #message = fix_note_chars(message)
        from_email = bundle.get('from_email')
        to_email = bundle.get('to_email')
        from_name = bundle.get('from_name')
        subject = bundle.get('subject')
        all_ccs = bundle.get('all_ccs')
        object_code = bundle.get('object_code')
        #Send it to the php mailer
        os.system("php /opt/spt/custom/formatted_emailer/inserted_order_email.php '''%s''' '''%s''' '''%s''' '''%s''' '''%s''' '''%s'''" % (filled_in_path, to_email, from_email, from_name, subject, all_ccs))
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

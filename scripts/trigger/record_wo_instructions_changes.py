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
        # CUSTOM_SCRIPT00084
        #Record the changes to work order instructions
        
        def make_timestamp():
            from pyasm.common import SPTDate
            #Makes a Timestamp for postgres
            import datetime
            #now = SPTDate.convert_to_local(datetime.datetime.now())
            now = datetime.datetime.now()
            return now
        
        def get_regex_info(str_in):
            import re
            good_bad_bool = True
            error_text = ''
            found = re.findall(r'<.*>', str_in)
            for f in found:
                good_bad_bool = False
                if error_text == '':
                    error_text = 'The following tags in your instructions are not allowed: "%s"' % f
                else:
                    error_text = '%s, "%s"' % (error_text, f)
            #found = re.findall(r'<', str_in)
            #if len(found) > 0:
            #    if error_text == '':
            #        error_text = 'The following character in your instructions is not allowed: "<"'
            #    else:
            #        error_text = '%s\nAlso, the following character in your instructions is not allowed: "<"' % error_text
            #Want Regex to return all characters that do not fit in pattern, but dont know what characters are ok and which aren't. Turning off for now 
            #found = re.findall(r'[^A-Za-z0-9 -\/\\.\"?,:;}{\]\[\n\t_+\)\(\&\*\^\$\#\@\!\~\`]', str_in)
            #print "FOUND = %s" % found
            error_text = error_text.replace('<','&lt;').replace('>','&gt;') 
            return [good_bad_bool, error_text]
        
        print "IN RECORD WO INSTRUCTIONS CHANGES"
        if 'update_data' in input.keys():
            from pyasm.common import Environment
            from pyasm.common import TacticException
            login = Environment.get_login()
            user_name = login.get_login()
            update_data = input.get('update_data') 
            prev_data = input.get('prev_data')
            old_instructions = prev_data.get('instructions')
            if old_instructions in [None,'']:
                old_instructions = ''
            new_instructions = update_data.get('instructions')
            regex_info = get_regex_info(new_instructions)
            finish_it = regex_info[0]
            error_text = regex_info[1]
            if finish_it:
                sobject = input.get('sobject')
                server.insert('twog/wo_instruction_changes', {'login': user_name, 'work_order_code': sobject.get('code'), 'title_code': sobject.get('title_code'), 'order_code': sobject.get('order_code'), 'old_instructions': old_instructions, 'new_instructions': new_instructions, 'process': sobject.get('process')})
                sobject = input.get('sobject')
                task_code = sobject.get('task_code')
                order_code = sobject.get('order_code')
                if task_code not in [None,''] and order_code not in [None,'']:
                    task = server.eval("@SOBJECT(sthpw/task['code','%s'])" % task_code)
                    if task:
                        task = task[0]
                        if task.get('flag_future_changes') in [True,'true','True',1,'1']:
                            instruction_update_times = task.get('instruction_update_times')
                            new_times = ''
                            if instruction_update_times == '':
                                new_times = '%s#USER=%s' % (make_timestamp(), user_name)
                            else: 
                                new_times = '%s,%s#USER=%s' % (instruction_update_times, make_timestamp(), user_name)
                            server.update(task.get('__search_key__'), {'instruction_update_times': new_times}, triggers=False) 
            else:
                raise TacticException(error_text)
                
         
        #print "LEAVING RECORD WO INSTRUCTIONS CHANGES"
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

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
        # CUSTOM_SCRIPT00002
        # Matthew Tyler Misenhimer
        # Inserts template sobjects after a pipeline is saved
        # THIS IS ADD_WO_OR_PROJ_TEMPL
        # input and server are assumed
        # sobj is config/process
        from pyasm.common import TacticException
        sobj = input.get('sobject')
        mode = input.get('mode')
        if mode == 'delete':
            sobj = input.get('data')
            
        pipeline_code = sobj.get('pipeline_code')
        pipeline_sk = server.build_search_key('sthpw/pipeline', pipeline_code)
        pipeline = server.get_by_search_key(pipeline_sk)
        
        
        if 'twog/proj' in  pipeline.get('search_type'):
            # Then it is a pipeline of work orders
            desc = sobj.get('description')
            if desc == None or desc == 'NULL' or desc == 'undefined':
                desc = ''
            filters=[('process',sobj.get('process')),('description', desc),('parent_pipe',pipeline_code)]
            # query if it exists
            if mode=='delete':
                filters.append(('process_code',sobj.get('code')))
                
            work_order_templ  = server.query('twog/work_order_templ', filters=filters, single=True )
           
            if not work_order_templ:
                instructions = ''
                server.insert('twog/work_order_templ',{
                    'process': sobj.get('process'), 
                    'process_code': sobj.get('code'), 
                    'description': desc,
                    'parent_pipe': pipeline_code,
                    'instructions': instructions
                    })
            
        
        if 'twog/title' in  pipeline.get('search_type'):
            #Then it is a pipeline of projs
            desc = sobj.get('description')
            if desc == None or desc == 'NULL' or desc == 'undefined':
                desc = ''
            filters=[('process',sobj.get('process')),('description', desc),('parent_pipe',pipeline_code)]
            # query if it exists
            if mode=='delete':
                filters.append(('process_code',sobj.get('code')))
                
            proj_templ  = server.query('twog/proj_templ', filters=filters, single=True )
           
            if not proj_templ:
                server.insert('twog/proj_templ',{
                    'process': sobj.get('process'), 
                    'process_code': sobj.get('code'), 
                    'parent_pipe': pipeline_code,
                    'description': desc
                    })
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

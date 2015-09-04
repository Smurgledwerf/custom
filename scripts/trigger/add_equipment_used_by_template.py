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
        # CUSTOM_SCRIPT00010
        # Matthew Tyler Misenhimer
        # If the work order has a template connected to equipment used templates, add them as equipment_used's to the work order
        sobj = input.get('sobject')
        code = sobj.get('code')
        wot_code = sobj.get('work_order_templ_code')
        wot_eus_expr = "@SOBJECT(twog/equipment_used_templ['work_order_templ_code','%s'])" % wot_code
        wot_eus = server.eval(wot_eus_expr)
        for eu in wot_eus:
            name = eu.get('name')
            equipment_code = eu.get('equipment_code')
            description = eu.get('description')
            expected_cost = eu.get('expected_cost')
            expected_duration = eu.get('expected_duration')
            expected_quantity = eu.get('expected_quantity')
            eq_templ_code = eu.get('equipment_used_templ_code')
            units = eu.get('units')
            server.insert('twog/equipment_used', {'name': name, 'work_order_code': code, 'equipment_code': equipment_code, 'equipment_used_templ_code': eq_templ_code,'description': description, 'expected_cost': expected_cost, 'expected_duration': expected_duration, 'expected_quantity': expected_quantity, 'units': units})
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

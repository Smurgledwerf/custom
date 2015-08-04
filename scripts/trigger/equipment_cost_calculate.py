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
        # CUSTOM_SCRIPT00050
        update_data = input.get('update_data')
        sobject = input.get('sobject')
        eq_code = sobject.get('equipment_code')
        eq_expr = "@SOBJECT(twog/equipment['code','%s'])" % eq_code
        #print "EQ EXPR = %s" % eq_expr
        eq = server.eval(eq_expr)
        #print "EQ = %s" % eq
        #print "IN EQ COST CALC"
        throwin_data = {}
        if eq:
            eq = eq[0]
            lengths = eq.get('lengths')
            if lengths not in [None,'']:
                if sobject.get('length') not in [None,'']:
                    sob_len = sobject.get('length')
                    eq_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['length','%s'])" % (eq_code, sob_len)
                    #print "EQ COST EXPR = %s" % eq_cost_expr
                    eq_cost = server.eval(eq_cost_expr)
                    #print "EQ COST = %s" % eq_cost
                    if eq_cost:
                        eq_cost = eq_cost[0]
                        cost = eq_cost.get('cost')
                        if cost in [None,'']:
                            cost = 0
                        cost = float(cost)
                        quant = sobject.get('expected_quantity')
                        if quant in [None,'',0,'0']:
                            throwin_data['expected_quantity'] = 1
                            quant = 1
                        quant = float(quant)
                        set_cost = float(cost * quant)
                        if set_cost > 0:
                            throwin_data['expected_cost'] = set_cost
                            throwin_data['actual_cost'] = set_cost
            else:
                # Calculate the cost normally here, update
                units = sobject.get('units')
                divisor = 1
                if units in [None,'','items']:
                    units = 'hr'
                    throwin_data['units'] = 'hr'
                if units == 'mb':
                    units == 'gb'
                    divisor = .01
                if ('E_DELIVERY' in sobject.get('name') or 'STORAGE' in sobject.get('name')) and units in ['hr','items']:
                    units = 'gb'
                    sk = server.build_search_key('twog/equipment_used', sobject.get('code'))
                    server.update(sk, {'units': 'gb'})
                actual_quant = expected_quant = sobject.get('expected_quantity')
                expected_dur = sobject.get('expected_duration')
                if expected_dur in [None,'',0,'0']:
                    expected_dur = 1
                    throwin_data['expected_duration'] = 1
                actual_dur = sobject.get('actual_duration')
                if actual_dur in [None,'',0,'0']:
                    actual_dur = 0
                expected_dur = float(expected_dur)
                actual_dur = float(actual_dur)
                if expected_quant in [None,'','0',0]:
                    actual_quant = expected_quant = 1
                    throwin_data['actual_quantity'] = 1
                    throwin_data['expected_quantity'] = 1
                actual_quant = expected_quant = float(expected_quant)
                eq_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['unit','%s'])" % (eq_code, units)
                #print "EQ COST EXPR = %s" % eq_cost_expr
                eq_cost = server.eval(eq_cost_expr)
                #print "EQ COST = %s" % eq_cost
                if eq_cost:
                    eq_cost = eq_cost[0]
                    cost = eq_cost.get('cost')
                    if cost in [None,'']:
                        cost = 0
                    cost = float(cost)
                    actual_cost = 0
                    expected_cost = 0
                    if units in ['hr','items']:
                        expected_cost = float(expected_dur * expected_quant * cost)
                        actual_cost = float(actual_dur * actual_quant * cost)
                    else:
                        expected_cost = float(expected_quant * expected_dur * divisor * cost)
                        actual_cost = expected_cost
                    throwin_data['expected_cost'] = expected_cost
                    throwin_data['actual_cost'] = actual_cost
        if throwin_data != {}:
            server.update(input.get('search_key'), throwin_data, triggers=False)
            #print "LEAVING EQ COST CALC"
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

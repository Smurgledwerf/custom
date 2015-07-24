import os, sys, math, getopt, random
opts, spins = getopt.getopt(sys.argv[1], '-m')
spins = int(spins)
print "SPINS = %s" % spins
opts, min_bet = getopt.getopt(sys.argv[2], '-m')
min_bet = int(min_bet)
print "MIN BET = %s" % min_bet
opts, max_bet = getopt.getopt(sys.argv[3], '-m')
max_bet = int(max_bet)
print "MAX BET = %s" % max_bet
opts, player_count = getopt.getopt(sys.argv[4], '-m')
player_count = int(player_count)
print "PLAYER_COUT = %s" % player_count
opts, player_cash = getopt.getopt(sys.argv[5], '-m')
player_cash = int(player_cash)
print "PLAYER_CASH = %s" % player_cash
opts, zero_threshold = getopt.getopt(sys.argv[6], '-m')
zero_threshold = int(zero_threshold)
print "ZERO THRESHOLD = %s" % zero_threshold
opts, zero_pct = getopt.getopt(sys.argv[7], '-m')
zero_pct = int(zero_pct)
print "ZERO PCT = %s" % zero_pct
players = {}
fibs = [1,1,2,3,5,8,13,21,34,55,89,144,233,377]
zero_pct = float(float(zero_pct)/float(100))
taken_thirds = []
thirds = [0,range(1,13), range(13,25), range(25,37)]
print thirds
numbers_hit = {}
for i in range(1,player_count+1):
    players[i] = {'bank': player_cash, 'current_range': thirds[i], 'range_num': i, 'cash_on_bet': 0, 'cash_on_zero': 0, 'current_fib': -1, 'last_was_win': False, 'wins': 0, 'losses': 0, 'zwins': 0, 'zlosses': 0, 'smallest_bank': 10000000000, 'biggest_bank': 0, 'history': ''}  
    print "PLAYERS[%s] = %s" % (i,players[i])
    taken_thirds.append(i)
for i in range(0,spins):
    all_on_table = 0
    for k in players.keys():
        #Choose a new Third
        players[k]['cash_on_bet'] = 0
        players[k]['cash_on_zero'] = 0
        if players[k]['bank'] >= min_bet:
            if players[k]['last_was_win']:
                players[k]['current_fib'] = 0
                #my_third = 0
                #while my_third == 0:
                #    for x in range(1,4):
                #        randy = x
                #        if randy not in taken_thirds or randy == players[k]['range_num']:
                #            my_third = randy 
                #if my_third != players[k]['range_num']:
                #    taken_thirds.append(my_third)
                #for f in range(0,len(taken_thirds) - 1):
                #    if taken_thirds[f] == players[k]['range_num']:
                #        taken_thirds.pop(f)
                #players[k]['current_range'] = thirds[my_third]
                #players[k]['range_num'] = my_third
            else:
                players[k]['current_fib'] = players[k]['current_fib'] + 1
            players[k]['last_was_win'] = False
           
            if players[k]['current_fib'] >= len(fibs):
                players[k]['current_fib'] = players[k]['current_fib'] - 1
            planned_bet = fibs[players[k]['current_fib']] * min_bet
            if planned_bet > max_bet:
                planned_bet = max_bet
            if players[k]['bank'] > planned_bet:
                players[k]['cash_on_bet'] = planned_bet 
                players[k]['bank'] = players[k]['bank'] - players[k]['cash_on_bet']
                all_on_table = all_on_table + players[k]['cash_on_bet']
            else:
                players[k]['cash_on_bet'] = 0
    extra_for_zeros = 0
    if all_on_table > 0 and all_on_table > zero_threshold:
        extra_for_zeros = math.ceil(float(float(all_on_table) * float(zero_pct)))
    for k in players.keys():
        if extra_for_zeros > min_bet and players[k]['bank'] > extra_for_zeros:
            players[k]['cash_on_zero'] = extra_for_zeros
            players[k]['bank'] = players[k]['bank'] - players[k]['cash_on_zero']
        else:         
            players[k]['cash_on_zero'] = 0

    print "SPIN #%s" % i
    hit_num = random.randrange(1,39) - 2
    print "HIT_NUM = %s" % hit_num
    if hit_num not in numbers_hit.keys():
        numbers_hit[hit_num] = 1
    else:
        numbers_hit[hit_num] = numbers_hit[hit_num] + 1
    for k in players.keys():
        this_win = 0
        if players[k]['cash_on_bet'] > 0:
            #print "PLAYER %s, HIT NUM = %s, in %s?" % (k, hit_num, players[k]['current_range'])
            if hit_num in players[k]['current_range']:
                # They win
                #print "THATS A WIN"
                this_win = players[k]['cash_on_bet'] * 3
                players[k]['last_was_win'] = True
                players[k]['wins'] = players[k]['wins'] + 1
            else:
                #print "THATS A LOSE"
                players[k]['last_was_win'] = False
                players[k]['losses'] = players[k]['losses'] + 1
               
            if players[k]['history'] == '':
                players[k]['history'] = this_win
            else:
                players[k]['history'] = '%s,%s' % (players[k]['history'], this_win)
    
        z_win = 0
        if players[k]['cash_on_zero'] > 0:
            print "Player #%s TRIED 0" % k
            if hit_num in [-1,0]:
                z_win = players[k]['cash_on_zero'] * 18
                players[k]['zwins'] = players[k]['zwins'] + 1
                #print "HIT!"
            else:
                players[k]['zlosses'] = players[k]['zlosses'] + 1
                #print "MISS!"

            if players[k]['history'] == '':
                players[k]['history'] = 'Z%s' % z_win
            else:
                players[k]['history'] = '%s,Z%s' % (players[k]['history'], z_win)
                    
        this_win = this_win + z_win
        players[k]['bank'] = players[k]['bank'] + this_win 
        if players[k]['bank'] > players[k]['biggest_bank']:
            players[k]['biggest_bank'] = players[k]['bank']
        if players[k]['bank'] < players[k]['smallest_bank']:
            players[k]['smallest_bank'] = players[k]['bank']
    total = 0
    for k in players.keys():
        guy = players[k]
        total = guy['bank'] + total
        print "PLAYER: %s\tCURRENT THIRD:%s\tCURRENTBANK: %s\tCASH_ON_BET: %s\tCASH_ON_ZERO: %s\tWINS: %s\tLOSSES: %s\tZWINS: %s\tZLOSSES: %s\tSMALLEST BANK: %s\tBIGGEST BANK: %s" % (k, guy['range_num'], guy['bank'], guy['cash_on_bet'], guy['cash_on_zero'], guy['wins'], guy['losses'], guy['zwins'], guy['zlosses'], guy['smallest_bank'], guy['biggest_bank'])
    print 'TOTAL IN BANK: %s' % total
    print '\n\n'
print '\n\n'
for k in players.keys():
    print "PLAYER #%s: %s" % (k, players[k]['history'])
print '\n\n'
for i in range(-2,40):
    if i in numbers_hit.keys():
        print "%s: %s" % (i, numbers_hit[i])



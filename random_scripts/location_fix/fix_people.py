import os, sys, math, hashlib, getopt, tacticenv, time
from tactic_client_lib import TacticServerStub
def kill_mul_spaces(origstrg):
    newstrg = ''
    for word in origstrg.split():
        newstrg=newstrg+' '+word
    return newstrg
def extract_key_and_value(xml_string):
    chunker = xml_string.split('"')
    key = chunker[1]
    first_chunk = chunker[2].split('</')[0]
    value = first_chunk[1:]
    return [key, value]
def split_and_insert(in_str, ch, missing_ch):
    new_str = in_str
    changed = False
    if ch in in_str:
        splits = in_str.split(ch)
        for sp in splits:
            if sp != '':
                if sp[len(sp) - 2] != missing_ch:
                    if changed:
                        new_str = '%s%s%s%s' % (new_str, sp[:len(sp) - 2], missing_ch, ch) 
                    else:
                        new_str = '%s%s%s' % (sp[:len(sp) - 2], missing_ch, ch) 
                    changed = True
    return new_str
def correct_quotes(in_str):
    in_str = split_and_insert(in_str, "'", "\\")
    in_str = split_and_insert(in_str, '"', "\\")
    in_str = split_and_insert(in_str, "`", "\\")
    return in_str
def internal_search_by_code(code, lookup_dict):
    send_back = None
    for guy in lookup_dict:
        if code == guy.get('code'):
            send_back = guy
            break
    return send_back
def make_table_dict(filename):
    f= open(filename, 'r')
    data = []
    line_data = {}
    counter = 0
    columns = None
    for line in f:
        if not line.strip():
            continue
        else:
	    line = line.rstrip('\r\n')
            if counter == 0:
                columns = line.split('\t')
            else:
                line_data = {}
                splitted = line.split('\t')
                count2 = 0
                for spli in splitted:
                    line_data[kill_mul_spaces(columns[count2]).strip()] = kill_mul_spaces(spli).strip()
                    count2 = count2 + 1
                data.append(line_data)
            counter = counter + 1
        
    f.close()
    return data
     
server = TacticServerStub.get(protocol="xmlrpc")
#server.start('FIXING SOURCES AND THINGS')
logins = server.eval("@SOBJECT(sthpw/login)")
persons = server.eval("@SOBJECT(twog/person)")
prolly_ok = []
prolly_bad = []
dupes = []
for guy in logins:
    stored = False
    login = guy.get('login')
    poss_pers_1 = server.eval("@SOBJECT(twog/person['login_name','%s'])" % login)
    if poss_pers_1 not in [None,[]]:
        if len(poss_pers_1) > 1:
            for dude in poss_pers_1:
                dupes.append([login,dude.get('code'), dude.get('first_name'), dude.get('last_name')])    
                stored = True
        else:
            poss_pers_1 = poss_pers_1[0]
            prolly_ok.append([login, poss_pers_1.get('code'), poss_pers_1.get('first_name'), poss_pers_1.get('last_name')])
            stored = True
    else:
        poss_pers_2 = server.eval("@SOBJECT(twog/person['first_name','~','%s']['last_name','~','%s'])" % (guy.get('first_name'), guy.get('last_name')))
        if poss_pers_2 not in [None,[]]:
            if len(poss_pers_2) > 1:
                for dude in poss_pers_2:
                    dupes.append([login, dude.get('code'), dude.get('first_name'), dude.get('last_name')])    
                    stored = True
            else:
                poss_pers_2 = poss_pers_2[0]
                prolly_ok.append([login, poss_pers_2.get('code'), poss_pers_2.get('first_name'), poss_pers_2.get('last_name')])
                stored = True
    if not stored:
        prolly_bad.append([login, guy.get('first_name'), guy.get('last_name')])

person_fixer = open('sql_update_person_fixer', 'w')
for prol in prolly_ok:
    person_fixer.write('Prolly Good Login: %s, Person Code: %s, Person Name: %s %s\n' % (prol[0], prol[1], prol[2], prol[3]))
for dupe in dupes:
    person_fixer.write('Dupe Login?: %s, Person Code: %s, Person Name: %s %s\n' % (dupe[0], dupe[1], dupe[2], dupe[3]))
for prol in prolly_bad:
    person_fixer.write('Prolly Bad Login: %s, First_Name: %s, Last_Name: %s\n' % (prol[0], prol[1], prol[2]))
        
person_fixer.close()

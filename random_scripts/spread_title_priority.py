import os, sys, math, hashlib, getopt, tacticenv, time
opts, file_name = getopt.getopt(sys.argv[1], '-m')

new_lines = []
f= open(file_name, 'r')
for line in f:
    if not line.strip():
        continue
    else:
        line = line.rstrip('\r\n')
        line = line.strip()
        line_s = line.split('|')
        title_code = line_s[0].strip()
        priority = line_s[1].strip()
        new_str = "update title set audio_priority = %s, compression_priority = %s, edeliveries_priority = %s, edit_priority = %s, machine_room_priority = %s, media_vault_priority = %s, qc_priority = %s, vault_priority = %s where code = '%s';" % (priority, priority, priority, priority, priority, priority, priority, priority, title_code) 
        new_lines.append(new_str)
f.close()
for i in new_lines: 
    print i

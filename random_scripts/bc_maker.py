import os, sys, math, hashlib, getopt, tacticenv
from tactic_client_lib import TacticServerStub
server = TacticServerStub.get(protocol='xmlrpc')
server.start('IMPORTING LOCATIONS AND THINGS')
chunks = {
            '1': ['ABCDEFGHI',5660,5668], 
            '2': ['ABCDEFGHI',5669,5677], 
            '3': ['ABCDEFGHI',5678,5686], 
            '4': ['ABCDEFGHI',5687,5695], 
            '5': ['ABCDEFGHI',5696,5704], 
            '6': ['ABCDEFGHI',5705,5713], 
            '7': ['ABCDEFGHI',5714,5722], 
            '8': ['ABCDEFGHI',5723,5731], 
            '9': ['ABCDEFGHI',5732,5740], 
            '10': ['ABCDEFGHI',5741,5749], 
            '11': ['ABCDEFGHI',5750,5758], 
            '12': ['ABCDEFGHI',5759,5767], 
            '13': ['ABCDEFGHI',5768,5776], 
            '14': ['ABCDEFGHI',5777,5785], 
            '15': ['ABCDEFGHI',5786,5794], 
            '16': ['ABCDEFGHI',5795,5803], 
            '17': ['ABCDEF',5804,5809], 
            '18': ['ABCDEF',5810,5815], 
            '19': ['ABCDEF',5816,5821], 
            '20': ['ABCDEF',5822,5827], 
            '21': ['ABCDEF',5828,5833], 
            '22': ['ABCDEF',5834,5839], 
            '23': ['ABCDEF',5840,5845], 
            '24': ['ABCDEF',5846,5851], 
            '25': ['ABCDEF',5852,5857], 
            '26': ['ABCDEF',5858,5863], 
            '27': ['ABCDEF',5864,5869], 
            '28': ['ABCDEF',5870,5875], 
            '29': ['ABCDEF',5876,5881], 
            '30': ['ABCDEF',5882,5887], 
            '31': ['ABCDEF',5888,5893], 
            '32': ['ABCDEF',5894,5899], 
            '33': ['ABCDEFGHIJKLMN',5900,5913], 
            '34': ['ABCDEFGHIJKLMN',5914,5927], 
            '35': ['ABCDEFGHIJKLMN',5928,5941], 
            '36': ['ABCDEFGHIJKLMN',5942,5955], 
            '37': ['ABCDEFGHI',5956,5964], 
            '38': ['ABCDEFGHI',5965,5973], 
            '39': ['ABCDEFGHI',5974,5982], 
            '40': ['ABCDEFGHI',5983,5991], 
            '41': ['ABCDEFGHI',6020,6028], 
            '42': ['ABCDEFGHI',6029,6037]
         } 
for k in chunks.keys():
    letters = chunks[k][0]
    first_num = chunks[k][1]
    last_num = chunks[k][2]
    current_number = first_num
    for letter in letters:
        if current_number <= last_num:
            server.insert('twog/inhouse_locations', {'name': 'Vault Column %s, Row %s' % (k, letter), 'barcode': '2G00%s' % current_number})
            current_number = current_number + 1
                    
                
server.finish()

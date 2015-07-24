__all__ = ["IMDBImageAssociatorCmd"]
import os, time
from pyasm.command import Command, CommandException


class IMDBImageAssociatorCmd(Command):

    def __init__(my, **kwargs):
        from client.tactic_client_lib import TacticServerStub
        super(IMDBImageAssociatorCmd, my).__init__(**kwargs)
        my.orders_str = str(kwargs.get('orders_to_associate'))
        my.orders = my.orders_str.split(',')
        my.server = TacticServerStub.get()

    def check(my):
        return True
    
    def execute(my):   
        import urllib
        from pyasm.checkin import FileCheckin
        from pyasm.search import Search
        pic_dict = {}
        pics = []
        order_dict = {}
        for ocode in my.orders:
            order = my.server.eval("@SOBJECT(twog/order['code','%s'])" % ocode)[0]
            ord_s = Search('twog/order')
            ord_s.add_filter('code',ocode)
            order = ord_s.get_sobject()
            if order:
                order_dict[ocode] = order
                poster = order.get_value('imdb_poster_url')
                if poster not in pics:
                    pics.append(poster)
                    pic_dict[poster] = [ocode]
                else:
                    pic_dict[poster].append(ocode)
        pic_places = {}
        number = 0
        for pic in pics:
            extension_s = pic.split('.')
            extension = extension_s[len(extension_s) - 1]
            place = '/var/www/html/imdb_images/associator%s.%s' % (number, extension) 
            f = open(place,'wb')
            f.write(urllib.urlopen(pic).read())
            f.close()
            pic_places[pic] = place
            number = number + 1

        for pic in pics:
            server_path = pic_places[pic]
            linked_orders = pic_dict[pic]
            for ocode in linked_orders: 
                sobject = order_dict[ocode]
                if sobject:
                    file_types = ['main']
                    context = "icon"
                    checkin = FileCheckin(
                        sobject,
                        file_paths=server_path,
                        file_types=file_types,
                        context=context,
                        mode="copy"
                    )
                    checkin.execute()

        
            

        return ''


    def check_security(my):
        '''give the command a callback that allows it to check security'''
        return True

    def get_title(my):
        return "Make Note"
        
         


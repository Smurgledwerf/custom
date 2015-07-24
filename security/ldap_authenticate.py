###########################################################
#
# Copyright (c) 2005, Southpaw Technology
#                     All Rights Reserved
#
# PROPRIETARY INFORMATION.  This software is proprietary to
# Southpaw Technology, and is not to be reproduced, transmitted,
# or disclosed in any way without written permission.
#
#
#
__all__ = ['CustomLdapAuthenticate']
#import tacticenv
import hashlib
import ldap

from pyasm.common import SecurityException, Config, Common
from pyasm.security import Login, Authenticate
from pyasm.search import Search



class CustomLdapAuthenticate(Authenticate):
    '''Authenticate using LDAP logins'''

    def get_mode(my):
        '''let config decide whether it's autocreate or cache'''
        return None

    def verify(my, login_name, password):
        # replace cn=attribute with cn={login} in the config ldap_path
        # e.g. cn={login},o=organization,ou=server,dc=domain
        path = Config.get_value("security", "ldap_path")
        server = Config.get_value("security", "ldap_server")
        assert path, server

        my.login_name = login_name
        my.internal = True
        path = path.replace("{login}", login_name)
        #import ldap

        try:
            l = ldap.open(server)
            l.simple_bind_s(path, password)
            l.unbind()
            return True
        except: 
            login = Login.get_by_login(login_name)
            # check if it's an external account and verify with standard approach
            if login and login.get_value('location', no_exception=True) == 'external':
                auth_class = "pyasm.security.TacticAuthenticate"
                authenticate = Common.create_from_class_path(auth_class)
                is_authenticated = authenticate.verify(login_name, password)
                if is_authenticated == True:
                    my.internal = False
                    return True
            elif login:
                auth_class = "pyasm.security.TacticAuthenticate"
                authenticate = Common.create_from_class_path(auth_class)
                is_authenticated = authenticate.verify(login_name, password)
                if is_authenticated == True:
                    my.internal = False
                    return True
            raise SecurityException("Login/Password combination incorrect")

    def add_user_info(my, login, password):
        '''update password, first and last name  in tactic account'''
        if not my.internal:
            return

        encrypted = hashlib.md5(password).hexdigest()
        login.set_value("password", encrypted)
        first = ''
        last = ''
        if len(my.login_name.split('.')) > 1:
            first, last = my.login_name.split('.',1)
        else:
            first = my.login_name.split('.')[0]
        if len(first) > 0:
            first = '%s%s' % (first[0].upper(), first[1:])
        if len(last) > 0:
            last = '%s%s' % (last[0].upper(), last[1:])
        
        login.set_value("first_name", first)
        login.set_value("last_name", last)
        login.set_value("license_type", 'user')
        login.set_value("location", "internal")
        login.set_value("email", '%s@2gdigital.com'%my.login_name)

        # Hard code adding this user to a group so he can view projects
        # this can't be done in a trigger yet
        login_in_group = Search.eval("@SOBJECT(sthpw/login_in_group['login','%s']['login_group','user'])" %my.login_name, single=True)
        if not login_in_group:
            login.add_to_group("user")


if __name__ == '__main__':
    ldap_server = 'moonlight.2gdigitalpost.local'
    l = ldap.open(ldap_server)
    user_name = 'boris.lai@2gdigitalpost.local'
    #ldap_path = 'cn=%sou=unit,dc=2GDIGITALPOST,dc=tld' %user_name
    ldap_path = user_name
    password = '2gdigital'
    try:
        num = l.simple_bind_s(ldap_path, password)
        dn = l.whoami_s()
        l.unbind()
    except:
        raise


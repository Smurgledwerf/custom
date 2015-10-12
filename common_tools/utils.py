"""
Common utility functions for tactic.
"""

__author__ = 'topher.hughes'
__date__ = '02/09/2015'

from tactic_client_lib import tactic_server_stub


def get_server():
    """

    :return:
    """
    try:
        server = tactic_server_stub.TacticServerStub.get()
    except tactic_server_stub.TacticApiException as e:
        # TODO: get a server object some other way
        raise e

    return server


def get_project_setting(key, search_type=None, server=None):
    """

    :param key:
    :param search_type:
    :return:
    """
    if not server:
        server = get_server()


def replace_multiple(string, rep_dict):
    """Does the equivalent of multiple string replaces all at once.
    Note that it's simultaneous and not in order.

    :param string: the string to replace
    :param rep_dict: dictionary of {'old': 'new'}
    :return: the new string with applied replaces
    """
    import re
    pattern = re.compile("|".join([re.escape(k) for k in rep_dict.keys()]), re.M)
    return pattern.sub(lambda x: rep_dict[x.group(0)], string)


def fix_date(date):
    # This is needed due to the way Tactic deals with dates (using timezone info), post v4.0
    from pyasm.common import SPTDate
    return_date = ''
    date_obj = SPTDate.convert_to_local(date)
    if date_obj not in [None, '']:
        return_date = date_obj.strftime("%Y-%m-%d  %H:%M")
    return return_date


def get_sobject_type(search_key):
    """Get the sobject type from the search key or search_type.
    This essentially strips the project and code, returning only
    the sobject's type, like 'order', 'title', 'proj', 'work_order'

    Ex. 'twog/order?project=twog&code=ORDER19297' will return 'order'

    :param search_key: an sobject search key
    :return: the sobject type as a string
    """
    sobject_type = search_key.split('?')[0].split('/')[1]
    return sobject_type


def get_base_url(server=None, project='twog'):
    """
    Gets the base url for tactic. This would be used to get the
    beginning of a custom url (like for the order_builder).

    Note: the server from the browser already has .2gdigital.com

    :param server: a TacticServerStub object
    :param project: the project as a string
    :return: the base url as a string
    """
    if not server:
        server = get_server()

    url = 'http://{0}/tactic/{1}/'.format(server.server_name, project)
    return url


def get_edit_wdg_from_search_key(search_key, server=None, project='twog'):
    """
    Convenience function for getting the edit widget url from a search key.

    Ex. get_edit_wdg_from_search_key('twog/source?project=twog&code=SOURCE178165')
    -> 'http://tactic01.2gdigital.com/tactic/twog/sobject/twog/source/SOURCE178165'

    :param search_key: the search key of an sobject
    :param server: a tactic server stub object
    :param project: the project as a string
    :return: a url to the sobject's view
    """
    search_type = search_key.split('?')[0]
    sobject_code = search_key.split('code=')[1]
    return get_edit_wdg_url(search_type, sobject_code, server, project)


def get_edit_wdg_url(search_type, sobject_code, server=None, project='twog'):
    """
    Gets the url for the view/edit widget

    Ex. get_edit_wdg_url('twog/title', 'TITLE1337')
    -> 'http://tactic01.2gdigital.com/tactic/twog/sobject/twog/title/TITLE1337'

    :param search_type: the tactic search type
    :param sobject_code: the sobject's code
    :param server: a tactic server stub object
    :param project: the project as a string
    :return: a url to the sobject's view
    """
    if not server:
        server = get_server()

    base_url = get_base_url(server, project)
    return "{0}sobject/{1}/{2}".format(base_url, search_type, sobject_code)


def get_edit_wdg_hyperlink(search_type, sobject_code, sobject_name='', server=None, project='twog'):
    """
    Convenience function to get the hyperlink for the view/edit widget.

    Ex. get_edit_wdg_url('twog/title', 'TITLE1337', 'Awesome Movie')
    -> '<a href="http://tactic01.2gdigital.com/tactic/twog/sobject/twog/title/TITLE1337">Awesome Movie</a>'

    :param search_type: the tactic search type
    :param sobject_code: the sobject's code
    :param sobject_name: the name of the sobject, to use for the link
    :param server: a tactic server stub object
    :param project: the project as a string
    :return: a url to the sobject's view
    """
    if not server:
        server = get_server()

    href = '<a href="{0}">{1}</a>'
    url = get_edit_wdg_url(search_type, sobject_code, server=server, project=project)
    if not sobject_name:
        sobject_name = sobject_code

    return href.format(url, sobject_name)


def get_order_builder_url(order_code, server=None, project='twog'):
    """
    Gets the order builder url for the given order code.
    Note that this does not format it as a hyperlink.

    Ex. get_order_builder_url('ORDER12345')
    -> 'http://tactic01.2gdigital.com/tactic/twog/order_builder/ORDER12345'

    :param order_code: the order code as a string
    :param server: a tactic server stub object
    :param project: the project as a string
    :return: a url to the order builder page
    """
    if not server:
        server = get_server()

    base_url = get_base_url(server, project)
    return "{0}order_builder/{1}".format(base_url, order_code)

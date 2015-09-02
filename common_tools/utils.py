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
    except tactic_server_stub.TacticApiException:
        pass


def get_project_setting(key, search_type=None, server=None):
    """

    :param key:
    :param search_type:
    :return:
    """
    if not server:
        server = get_server()

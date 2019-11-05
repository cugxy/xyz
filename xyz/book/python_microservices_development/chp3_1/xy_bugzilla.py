# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       xy_bugzilla.py
   Description :
   Author :          cugxy
   date：            2019/11/4
-------------------------------------------------
   Change Activity:
                     2019/11/4
-------------------------------------------------
"""
import requests


class XYBugzilla(object):
    def __init__(self, account, server='https://bugzilla.mozilla.org'):
        self.account = account
        self.server = server
        self.session = requests.session()

    def bug_link(self, bug_id):
        return '%s/show_bug.cgi?id=%s' % (self.server, bug_id)

    def get_new_bugs(self):
        call = self.server + '/rest/bug'
        params = {'assigned_to': self.account,
                  'status': 'NEW',
                  'limit': 10}
        try:
            tmp = self.session.get(call, params=params)
            res = tmp.json()
        except requests.exceptions.ConnectionError:
            res = {'bugs': []}

        def _add_link(bug):
            bug['link'] = self.bug_link(bug['id'])
            return bug

        for bug in res['bugs']:
            yield _add_link(bug)




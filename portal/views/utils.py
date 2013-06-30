# -*- coding: utf-8 -*-
"""
Some helper function
"""

from django.shortcuts import render_to_response

from portal import models


def render(template_name, payment):
    return render_to_response('portal/%s' % template_name,
                              payment)


def set_session(req, username):
    req.session['username'] = username


def unset_session(req, username):
    del req.session['username']


def get_user_obj(req):
    """Since the method is invoked after check_authentication(),
    so I assume 'username' always in session.
    """
    username = req.session.get('username')
    return models.User.objects.filter(username=username)[0]

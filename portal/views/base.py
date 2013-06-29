# -*- coding: utf-8 -*-
"""
The basic view logic here.

For example: signin, signup, homepage , etc.
"""

import logging
import functools

from portal import forms
from portal import models
from portal.views import utils

LOG = logging.getLogger(__name__)


def check_authentication(func):
    """The decorator will check username existed in session. If it is continue.
    """
    @functools.wraps(func)
    def _check_authentication(req):
        username = req.session.get('username')
        if not username:
            return signin(req)
        else:
            return func(req)

    return _check_authentication


def signin(req):
    """登陆"""
    if req.method == 'GET':
        form = forms.SignInForm()
        return utils.render('sign_in.html', {'form': form})
    elif req.method == 'POST':
        form = forms.SignInForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            users = models.User.objects.filter(username=data['username'])
            if users and users[0].password == data['password']:
                LOG.debug('%s login success.' % users)
                utils.set_session(req, users[0].username)
                return portal(req)
            else:
                LOG.debug("%s login failed." % users)
                return utils.render('sign_in.html',
                                {'errors': 'Username or password wrong',
                                 'form': form})
        else:
            return utils.render('sign_in.html', {'form': form})


def signup(req):
    """注册"""
    if req.method == 'GET':
        form = forms.SignUpForm()
        return utils.render('sign_up.html', {'form': form})
    elif req.method == 'POST':
        form = forms.SignUpForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = models.User(**data)
            user.save()
            return utils.render('portal.html', {})
        else:
            return utils.render('sign_up.html', {'form': form})


def portal(req):
    user = utils.get_user_obj(req)
    houses = user.house_set.all()
    orders = user.order_set.all()
    return utils.render('portal.html', {'houses': houses,
                                        'orders': orders})


@check_authentication
def chargerent(req):
    pass


@check_authentication
def payrent(req):
    pass

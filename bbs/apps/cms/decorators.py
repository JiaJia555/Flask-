# @ Time    : 2020/5/11 20:51
# @ Author  : JuRan

from flask import session, redirect, url_for


def login_required(func):
    def inner(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))
    return inner
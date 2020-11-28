# @ Time    : 2020/5/8 21:27
# @ Author  : JuRan

from flask import (
    Blueprint,
    render_template,
    views,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    g
)

from apps.cms.forms import LoginForm, ResetPwdForm
from apps.cms.models import CMSUser
from exts import db
from utils import restful

from .decorators import login_required

cms_bp = Blueprint("cms", __name__, url_prefix='/cms')
from .hooks import before_request


@cms_bp.route("/")
# @login_required
def index():
    # print(session.get('user_id'))
    # return "cms index"
    return render_template("cms/cms_index.html")


@cms_bp.route('/logout/')
def logout():
    # 删除session  user_id
    # 重定向 登录页面
    del session['user_id']
    return redirect(url_for('cms.login'))

# @cms_bp.route('/test/')
# def demo():
#     return "测试是否可以访问"

@cms_bp.route("/profile/")
def profile():
    return render_template("cms/cms_profile.html")


class LoginView(views.MethodView):

    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        login_form = LoginForm(request.form)
        if login_form.validate():
            # 数据库验证
            email = login_form.email.data
            password = login_form.password.data
            remember = login_form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            # 验证用户是否存在  以及密码是否正确
            if user and user.check_password(password):
                session['user_id'] = user.id
                if remember:
                    session.permanent = True
                # 登录成功 跳转首页
                return redirect(url_for('cms.index'))
            else:
                # render_template('cms/cms_login.html', message="邮箱或者密码错误")
                return self.get(message="邮箱或者密码错误")
        else:
            # print(login_form.errors.popitem()[1][0])
            # message = login_form.errors.popitem()[1][0]
            # return "表单验证错误"
            return self.get(message=login_form.get_error())


class ResetPwdView(views.MethodView):

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            # 对象
            user = g.cms_user
            # 用户提交的数据 juran 密码 是否和数据库中一直
            if user.check_password(oldpwd):
                # 更新我的密码
                user.password = newpwd
                db.session.commit()
                # return jsonify({"code": 200, "message": ""})
                return restful.success()
            else:
                # return jsonify({"code": 400, "message": "旧密码错误"})
                return restful.params_errors(message="旧密码错误")
        else:
            # ajax json类型的数据
            # message = form.errors.popitem()[1][0]
            # return jsonify({"code": 400, "message": message})
            return restful.params_errors(message=form.get_error())


class ResetEmailView(views.MethodView):

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        pass


cms_bp.add_url_rule("/login/", view_func=LoginView.as_view('login'))
cms_bp.add_url_rule("/resetpwd/", view_func=ResetPwdView.as_view('resetpwd'))
cms_bp.add_url_rule("/resetemail/", view_func=ResetEmailView.as_view('resetemail'))


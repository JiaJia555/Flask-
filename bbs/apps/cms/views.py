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

from apps.cms.forms import LoginForm, ResetPwdForm, ResetEmailForm
from apps.cms.models import CMSUser
from exts import db, mail
from utils import restful, random_captcha, lgcache
from flask_mail import Message


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
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            # 查询数据库
            # CMSUser.query.filter_by(email=email).first()
            # CMSUser.query.filter(CMSUser.email==email).first()

            g.cms_user.email = email
            db.session.commit()
            return restful.success()

        else:
            return restful.params_errors(form.get_error())

# 发送邮件
@cms_bp.route("/send_mail/")
def send_mail():
    message = Message('邮件发送', recipients=['2705185834@qq.com'], body='测试邮件发送')
    mail.send(message)
    return '邮件已发送'


# 邮件发送
class EmailCaptcha(views.MethodView):
    def get(self):
        email = request.args.get('email')
        if not email:
            return restful.params_errors('请传递邮箱参数')

        # 发送邮件  内容发送一个验证码 4 6 数字和英文组合
        captcha = random_captcha.get_random_captcha(4)
        message = Message('逻辑论坛邮箱验证码', recipients=[email], body='您的验证码是 %s' % captcha)
        try:
            mail.send(message)
        except:
            return restful.server_errors()

        # 验证码 保存下来 MySQL 过期时间  Redis 效率  key email value captcha
        lgcache.redis_set(email, captcha)
        return restful.success()


cms_bp.add_url_rule("/login/", view_func=LoginView.as_view('login'))
cms_bp.add_url_rule("/resetpwd/", view_func=ResetPwdView.as_view('resetpwd'))
cms_bp.add_url_rule("/resetemail/", view_func=ResetEmailView.as_view('resetemail'))
cms_bp.add_url_rule("/email_captcha/", view_func=EmailCaptcha.as_view('email_captcha'))


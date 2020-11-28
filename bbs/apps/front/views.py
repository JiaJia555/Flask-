# @ Time    : 2020/5/8 21:27
# @ Author  : JuRan
from flask import Blueprint, views, render_template, make_response, request, session
from utils.captcha import Captcha
from utils import lgcache, restful, safe_url
from io import BytesIO
from .forms import SignupForm, SigninForm
from .models import FrontUser
from exts import db



front_bp = Blueprint("front", __name__)


@front_bp.route("/")
def index():
    return render_template('front/front_index.html')


@front_bp.route('/captcha/')
def graph_captcha():
    try:
        text, image = Captcha.gene_graph_captcha()
        lgcache.redis_set(text.lower(), text.lower())
        # BytesIO 字节流
        out = BytesIO()
        # 把图片保存在字节流中  并制定格式png
        image.save(out, 'png')
        # 文件流指针
        out.seek(0)
        resp = make_response(out.read())
        resp.content_type = 'image/png'
    except:
        return graph_captcha()
    return resp


@front_bp.route('/test/')
def test():
    return render_template('front/test.html')


class SignupView(views.MethodView):

    def get(self):
        # 在当前的页面  None
        # referrer  页面的跳转
        # http://127.0.0.1:5000/test/ => www.baidu.com
        # print(request.referrer)
        return_to = request.referrer
        # print(safe_url.is_safe_url(return_to))
        # is_safe_url 请求是否来自站内
        if return_to and return_to != request.url and safe_url.is_safe_url(return_to):
            # text, image = Captcha.gene_graph_captcha()
            # print(text)
            # print(image)
            return render_template("front/front_signup.html", return_to=return_to)
        else:
            return render_template('front/front_signup.html')


    def post(self):
        form = SignupForm(request.form)

        # 表单验证
        if form.validate():
            # 保存到数据库
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data

            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_errors(message=form.get_error())


class SigninView(views.MethodView):

    def get(self):
        # http://127.0.0.1:5000/signin/
        # print(request.url)  当前的URL地址
        return_to = request.referrer
        if return_to and return_to != request.url and safe_url.is_safe_url(return_to):
            return render_template('front/front_signin.html', return_to=return_to)
        else:
            return render_template('front/front_signin.html')


    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data

            # user = FrontUser.query.filter(FrontUser.telephone == telephone).first()
            user = FrontUser.query.filter_by(telephone=telephone).first()

            if user and user.check_password(password):
                session['user_id'] = user.id
                if remember:
                    # 持久化
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_errors(message='手机号或者密码错误')

        else:
            return restful.params_errors(message=form.get_error())


front_bp.add_url_rule("/signup/", view_func=SignupView.as_view('signup'))
front_bp.add_url_rule("/signin/", view_func=SigninView.as_view('signin'))


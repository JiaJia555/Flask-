# @ Time    : 2020/5/8 21:27
# @ Author  : JuRan

from flask import Blueprint, render_template, views

cms_bp = Blueprint("cms", __name__, url_prefix='/cms')


@cms_bp.route("/")
def index():
    return "cms index"


class LoginView(views.MethodView):
    def get(self):
        return render_template('cms/cms_login.html')


cms_bp.add_url_rule("/login/", view_func=LoginView.as_view('login'))


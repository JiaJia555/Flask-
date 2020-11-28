# @ Time    : 2020/5/8 21:27
# @ Author  : JuRan
from flask import Blueprint, views, render_template, make_response
from utils.captcha import Captcha
from io import BytesIO

front_bp = Blueprint("front", __name__)


@front_bp.route("/")
def index():
    return "front index"


@front_bp.route('/captcha/')
def graph_captcha():
    try:
        text, image = Captcha.gene_graph_captcha()
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


class SingupView(views.MethodView):

    def get(self):
        text, image = Captcha.gene_graph_captcha()
        # print(text)
        # print(image)
        return render_template("front/front_signup.html")




front_bp.add_url_rule("/singup/", view_func=SingupView.as_view('singup'))



#
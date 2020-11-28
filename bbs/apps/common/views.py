# @ Time    : 2020/5/8 21:27
# @ Author  : JuRan

from utils import send_msg, restful
from flask import Blueprint, request
from utils.captcha import Captcha
from .forms import SMSCaptchaForm


common_bp = Blueprint("common", __name__, url_prefix='/c')


# 只要到当前的请求 就会发生短信
# @common_bp.route("/sms_captcha/", methods=['POST'])
# def sms_captcha():
#     telephone = request.form.get('telephone')
#
#     if not telephone:
#         return restful.params_errors(message='请填写手机号码')
#
#     captcha = Captcha.gene_text(number=4)
#
#     if send_msg.send_mobile_msg(telephone, captcha) == 0:
#         return restful.success()
#     else:
#         return restful.params_errors(message='发送失败')


@common_bp.route("/sms_captcha/", methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)

    if form.validate():
        return restful.success()

    else:
        return restful.params_errors(message='参数错误')
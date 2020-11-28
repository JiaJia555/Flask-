# @ Time    : 2020/5/8 21:27
# @ Author  : JuRan

from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo


class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message

#
class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请出入正确的邮箱地址'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
    remember = IntegerField()



# 表单提交上来的数据 是否符合要求
class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='密码长度有误')])
    newpwd = StringField(validators=[Length(6, 20, message='密码长度有误')])
    # 两次密码输入是否一致
    newpwd2 = StringField(validators=[EqualTo("newpwd", message="两次密码输入不一致")])


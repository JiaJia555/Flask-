# @ Time    : 2020/5/8 21:27
# @ Author  : JuRan

from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length


class LoginForm(Form):
    email = StringField(validators=[Email(message='请出入正确的邮箱地址'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
    remember = IntegerField()

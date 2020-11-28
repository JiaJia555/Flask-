# @ Time    : 2020/5/8 21:27
# @ Author  : JuRan

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class CMSPersmission(object):
    # 255二进制来表示所有的权限
    ALL_PERMISSION  = 0b11111111

    # 访问权限
    VISITOR         = 0b00000001

    # 管理帖子权限
    POSTER          = 0b00000010

    # 管理评论
    COMMENTER       = 0b00000100

    # 管理板块
    BOARDER         = 0b00001000

    # 管理前台用户
    FRONTUSER       = 0b00010000

    # 管理后台用户
    CMSUSER         = 0b00100000

    # 管理管理员用户
    ADMINER         = 0b01000000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True),
)


# 角色
class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=CMSPersmission.VISITOR)

    users = db.relationship('CMSUser', secondary=cms_role_user, backref='roles')



class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            # 获取角色的所有的权限
            all_permissions |= permissions

        return all_permissions

    # CMSPersmission.VISITOR
    def has_permission(self, permission):

        all_permissions = self.permissions
        # 0b11111111    用户的权限 0b00001000
        # 0b00000001  permission
        result = all_permissions & permission == permission
        return result

    @property
    def is_developer(self):
        return self.has_permission(CMSPersmission.ALL_PERMISSION)






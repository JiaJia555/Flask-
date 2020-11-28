# @ Time    : 2020/5/8 21:24
# @ Author  : JuRan
from flask_script import Manager
from bbs import app
from flask_migrate import Migrate, MigrateCommand
from exts import db
# 导入模型
from apps.cms.models import CMSUser


manager = Manager(app)

Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print("cms用户添加成功")


if __name__ == '__main__':
    manager.run()
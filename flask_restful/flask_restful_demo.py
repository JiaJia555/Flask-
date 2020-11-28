# @ Time    : 2020/5/8 20:36
# @ Author  : JuRan

from flask import Flask, render_template, url_for
from flask_restful import Api, Resource, reqparse, inputs, fields, marshal_with
import config
from exts import db
from models import Article

app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)

# 用Api来绑定app
api = Api(app)

class ArticleView(Resource):

    resource_fields = {
        # 'title': fields.String,
        'artcile_title': fields.String(attribute='title'),
        # 如果模型中有这个字段 而且有值 default 没有作用 数据库中有值的话 显示数据库中的值
        'content': fields.String(default='1234'),
        # 'author': fields.String,
        'author': fields.Nested({
            "username": fields.String,
            "email": fields.String
        }),
        # 'tags': fields.String
        'tags': fields.List(fields.Nested({
            "id": fields.Integer,
            "name": fields.String
        })),
        # 默认值
        'read_count': fields.Integer(default=0)
        # 'tags':
    }

    # 及时这个参数没有值,也会返回
    @marshal_with(resource_fields)
    def get(self, article_id):
        article = Article.query.get(article_id)
        # return {"title": "juran"}
        return article


api.add_resource(ArticleView, '/article/<article_id>', endpoint='article')


if __name__ == '__main__':
    app.run(debug=True, port=7000)
# @ Time    : 2020/5/8 21:27
# @ Author  : JuRan
from flask import Blueprint

front_bp = Blueprint("front", __name__)


@front_bp.route("/")
def index():
    return "front index"
from flask import Blueprint, abort, render_template, request

from requests import get

bp = Blueprint("proxy", __name__)


@bp.route("/image/<int:original_width>/<id>")
def image(original_width, id):
    try:
        response = get(f"https://miro.medium.com/max/{original_width}/{id}", timeout=15)
        return response.content, response.status_code, response.headers.items()
    except Exception as e:
        print(f"Error fetching image: {str(e)}")
        abort(500)


@bp.route("/iframe/")
def iframe():
    return render_template("iframe.html", url=request.args.get("url"))

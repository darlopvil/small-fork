from flask import Blueprint, render_template, abort

from small.services.medium_client import MediumClient
from small.utils.parse_article_id import parse_article_id

bp = Blueprint("articles", __name__)


@bp.route("/<path:article_url>")
def article(article_url):
    article_id = parse_article_id(article_url)
    if not article_id:
        abort(404)

    try:
        page = MediumClient.get_post(article_id)
        return render_template("article.html", page=page)
    except Exception as e:
        print(f"Error fetching article: {str(e)}")
        abort(500)

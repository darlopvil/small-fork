from flask import Blueprint, render_template, abort
from werkzeug.exceptions import NotFound

from small.services.medium_client import MediumClient
from small.services.github_client import GithubClient
from small.utils.parse_article_id import parse_article_id

bp = Blueprint("articles", __name__)


@bp.route("/<path:article_url>")
def article(article_url):
    article_id = parse_article_id(article_url)
    if not article_id:
        abort(404)

    try:
        page = MediumClient.get_post(article_id)

        if not page:
            abort(404)

        for paragraph in page.content:
            for child in paragraph.children:
                if child.__class__.__name__ == "GithubGist":
                    try:
                        gist = GithubClient.get_gist(child.id)
                        child.content = gist
                    except Exception as e:
                        print(f"Error fetching gist: {str(e)}")

        return render_template("article.html", page=page)
    except Exception as e:
        if isinstance(e, NotFound):
            raise

        print(f"Error fetching article: {str(e)}")
        abort(500)

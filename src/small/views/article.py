from flask import Blueprint, render_template, abort, url_for
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

        list_nest = []

        for paragraph in page.content:
            for child in paragraph.children:
                if child.__class__.__name__ == "GithubGist":
                    try:
                        gist = GithubClient.get_gist(child.id)
                        child.content = gist
                    except Exception as e:
                        print(f"Error fetching gist: {str(e)}")

                elif child.__class__.__name__ == "Text":
                    child.type = child.type.lower()

                    if child.type == "oli":
                        if not list_nest or not list_nest[-1] == "oli":
                            list_nest.append("oli")
                            child.prepend = "<ol>"

                        child.type = "li"

                    elif child.type == "uli":
                        if not list_nest or not list_nest[-1] == "uli":
                            list_nest.append("uli")
                            child.prepend = "<ul>"

                        child.type = "li"

                    else:
                        while list_nest:
                            if list_nest[-1] == "oli":
                                child.prepend += "</ol>"
                            elif list_nest[-1] == "uli":
                                child.prepend += "</ul>"

                            list_nest.pop()

                    # Handle other markups
                    child.markups = sorted(
                        child.markups, key=lambda x: x["start"], reverse=True
                    )

                    for markup in child.markups:
                        start_markup = f"""<{markup["type"].lower()} {" ".join([f"{k}='{v}'" for k, v in markup.items() if v and k != "type"])}>"""
                        end_markup = f"</{markup['type'].lower()}>"

                        child.content = (
                            child.content[: markup["start"]]
                            + start_markup
                            + child.content[markup["start"] : markup["end"]]
                            + end_markup
                            + child.content[markup["end"] :]
                        )

        # Close any open lists
        while list_nest:
            if list_nest[-1] == "oli":
                page.content[-1].children[-1].append += "</ol>"
            elif list_nest[-1] == "uli":
                page.content[-1].children[-1].append += "</ul>"

            list_nest.pop()

        return render_template("article.html", page=page)
    except Exception as e:
        if isinstance(e, NotFound):
            raise

        print(f"Error fetching article: {str(e)}")
        abort(500)

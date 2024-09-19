import requests

from flask import url_for

from small.models.nodes import Page, Paragraph, Text, Image, IFrame, GithubGist

from urllib.parse import quote
from datetime import datetime


class MediumClient:
    @staticmethod
    def get_post(post_id):
        url = "https://medium.com/_/graphql"
        query = (
            """
        query {
          post(id: "%s") {
            title
            createdAt
            creator {
              name
            }
            content {
              bodyModel {
                paragraphs {
                  type
                  text
                  metadata {
                    id
                    originalWidth
                    originalHeight
                  }
                  iframe {
                    mediaResource {
                      href
                      iframeSrc
                      iframeWidth
                      iframeHeight
                    }
                  }
                }
              }
            }
          }
        }
        """
            % post_id
        )

        response = requests.post(url, json={"query": query})
        data = response.json()["data"]["post"]

        if not data:
            return None

        paragraphs = []
        for p in data["content"]["bodyModel"]["paragraphs"]:
            if p["type"] == "IMG":
                children = [
                    Image(
                        src=url_for(
                            "proxy.image",
                            original_width=p["metadata"]["originalWidth"],
                            id=p["metadata"]["id"],
                        ),
                        alt=p["text"],
                        width=p["metadata"]["originalWidth"],
                        height=p["metadata"]["originalHeight"],
                    )
                ]
            elif p["type"] == "IFRAME":
                iframe = p["iframe"]["mediaResource"]
                if "gist.github.com" in iframe["href"]:
                    gist_id = iframe["href"].split("/")[-1]
                    children = [GithubGist(id=gist_id)]
                else:
                    src = quote(iframe["iframeSrc"] or iframe["href"], safe="")
                    url = url_for("proxy.iframe") + f"?url={src}"

                    children = [
                        IFrame(
                            src=url,
                            width=iframe["iframeWidth"],
                            height=iframe["iframeHeight"],
                        )
                    ]
            else:
                children = [Text(content=p["text"], type=p["type"])]
            paragraphs.append(Paragraph(children=children))

        return Page(
            title=data["title"],
            author=data["creator"]["name"],
            created_at=datetime.fromtimestamp(data["createdAt"] / 1000).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            content=paragraphs,
        )

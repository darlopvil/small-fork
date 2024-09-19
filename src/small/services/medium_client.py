import requests

from flask import url_for

from small.models.nodes import Page, Paragraph, Text, Image

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
            else:
                children = [Text(content=p["text"].strip(), type=p["type"])]
            paragraphs.append(Paragraph(children=children))

        return Page(
            title=data["title"],
            author=data["creator"]["name"],
            created_at=datetime.fromtimestamp(data["createdAt"] / 1000).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            content=paragraphs,
        )

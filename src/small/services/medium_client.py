import requests
from datetime import datetime
from urllib.parse import quote

from flask import url_for

from small.models.nodes import Page, Paragraph, Text, Image, IFrame, GithubGist


class MediumClient:
    POST_URL = "https://medium.com/_/graphql"
    PARAGRAPH_TAGS = {
        "H1": "h1",
        "H2": "h2",
        "H3": "h3",
        "H4": "h4",
        "P": "p",
        "BQ": "blockquote",
        "PQ": "blockquote",
        "PRE": "pre",
        "OLI": "li",
        "ULI": "li",
    }

    @staticmethod
    def _headers():
        return {
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0.0.0 Safari/537.36"
            ),
            "X-Apollo-Operation-Name": "FullPostQuery",
            "X-Obvious-CID": "web",
            "X-Xsrf-Token": "1",
        }

    @staticmethod
    def _query(post_id):
        return {
            "operationName": "FullPostQuery",
            "variables": {
                "postId": post_id,
                "postMeteringOptions": {},
            },
            "query": """
                query FullPostQuery($postId: ID!, $postMeteringOptions: PostMeteringOptions) {
                  post(id: $postId) {
                    title
                    createdAt
                    firstPublishedAt
                    latestPublishedAt
                    creator {
                      name
                    }
                    content(postMeteringOptions: $postMeteringOptions) {
                      bodyModel {
                        paragraphs {
                          id
                          name
                          href
                          type
                          text
                          layout
                          hasDropCap
                          markups {
                            title
                            type
                            href
                            userId
                            start
                            end
                            anchorType
                          }
                          metadata {
                            id
                            alt
                            originalWidth
                            originalHeight
                          }
                          iframe {
                            iframeWidth
                            iframeHeight
                            mediaResource {
                              id
                              iframeSrc
                              iframeWidth
                              iframeHeight
                              title
                              thumbnailUrl
                            }
                          }
                          mixtapeMetadata {
                            href
                            thumbnailImageId
                          }
                          codeBlockMetadata {
                            lang
                            mode
                          }
                        }
                      }
                    }
                  }
                }
            """,
        }

    @classmethod
    def _request_post(cls, payload):
        response = requests.post(
            cls.POST_URL,
            headers=cls._headers(),
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("post")

    @classmethod
    def _paragraph_tag(cls, paragraph_type):
        return cls.PARAGRAPH_TAGS.get(paragraph_type or "P", "p")

    @staticmethod
    def _timestamp_to_string(post_data):
        timestamp = (
            post_data.get("firstPublishedAt")
            or post_data.get("createdAt")
            or post_data.get("latestPublishedAt")
        )
        if not timestamp:
            return None

        return datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _paragraphs(post_data):
        content = post_data.get("content") or {}
        body_model = content.get("bodyModel") or {}
        return body_model.get("paragraphs") or []

    @staticmethod
    def _iframe_media_resource(paragraph):
        iframe = paragraph.get("iframe") or {}
        return iframe.get("mediaResource") or {}

    @classmethod
    def _build_child(cls, paragraph):
        paragraph_type = paragraph.get("type")
        metadata = paragraph.get("metadata") or {}

        if paragraph_type == "IMG" and metadata.get("id"):
            return Image(
                src=url_for(
                    "proxy.image",
                    original_width=metadata.get("originalWidth") or 0,
                    id=metadata["id"],
                ),
                alt=metadata.get("alt") or paragraph.get("text") or "",
                width=metadata.get("originalWidth") or 0,
                height=metadata.get("originalHeight") or 0,
            )

        if paragraph_type == "IFRAME":
            media_resource = cls._iframe_media_resource(paragraph)
            candidate_url = (
                paragraph.get("href")
                or media_resource.get("iframeSrc")
                or media_resource.get("thumbnailUrl")
                or ""
            )

            if "gist.github.com" in candidate_url:
                gist_id = candidate_url.rstrip("/").split("/")[-1]
                return GithubGist(id=gist_id)

            if candidate_url:
                src = quote(candidate_url, safe="")
                url = url_for("proxy.iframe") + f"?url={src}"
                iframe = paragraph.get("iframe") or {}

                return IFrame(
                    src=url,
                    width=media_resource.get("iframeWidth")
                    or iframe.get("iframeWidth")
                    or 0,
                    height=media_resource.get("iframeHeight")
                    or iframe.get("iframeHeight")
                    or 0,
                )

        return Text(
            content=paragraph.get("text") or "",
            type=paragraph_type or "P",
            tag=cls._paragraph_tag(paragraph_type),
            markups=paragraph.get("markups") or [],
        )

    @classmethod
    def _build_page(cls, post_data):
        paragraphs = [
            Paragraph(children=[cls._build_child(paragraph)])
            for paragraph in cls._paragraphs(post_data)
        ]

        return Page(
            title=post_data.get("title") or "Untitled",
            author=(post_data.get("creator") or {}).get("name") or "Unknown author",
            created_at=cls._timestamp_to_string(post_data),
            content=paragraphs,
        )

    @staticmethod
    def get_post(post_id):
        data = MediumClient._request_post(MediumClient._query(post_id))
        if data:
            return MediumClient._build_page(data)

        return None

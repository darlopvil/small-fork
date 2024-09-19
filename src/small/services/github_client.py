import requests


class GithubClient:
    @staticmethod
    def get_gist(gist_id):
        url = f"https://api.github.com/gists/{gist_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            files = data["files"]
            return {
                filename: file_data["content"] for filename, file_data in files.items()
            }
        else:
            return None

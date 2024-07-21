import base64
from pathlib import Path

from sample_finder.sources.source import Source


class SourceMalpedia(Source):
    NAME = "malpedia"
    URL_API = "https://malpedia.caad.fkie.fraunhofer.de/api"

    SUPPORTED_HASHES = ("md5", "sha256")

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._session.headers.update({"Authorization": f"apitoken {self._config['api_key']}"})

    def download_file(self, sample_hash: str, output_path: Path) -> bool:
        response = self._get(f"{self.URL_API}/get/sample/{sample_hash}/raw")
        if not response or not response.ok:
            return False

        response_json = response.json()
        data = base64.b64decode(response_json["packed"])

        with output_path.open("wb") as h_file:
            h_file.write(data)

        return True

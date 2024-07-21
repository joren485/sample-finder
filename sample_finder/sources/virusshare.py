import base64
from pathlib import Path

from loguru import logger

from sample_finder.sources.source import Source


class SourceVirusshare(Source):
    NAME = "virusshare"
    URL_API = "https://virusshare.com/apiv2"

    def __init__(self, config: dict) -> None:
        super().__init__(config)

    def download_file(self, sample_hash: str, output_path: Path) -> bool:
        response = self._get(
            f"{self.URL_API}/download", params={"apikey": self._config["api_key"], "hash": sample_hash}
        )
        if not response or response.status_code != 200:
            if response.status_code == 204:
                logger.warning("Rate limited")
            return False

        data = self._decrypt_zip(response.content)
        with output_path.open("wb") as h_file:
            h_file.write(data)

        return True

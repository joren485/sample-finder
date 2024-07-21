import base64
from pathlib import Path

from loguru import logger

from sample_finder.sources.source import Source


class SourceVirustotal(Source):
    NAME = "virustotal"
    URL_API = "https://www.virustotal.com/api/v3"

    URL_WEBAPP = "https://www.virustotal.com/gui/file"

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._session.headers.update({"x-apikey": self._config["api_key"]})
        self._is_premium = self._config.get("premium", False)

    def download_file(self, sample_hash: str, output_path: Path) -> bool:
        if self._is_premium:
            raise NotImplementedError

        response = self._get(f"{self.URL_API}/files/{sample_hash}")
        if not response or not response.ok:
            return False

        logger.success(f"Available on VirusTotal: {self.URL_WEBAPP}/{sample_hash}")

        return False

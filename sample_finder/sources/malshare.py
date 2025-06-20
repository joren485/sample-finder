from pathlib import Path

from sample_finder.sources.source import Source


class SourceMalshare(Source):
    """
    Implements MalShare Source.

    References
    ----------
        * https://malshare.com/doc.php

    """

    NAME = "malshare"
    URL_API = "https://malshare.com/api.php"
    SUPPORTED_HASHES = ("md5", "sha1", "sha256")

    def download_file(self, sample_hash: str, output_path: Path) -> bool:
        """Download a file from MalShare."""
        response = self._get(
            self.URL_API, params={"api_key": self._config["api_key"], "action": "getfile", "hash": sample_hash}
        )
        if not response or not response.ok:
            return False

        with output_path.open("wb") as h_file:
            h_file.write(response.content)

        return True

from pathlib import Path

import requests

from sample_finder.sources.source import Source


class SourceVirusExchange(Source):
    """
    Implements Virus.Exchange Source.

    References
    ----------
        * https://docs.virus.exchange/

    """

    NAME = "virusexchange"
    URL_API = "https://virus.exchange/api/samples/"
    SUPPORTED_HASHES = ("sha256",)

    def __init__(self, config: dict) -> None:
        """
        Construct SourceVirusExchange object.

        Add the api key to the session headers.
        """
        super().__init__(config)
        self._session.headers.update({"Authorization": f"Bearer {self._config['api_key']}"})

    def download_file(self, sample_hash: str, output_path: Path) -> bool:
        """Download a file from VirusExchange."""
        response = self._get(f"{self.URL_API}/{sample_hash}")
        if response is None or not response.ok:
            return False

        download_link = response.json()["download_link"]
        self._download_without_auth(download_link, output_path)
        return True

    def _download_without_auth(self, url: str, output_path: Path) -> None:
        """Download the contents of a url without any authentication."""
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with output_path.open("wb") as h_file:
                for chunk in response.iter_content(chunk_size=8192):
                    h_file.write(chunk)

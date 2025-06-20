from pathlib import Path

from sample_finder.sources.source import Source


class SourceMWDB(Source):
    """
    Implements the MWDB Source.

    References
    ----------
        * https://mwdb.cert.pl/docs

    """

    NAME = "mwdb"
    URL_API = "https://mwdb.cert.pl/api"
    URL_FILE = f"{URL_API}/file"
    SUPPORTED_HASHES = ("md5", "sha1", "sha256", "sha512")

    def __init__(self, config: dict) -> None:
        """Construct SourceMWDB object."""
        super().__init__(config)
        self._session.headers.update({"Authorization": f"Bearer {self._config['api_key']}"})

    def download_file(self, sample_hash: str, output_path: Path) -> bool:
        """Download file from MWDB."""
        response = self._get(url=f"{self.URL_FILE}/{sample_hash}/download")
        if response is None or not response.ok:
            return False

        with output_path.open("wb") as h_file:
            h_file.write(response.content)

        return True

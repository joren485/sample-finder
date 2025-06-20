from pathlib import Path

from loguru import logger

from sample_finder.sources.source import Source


class SourceVirustotal(Source):
    """
    Implements VirusTotal Source.

    As downloading files from VirusTotal requires a premium account,
    we currently only support checking if the file exists.

    References
    ----------
        * https://docs.virustotal.com/

    """

    NAME = "virustotal"
    URL_API = "https://www.virustotal.com/api/v3"
    URL_WEBAPP = "https://www.virustotal.com/gui/file"
    SUPPORTED_HASHES = ("md5", "sha1", "sha256")

    def __init__(self, config: dict) -> None:
        """
        Construct a SourceVirustotal object.

        Set the api key in the session headers.
        """
        super().__init__(config)
        self._session.headers.update({"x-apikey": self._config["api_key"]})

    def download_file(self, sample_hash: str, output_path: Path) -> bool:
        """
        Check if a file exists on VirusTotal.

        Implements https://docs.virustotal.com/reference/file-info

        As downloading files from VirusTotal requires a premium account,
        we currently only support checking if the file exists.
        """
        response = self._get(f"{self.URL_API}/files/{sample_hash}")
        if not response or not response.ok:
            return False

        logger.success(f"Available on VirusTotal: {self.URL_WEBAPP}/{sample_hash}")

        return False

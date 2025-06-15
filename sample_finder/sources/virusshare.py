from pathlib import Path

from loguru import logger

from sample_finder.sources.source import Source


class SourceVirusshare(Source):
    """
    Implements VirusShare Source.

    References
    ----------
        * https://virusshare.com/apiv2_reference

    """

    NAME = "virusshare"
    URL_API = "https://virusshare.com/apiv2"

    def download_file(self, sample_hash: str, output_path: Path) -> bool:
        """
        Download a file from VirusShare.

        If status code 204 is returned, we are rate limited.

        The sample is zip compressed and encrypted.
        """
        response = self._get(
            f"{self.URL_API}/download", params={"apikey": self._config["api_key"], "hash": sample_hash}
        )
        if response is None or response.status_code != 200:
            if response and response.status_code == 204:
                logger.warning("Rate limited")
            return False

        try:
            data = self._decrypt_zip(response.content)
            with output_path.open("wb") as h_file:
                h_file.write(data)
        except ValueError as e:
            logger.warning(f"Failed to decrypt ZIP file: {e}")
            return False
        else:
            return True

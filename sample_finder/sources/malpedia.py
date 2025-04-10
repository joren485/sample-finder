import base64
from pathlib import Path

from sample_finder.sources.source import Source


class SourceMalpedia(Source):
    """
    Implements Malpedia Source.

    References
    ----------
        * https://malpedia.caad.fkie.fraunhofer.de/usage/api

    """

    NAME = "malpedia"
    URL_API = "https://malpedia.caad.fkie.fraunhofer.de/api"

    SUPPORTED_HASHES = ("md5", "sha256")

    def __init__(self, config: dict) -> None:
        """
        Construct SourceMalpedia object.

        Add the api key to the session headers.
        """
        super().__init__(config)
        self._session.headers.update({"Authorization": f"apitoken {self._config['api_key']}"})

    def download_file(self, sample_hash: str, output_path: Path) -> bool:
        """Download a file from Malpedia."""
        response = self._get(f"{self.URL_API}/get/sample/{sample_hash}/raw")
        if not response or not response.ok:
            return False

        response_json = response.json()

        for key in ("unpacked", "packed"):
            if key in response_json:
                data = base64.b64decode(response_json[key])
                with output_path.open("wb") as h_file:
                    h_file.write(data)
                return True

        return False

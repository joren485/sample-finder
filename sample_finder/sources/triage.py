from pathlib import Path

from loguru import logger

from sample_finder.sources.source import Source
from sample_finder.validators import validate_content_hash


class SourceTriage(Source):
    """
    Implements Triage Source.

    References
    ----------
        * https://tria.ge/docs/

    """

    NAME = "triage"
    URL_API = "https://tria.ge/api/v0"
    SUPPORTED_HASHES = ("md5", "sha1", "sha256", "sha512")

    def __init__(self, config: dict[str, str]) -> None:
        """
        Construct SourceTriage object.

        Add the api key to the session headers.
        """
        super().__init__(config)
        self._session.headers.update({"Authorization": f"Bearer {self._config['api_key']}"})

    def download_file(self, sample_hash: str, output_path: Path) -> bool:
        """Download a file from Triage."""
        response = self._get(f"{self.URL_API}/search", params={"query": self._generate_hash_query(sample_hash)})
        if response is None or not response.ok:
            return False

        data = response.json()["data"]
        if len(data) == 0:
            return False

        for sample in data:
            sample_id = sample["id"]
            response = self._get(f"{self.URL_API}/samples/{sample_id}/sample")
            if response is None or not response.ok:
                continue

            if not validate_content_hash(sample_hash=sample_hash, data=response.content):
                logger.debug("Found sample with invalid hash")
                continue

            with output_path.open("wb") as h_file:
                h_file.write(response.content)

            return True

        return False

    @staticmethod
    def _generate_hash_query(sample_hash: str) -> str:
        """Prefix a hash with its type."""
        match len(sample_hash):
            case 32:
                return f"md5:{sample_hash}"

            case 40:
                return f"sha1:{sample_hash}"

            case 64:
                return f"sha256:{sample_hash}"

            case 128:
                return f"sha512:{sample_hash}"

            case _:
                raise ValueError(f"Unknown hash: {sample_hash}")

from pathlib import Path

from sample_finder.sources.source import Source


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

    def __init__(self, config: dict) -> None:
        """
        Construct SourceTriage object.

        Add the api key to the session headers.
        """
        super().__init__(config)
        self._session.headers.update({"Authorization": f"Bearer {self._config['api_key']}"})

    def download_file(self, sample_hash: str, output_path: Path) -> bool:
        """Download a file from Triage."""
        sample_hash = self._get_hash_prefix(sample_hash)

        response = self._get(f"{self.URL_API}/search", params={"query": sample_hash})
        if response is None or not response.ok:
            return False

        data = response.json()["data"]
        if len(data) == 0:
            return False

        sample_id = data[0]["id"]
        response = self._get(f"{self.URL_API}/samples/{sample_id}/sample")
        if response is None or not response.ok:
            return False

        with output_path.open("wb") as h_file:
            h_file.write(response.content)

        return True

    @staticmethod
    def _get_hash_prefix(sample_hash: str) -> str:
        """Prefix a hash with its type."""
        if len(sample_hash) == 32:
            return f"md5:{sample_hash}"

        if len(sample_hash) == 40:
            return f"sha1:{sample_hash}"

        if len(sample_hash) == 64:
            return f"sha256:{sample_hash}"

        if len(sample_hash) == 128:
            return f"sha512:{sample_hash}"

        raise ValueError(f"Unknown hash: {sample_hash}")

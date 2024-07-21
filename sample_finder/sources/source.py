import io
from collections.abc import Iterable
from pathlib import Path
from typing import Literal, Self

import pyzipper  # type: ignore[import]
import requests
from loguru import logger

from sample_finder.validators import verify_md5, verify_sha1, verify_sha256


class Source:
    """Abstract class for Source."""

    NAME: str | None = None
    SUPPORTED_HASHES: Iterable[Literal["md5", "sha1", "sha256"]] = ("md5", "sha1", "sha256")

    def __init__(self, config: dict) -> None:
        """Construct a source."""
        self._session = requests.Session()
        self._config = config

    @classmethod
    def supported_hash(cls, h: str) -> bool:
        """Check if the hash matches one of the supported hashes."""
        return (
            ("md5" in cls.SUPPORTED_HASHES and verify_md5(h))
            or ("sha1" in cls.SUPPORTED_HASHES and verify_sha1(h))
            or ("sha256" in cls.SUPPORTED_HASHES and verify_sha256(h))
        )

    def download_file(self, sample_hash: str, output_path: Path) -> bool:
        """
        Download a sample from a source.

        This should be implemented by each source.
        """
        raise NotImplementedError

    def _get(self, url: str, params: dict | None = None) -> requests.Response | None:
        try:
            response = self._session.get(url, params=params)
        except requests.RequestException as e:
            logger.warning(f"Exception: {e}")
            return None

        self._log_response(response)

        return response

    def _post(self, url: str, data: dict | None = None) -> requests.Response | None:
        try:
            response = self._session.post(url, data=data)
        except requests.RequestException as e:
            logger.warning(f"Exception: {e}")
            return None

        self._log_response(response)

        return response

    @staticmethod
    def _log_response(response: requests.Response) -> None:
        data = response.text[:100]
        if len(response.text) >= 100:
            data += "..."

        logger.debug(f"Got response: {data!r}")

    @classmethod
    def get_source(cls, name: str, config: dict) -> Self:
        """Get source instance from a name and config dict."""
        for source in cls.__subclasses__():
            if name == source.NAME:
                return source(config)
        raise ValueError(f"Invalid source: '{name}'.")

    @staticmethod
    def _decrypt_zip(data: bytes, password: bytes = b"infected") -> bytes:
        zip_data = io.BytesIO(data)
        with pyzipper.AESZipFile(zip_data, encryption=pyzipper.WZ_AES) as h_zip:
            h_zip.setpassword(password)
            return h_zip.read(h_zip.filelist[0])

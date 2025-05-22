import pytest

from sample_finder.validators import verify_md5, verify_sha1, verify_sha256


class TestValidators:
    @pytest.mark.parametrize(("value", "result"), [("a" * 32, True), ("a" * 10, False)])
    def test_verify_md5(self, value: str, result: bool):
        assert verify_md5(value) is result

    @pytest.mark.parametrize(("value", "result"), [("a" * 40, True), ("a" * 10, False)])
    def test_verify_sha1(self, value: str, result: bool):
        assert verify_sha1(value) is result

    @pytest.mark.parametrize(("value", "result"), [("a" * 64, True), ("a" * 10, False)])
    def test_verify_sha256(self, value: str, result: bool):
        assert verify_sha256(value) is result

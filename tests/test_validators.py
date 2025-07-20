import pytest

from sample_finder.validators import validate_content_hash, verify_md5, verify_sha1, verify_sha256


class TestValidators:
    @pytest.mark.parametrize(("value", "result"), [("a" * 32, True), ("a" * 10, False)])
    def test_verify_md5(self, value: str, result: bool) -> None:
        assert verify_md5(value) is result

    @pytest.mark.parametrize(("value", "result"), [("a" * 40, True), ("a" * 10, False)])
    def test_verify_sha1(self, value: str, result: bool) -> None:
        assert verify_sha1(value) is result

    @pytest.mark.parametrize(("value", "result"), [("a" * 64, True), ("a" * 10, False)])
    def test_verify_sha256(self, value: str, result: bool) -> None:
        assert verify_sha256(value) is result

    def test_verify_hashes(self) -> None:
        with pytest.raises(ValueError, match="Unknown hash: a"):
            validate_content_hash(sample_hash="a", data=b"\x00")

        assert validate_content_hash(sample_hash="93b885adfe0da089cdf634904fd59f71", data=b"\x00")
        assert validate_content_hash(sample_hash="5ba93c9db0cff93f52b521d7420e43f6eda2784f", data=b"\x00")
        assert validate_content_hash(
            sample_hash="fff9292b4201617bdc4d3053fce02734166a683d7d858a7f5f59b073", data=b"\x00"
        )
        assert validate_content_hash(
            sample_hash="6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d", data=b"\x00"
        )
        assert validate_content_hash(
            sample_hash="bec021b4f368e3069134e012c2b4307083d3a9bdd206e24e5f0d86e13d6636655933ec2b413465966817a9c208a11717",
            data=b"\x00",
        )
        assert validate_content_hash(
            sample_hash="b8244d028981d693af7b456af8efa4cad63d282e19ff14942c246e50d9351d22704a802a71c3580b6370de4ceb293c324a8423342557d4e5c38438f0e36910ee",
            data=b"\x00",
        )

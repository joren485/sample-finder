import string


def _verify_hash(sample_hash: str, valid_length: int) -> bool:
    """Validate a string contains only hexadecimal characters and is of a specified length."""
    return len(sample_hash) == valid_length and all(c in string.hexdigits for c in sample_hash)


def verify_md5(sample_hash: str) -> bool:
    """Validate a string is a valid MD5 hash."""
    return _verify_hash(sample_hash, 32)


def verify_sha1(sample_hash: str) -> bool:
    """Validate a string is a valid SHA-1 hash."""
    return _verify_hash(sample_hash, 40)


def verify_sha224(sample_hash: str) -> bool:
    """Validate a string is a valid SHA-224 hash."""
    return _verify_hash(sample_hash, 56)


def verify_sha256(sample_hash: str) -> bool:
    """Validate a string is a valid SHA-256 hash."""
    return _verify_hash(sample_hash, 64)


def verify_sha384(sample_hash: str) -> bool:
    """Validate a string is a valid SHA-384 hash."""
    return _verify_hash(sample_hash, 96)


def verify_sha512(sample_hash: str) -> bool:
    """Validate a string is a valid SHA-512 hash."""
    return _verify_hash(sample_hash, 128)

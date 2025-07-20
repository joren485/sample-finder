import string

from Crypto.Hash import MD5, SHA1, SHA224, SHA256, SHA384, SHA512


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


def validate_content_hash(sample_hash: str, data: bytes) -> bool:
    """
    Validate sample data matches a given hash.

    This function assumes the sample hash is lowercase.
    """
    match len(sample_hash):
        case 32:
            return MD5.new(data=data).hexdigest() == sample_hash

        case 40:
            return SHA1.new(data=data).hexdigest() == sample_hash

        case 56:
            return SHA224.new(data=data).hexdigest() == sample_hash

        case 64:
            return SHA256.new(data=data).hexdigest() == sample_hash

        case 96:
            return SHA384.new(data=data).hexdigest() == sample_hash

        case 128:
            return SHA512.new(data=data).hexdigest() == sample_hash

        case _:
            raise ValueError(f"Unknown hash: {sample_hash}")

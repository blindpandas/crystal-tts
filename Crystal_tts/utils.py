# coding: utf-8


import hashlib
import re
import typing
import unicodedata
import numpy as np


def audio_float_to_int16(
    audio: np.ndarray, max_wav_value: float = 32767.0
) -> np.ndarray:
    """Normalize audio and convert to int16 range"""
    audio_norm = audio * (max_wav_value / max(0.01, np.max(np.abs(audio))))
    audio_norm = np.clip(audio_norm, -max_wav_value, max_wav_value)
    audio_norm = audio_norm.astype("int16")
    return audio_norm


def wildcard_to_regex(template: str, wildcard: str = "*") -> re.Pattern:
    """Convert a string with wildcards into a regex pattern"""
    wildcard_escaped = re.escape(wildcard)

    pattern_parts = ["^"]
    for i, template_part in enumerate(re.split(f"({wildcard_escaped})", template)):
        if (i % 2) == 0:
            # Fixed string
            pattern_parts.append(re.escape(template_part))
        else:
            # Wildcard separator
            pattern_parts.append(".*")

    pattern_parts.append("$")
    pattern_str = "".join(pattern_parts)

    return re.compile(pattern_str)


def file_sha256_sum(fp: typing.BinaryIO, block_bytes: int = 4096) -> str:
    """Return the sha256 sum of a (possibly large) file"""
    current_hash = hashlib.sha256()

    # Read in blocks in case file is very large
    block = fp.read(block_bytes)
    while len(block) > 0:
        current_hash.update(block)
        block = fp.read(block_bytes)

    return current_hash.hexdigest()


def to_codepoints(s: str) -> typing.List[str]:
    """Split string into a list of codepoints"""
    return list(unicodedata.normalize("NFC", s))

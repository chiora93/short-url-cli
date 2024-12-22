import random
import string
from urllib.parse import urlparse

import settings


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def shorten_url(url: str) -> str:
    # Step 1: Create a simple hash by summing the ASCII values of each character
    # and applying a modulo operation to keep the number within a certain range.
    mod_value = 999983  # A large prime number to better distribute hash values
    hash_val = 0
    for ch in url:
        hash_val = (hash_val * 31 + ord(ch)) % mod_value

    # Step 2: Convert this numeric value into a "base 62" format to get a compact string.
    # We use [0-9, a-z, A-Z] as the character set.
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    short_code = ""

    # Handle the case where hash_val is 0
    if hash_val == 0:
        short_code = chars[0]
    else:
        while hash_val > 0:
            remainder = hash_val % 62
            short_code = chars[remainder] + short_code
            hash_val //= 62

    # Step 3: Add randomness to shorted URL
    for i in range(1, 4):
        short_code = short_code + random.choice(string.ascii_letters)

    # Step 4: Prepend a prefix to form a complete shortened URL
    short_url = settings.SHORTENED_URL_BASE_URL + short_code
    return short_url

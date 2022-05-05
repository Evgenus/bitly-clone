from django.conf import settings

from random import choice

from string import (
    ascii_letters,
    digits,
)

SIZE = getattr(settings, "MAXIMUM_URL_CHARS", 7)
AVAILABLE_CHARS = ascii_letters + digits


def create_random_code(chars=AVAILABLE_CHARS, size=SIZE):
    """
    Creates a random string with the predetermined size
    """
    return "".join(
        [choice(chars) for _ in range(size)]
    )

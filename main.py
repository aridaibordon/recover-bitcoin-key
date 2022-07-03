from dotenv import load_dotenv

load_dotenv()

import os
from scripts.utils import get_WIF_from_hex, get_public_address_from_private_key

PUBLIC_ADDRESS = os.environ["PUBLIC_ADDRESS"]
PARTIAL_PRIVATE_KEY = os.environ["PARTIAL_PRIVATE_KEY"]


def try_new_key() -> str:
    """
    Generator of all possible private keys from a partial private key.

    """
    unknown_chars = PARTIAL_PRIVATE_KEY.count("X")

    number = 0

    while True:
        new_key = PARTIAL_PRIVATE_KEY
        number += 1
        hex_number = hex(number)[2:].zfill(unknown_chars)

        for i in range(unknown_chars):
            new_key = new_key.replace("X", hex_number[i], 1)

        yield get_WIF_from_hex(new_key)


def main() -> None:
    for private_key in try_new_key():
        public_address = get_public_address_from_private_key(private_key)
        if public_address == PUBLIC_ADDRESS:
            print(f"Congratulations! Your private address is: {private_key}")


if __name__ == "__main__":
    main()
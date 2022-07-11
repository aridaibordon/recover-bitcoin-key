from tracemalloc import start
from config import config

from scripts.backup import create_backup, load_backup
from scripts.utils import get_WIF_from_hex, get_public_address_from_private_key

PUBLIC_ADDRESS = config["PUBLIC_ADDRESS"]
PARTIAL_PRIVATE_KEY = config["PARTIAL_PRIVATE_KEY"]
UNKNOWN_CHAR = config["UNKNOWN_CHAR"]

CREATE_BACKUP = config["CREATE_BACKUP"]
PERIOD_BACKUP = config["PERIOD_BACKUP"]


def try_new_key(start=0) -> str:
    """
    Generator of all possible private keys from a partial private key.

    """
    unknown_chars = PARTIAL_PRIVATE_KEY.count(UNKNOWN_CHAR)
    possible_comb = 16**unknown_chars
    number = start

    while number < possible_comb:
        new_key = PARTIAL_PRIVATE_KEY
        hex_number = hex(number)[2:].zfill(unknown_chars)

        for i in range(unknown_chars):
            new_key = new_key.replace(UNKNOWN_CHAR, hex_number[i], 1)

        if CREATE_BACKUP and number % PERIOD_BACKUP == 0:
            create_backup(hex_number)

        number += 1
        yield get_WIF_from_hex(new_key)


def main() -> None:
    for private_key in try_new_key(start=load_backup()):
        public_address = get_public_address_from_private_key(private_key)
        if public_address == PUBLIC_ADDRESS:
            print(f"Congratulations! Your private address is: {private_key}")


if __name__ == "__main__":
    main()
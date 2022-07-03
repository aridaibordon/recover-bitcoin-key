import codecs
import hashlib
import ecdsa
import base58

def get_WIF_from_hex(hex: str) -> str:
    """
    Transform a hex private key to WIF format
    
    Parameters
    ----------
    * hex: private key in hex format.

    """
    PK1 = '80' + hex
    PK2 = hashlib.sha256(codecs.decode(PK1, 'hex'))
    PK3 = hashlib.sha256(PK2.digest())
    checksum = codecs.encode(PK3.digest(), 'hex')[0:8]
    PK4 = PK1 + str(checksum)[2:10]

    # Define base58
    def base58(address_hex):
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        b58_string = ''
        # Get the number of leading zeros
        leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
        # Convert hex to decimal
        address_int = int(address_hex, 16)
        # Append digits to the start of string
        while address_int > 0:
            digit = address_int % 58
            digit_char = alphabet[digit]
            b58_string = digit_char + b58_string
            address_int //= 58
        # Add ‘1’ for each 2 leading zeros
        ones = leading_zeros // 2
        for one in range(ones):
            b58_string = '1' + b58_string
        return b58_string

    WIF = base58(PK4)
    return WIF


def get_public_address_from_private_key(private_key: str):
    """ Return the public address from a private key

    Parameters
    ----------
    * private_key: string with the private key.

    Original code from Shlomi Zeltsinger (https://www.youtube.com/watch?v=tX-XokHf_nI).

    ALWAYS REMEMBER TO KEEP YOUR PRIVATE KEYS SECRET. THE ACCESS OF A THIRD PARTY TO YOUR
    KEYS COULD LEAD TO THE LOSE OF ALL YOUR FUNDS.

    """
    # WIF to private key by https://en.bitcoin.it/wiki/Wallet_import_format
    private_key = base58.b58decode_check(private_key)
    private_key = private_key[1:]

    # Private key to public key (ecdsa transformation)
    signing_key = ecdsa.SigningKey.from_string(private_key,
                                               curve=ecdsa.SECP256k1)
    verifying_key = signing_key.get_verifying_key()
    public_key = bytes.fromhex("04") + verifying_key.to_string()

    # hash sha 256 of pubkey
    sha256_1 = hashlib.sha256(public_key)

    # hash ripemd of sha of pubkey
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(sha256_1.digest())

    # checksum
    hashed_public_key = bytes.fromhex("00") + ripemd160.digest()
    checksum_full = hashlib.sha256(
        hashlib.sha256(hashed_public_key).digest()).digest()
    checksum = checksum_full[:4]
    bin_addr = hashed_public_key + checksum

    # encode address to base58 and print
    public_address = base58.b58encode(bin_addr)
    return public_address.decode("utf-8")

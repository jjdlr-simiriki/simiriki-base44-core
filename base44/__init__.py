ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$%*+-./:"

def encode(data: bytes) -> str:
    """Encode bytes into a Base44 string."""
    if not data:
        return ""
    # Count leading zero bytes
    leading_zeros = 0
    for b in data:
        if b == 0:
            leading_zeros += 1
        else:
            break
    remaining = data[leading_zeros:]
    if not remaining:
        return ALPHABET[0] * leading_zeros
    num = int.from_bytes(remaining, "big")
    digits = []
    while num > 0:
        num, rem = divmod(num, 44)
        digits.append(ALPHABET[rem])
    encoded = "".join(reversed(digits))
    return ALPHABET[0] * leading_zeros + encoded


def decode(text: str) -> bytes:
    """Decode a Base44 string into bytes."""
    if not text:
        return b""
    prefix = 0
    for ch in text:
        if ch == ALPHABET[0]:
            prefix += 1
        else:
            break
    num = 0
    for ch in text[prefix:]:
        idx = ALPHABET.find(ch)
        if idx == -1:
            raise ValueError(f"Invalid character: {ch}")
        num = num * 44 + idx
    decoded = b"" if not text[prefix:] else num.to_bytes((num.bit_length() + 7) // 8, "big")
    return b"\x00" * prefix + decoded

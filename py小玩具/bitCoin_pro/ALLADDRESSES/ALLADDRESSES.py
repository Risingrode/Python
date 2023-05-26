"""

"""


from enum import Enum
from time import sleep
from hmac import new as hmac
from secrets import randbits
from audioplayer import AudioPlayer
from requests import get as get_from_api
from typing import Any, Final, Tuple, Union
from multiprocessing.pool import ThreadPool
import colorama
from multiprocessing import cpu_count, Process, Queue
from os import name as system_type, system as run_command
from hashlib import new as hash_function, pbkdf2_hmac, sha256, sha3_512


# Type Hints.
Point = Tuple[int, int]
Jacobian_Coordinate = Tuple[int, int, int]
Private_Keys = Tuple[str, str]
Public_Keys = Tuple[str, ...]
Addresses = Tuple[str, str, str, str, str]
Balances = Tuple[float, ...]
BTC_Data = Tuple[str, str, str, str, str,
                 str, str, str, str, Addresses, Balances]


# Define clear function.
def clear() -> None:
    """
    Tests the operating system type and sets the screen clear command.
    """
    # Screen clear command for Windows operating system.
    if system_type == "nt":
        _ = run_command("cls")

    # Screen clear command for macOS/Linux operating system.
    elif system_type == "posix":
        _ = run_command("clear")


# Get ANSI escapes from color scheme to work on Windows.


#       Mathematical domain parameters of the elliptic curve SECP256K1.
#       Source: https://www.secg.org/sec2-v2.pdf


# The finite field (Fp) is defined by:
FP_CURVE: Final[int] = \
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F


# The elliptic curve (y^2 = x^3 + ax + b) over Fp is defined by:
A_CURVE: Final[int] = \
    0x0000000000000000000000000000000000000000000000000000000000000000

B_CURVE: Final[int] = \
    0x0000000000000000000000000000000000000000000000000000000000000007


# The generator point is defined by:
GENERATOR_POINT_CURVE: Final[Point] = \
    (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)


# The order of generator point and the cofactor are defined by:
N_CURVE: Final[int] = \
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

H_CURVE: Final[int] = \
    0x0000000000000000000000000000000000000000000000000000000000000001


# The point that points to infinity on the elliptic curve is defined by:
POINT_INFINITY_CURVE: Final[Point] = (0, 0)


# The point that points to infinity on the elliptic curve over Jacobian
# coordinate is defined by:
POINT_INFINITY_JACOBIAN: Final[Jacobian_Coordinate] = (1, 1, 0)


def modular_inverse(k: int, p: int) -> int:
    """
    Extended Euclidean algorithm/division on the elliptic curve.

    Returns the multiplicative inverse of {k % p}. Where the only
    integer {x} is defined such that {(k * x) % p == 1}.

    {k} must be non-zero and {p} must be a prime.
    """
    if k == 0:
        raise ZeroDivisionError("Division by zero!")
    if k < 0:
        result = p - modular_inverse(- k, p)
        return result
    old_r, r = (k, p)
    old_s, s = (1, 0)
    old_t, t = (0, 1)
    while old_r != 0:
        quotient = r // old_r
        r, old_r = (old_r, r - quotient * old_r)
        s, old_s = (old_s, s - quotient * old_s)
        t, old_t = (old_t, t - quotient * old_t)
    gcd, x, y = (r, s, t)
    if k == 1:
        assert gcd == 1
        assert (k * x) % p == 1
        assert (p * y) % k == 0
    if k == p:
        assert gcd == p
        assert (k * x) % p == 0
        assert (p * y) % k == 0
    if k != 1 and k != p:
        assert gcd == 1
        assert (k * x) % p == 1
        assert (p * y) % k == 1
    result = x % p
    return result


def is_infinite(point: Point) -> bool:
    """
    Returns True if the point at infinity on the elliptic curve,
    otherwise it returns False.
    """
    result = point == POINT_INFINITY_CURVE or 0 in point
    return result


def is_on_curve(point: Point) -> bool:
    """
    Returns True if the point lies on the elliptic curve, otherwise it
    returns False.
    """
    if is_infinite(point):
        result = True
        return result
    xp, yp = point
    result = (pow(yp, 2, FP_CURVE) - pow(xp, 3, FP_CURVE) -
              A_CURVE * xp - B_CURVE) % FP_CURVE == 0
    return result


def x(point: Point) -> int:
    """
    Refers to {x} coordinate of point, assuming it is not at infinity,
    then returns {x}.
    """
    assert not is_infinite(point)
    assert is_on_curve(point)
    xp, _ = point
    result = xp
    return result


def y(point: Point) -> int:
    """
    Refers to {y} coordinate of point, assuming it is not at infinity,
    then returns {y}.
    """
    assert not is_infinite(point)
    assert is_on_curve(point)
    _, yp = point
    result = yp
    return result


def has_even_y(point: Point) -> bool:
    """
    Where point is not at infinity, it returns True if {yp mod 2 = 0},
    otherwise it returns False.
    """
    assert not is_infinite(point)
    assert is_on_curve(point)
    yp = y(point)
    result = yp % 2 == 0
    return result


def is_infinite_jacobian(jacobian: Jacobian_Coordinate) -> bool:
    """
    Returns True if the point at infinity on the elliptic curve over
    Jacobian coordinate, otherwise it returns False.
    """
    _, _, zp = jacobian
    result = jacobian == POINT_INFINITY_JACOBIAN or zp == 0
    return result


def is_on_curve_jacobian(jacobian: Jacobian_Coordinate) -> bool:
    """
    Returns True if the point lies on the elliptic curve over Jacobian
    coordinate, otherwise it returns False.
    """
    if is_infinite_jacobian(jacobian):
        result = True
        return result
    xp, yp, zp = jacobian
    zp_2 = pow(zp, 2, FP_CURVE)
    zp_4 = pow(zp, 4, FP_CURVE)
    result = (pow(yp, 2, FP_CURVE) - pow(xp, 3, FP_CURVE) -
              A_CURVE * xp * zp_4 - B_CURVE * zp_2 * zp_4) % FP_CURVE == 0
    return result


def is_affine_jacobian(jacobian: Jacobian_Coordinate) -> bool:
    """
    Returns True if the point is affine form in Jacobian coordinate
    (x, y, 1).
    """
    assert not is_infinite_jacobian(jacobian)
    assert is_on_curve_jacobian(jacobian)
    _, _, zp = jacobian
    result = zp == 1
    return result


def to_jacobian(point: Point) -> Jacobian_Coordinate:
    """
    Convert an affine point to Jacobian coordinate, or returns point at
    infinity.

    A Jacobian coordinate is represented as (x, y, z).
    """
    assert is_on_curve(point)
    if is_infinite(point):
        jacobian = POINT_INFINITY_JACOBIAN
        result = jacobian
        assert is_on_curve_jacobian(result)
        return result
    xp, yp = point
    xp, yp, zp = (xp, yp, 1)
    jacobian = (xp, yp, zp)
    result = jacobian
    assert is_on_curve_jacobian(result)
    return result


def from_jacobian(jacobian: Jacobian_Coordinate) -> Point:
    """
    Convert a Jacobian coordinate to affine point, or returns point at
    infinity.

    An affine point is represented as (x, y).
    """
    assert is_on_curve_jacobian(jacobian)
    if is_infinite_jacobian(jacobian):
        point = POINT_INFINITY_CURVE
        result = point
        assert is_on_curve(result)
        return result
    xp, yp, zp = jacobian
    if is_affine_jacobian(jacobian):
        point = (xp, yp)
        result = point
        assert is_on_curve(result)
        return result
    zp_inv = modular_inverse(zp, FP_CURVE)
    zp_inv_2 = pow(zp_inv, 2, FP_CURVE)
    zp_inv_3 = pow(zp_inv, 3, FP_CURVE)
    point = ((zp_inv_2 * xp) % FP_CURVE, (zp_inv_3 * yp) % FP_CURVE)
    result = point
    assert is_on_curve(result)
    return result


def jacobian_point_doubling(
        jacobian_p: Jacobian_Coordinate) -> Jacobian_Coordinate:
    """
    Point doubling on the elliptic curve over Jacobian coordinate
    (x, y, z).

    It doubles Point-P.
    """
    assert is_on_curve_jacobian(jacobian_p)
    if is_infinite_jacobian(jacobian_p):
        jacobian_r = POINT_INFINITY_JACOBIAN
        result = jacobian_r
        assert is_on_curve_jacobian(result)
        return result
    xp, yp, zp = jacobian_p
    xp_2 = pow(xp, 2, FP_CURVE)
    yp_2 = pow(yp, 2, FP_CURVE)
    yp_4 = pow(yp, 4, FP_CURVE)
    s = (4 * xp * yp_2) % FP_CURVE
    m = (3 * xp_2) % FP_CURVE
    if A_CURVE:
        zp_4 = pow(zp, 4, FP_CURVE)
        m += (A_CURVE * zp_4) % FP_CURVE
    m = m % FP_CURVE
    xr = (pow(m, 2, FP_CURVE) - 2 * s) % FP_CURVE
    yr = (m * (s - xr) - 8 * yp_4) % FP_CURVE
    zr = (2 * yp * zp) % FP_CURVE
    jacobian_r = (xr, yr, zr)
    result = jacobian_r
    assert is_on_curve_jacobian(result)
    return result


def jacobian_point_addition_mixed(
        jacobian_p: Jacobian_Coordinate,
        jacobian_q: Jacobian_Coordinate) -> Jacobian_Coordinate:
    """
    Point addition (mixed) on the elliptic curve over Jacobian
    coordinate (x, y, z) and affine form in Jacobian coordinate
    (x, y, 1).

    It adds Point-P with Point-Q.
    """
    assert is_on_curve_jacobian(jacobian_p)
    assert is_on_curve_jacobian(jacobian_q)
    assert is_affine_jacobian(jacobian_q)
    if is_infinite_jacobian(jacobian_p):
        jacobian_r = jacobian_q
        result = jacobian_r
        return result
    xp, yp, zp = jacobian_p
    xq, yq, _ = jacobian_q
    zp_2 = pow(zp, 2, FP_CURVE)
    zp_3 = pow(zp, 3, FP_CURVE)
    uq = (xq * zp_2) % FP_CURVE
    sq = (yq * zp_3) % FP_CURVE
    if xp == uq and yp != sq:
        jacobian_r = POINT_INFINITY_JACOBIAN
        result = jacobian_r
        assert is_on_curve_jacobian(result)
        return result
    if xp == uq and yp == sq:
        jacobian_r = jacobian_point_doubling(jacobian_p)
        result = jacobian_r
        return result
    h = (uq - xp) % FP_CURVE
    r = (sq - yp) % FP_CURVE
    h_2 = pow(h, 2, FP_CURVE)
    h_3 = pow(h, 3, FP_CURVE)
    xp_h_2 = (xp * h_2) % FP_CURVE
    xr = (pow(r, 2, FP_CURVE) - h_3 - 2 * xp_h_2) % FP_CURVE
    yr = (r * (xp_h_2 - xr) - yp * h_3) % FP_CURVE
    zr = (h * zp) % FP_CURVE
    jacobian_r = (xr, yr, zr)
    result = jacobian_r
    assert is_on_curve_jacobian(result)
    return result


def jacobian_point_addition(
        jacobian_p: Jacobian_Coordinate,
        jacobian_q: Jacobian_Coordinate) -> Jacobian_Coordinate:
    """
    Point addition on the elliptic curve over Jacobian coordinate
    (x, y, z).

    It adds Point-P with Point-Q.
    """
    assert is_on_curve_jacobian(jacobian_p)
    assert is_on_curve_jacobian(jacobian_q)
    if is_infinite_jacobian(jacobian_p):
        jacobian_r = jacobian_q
        result = jacobian_r
        return result
    if is_infinite_jacobian(jacobian_q):
        jacobian_r = jacobian_p
        result = jacobian_r
        return result
    if is_affine_jacobian(jacobian_p):
        jacobian_r = jacobian_point_addition_mixed(jacobian_q, jacobian_p)
        result = jacobian_r
        return result
    if is_affine_jacobian(jacobian_q):
        jacobian_r = jacobian_point_addition_mixed(jacobian_p, jacobian_q)
        result = jacobian_r
        return result
    xp, yp, zp = jacobian_p
    xq, yq, zq = jacobian_q
    zp_2 = pow(zp, 2, FP_CURVE)
    zp_3 = pow(zp, 3, FP_CURVE)
    zq_2 = pow(zq, 2, FP_CURVE)
    zq_3 = pow(zq, 3, FP_CURVE)
    up = (xp * zq_2) % FP_CURVE
    uq = (xq * zp_2) % FP_CURVE
    sp = (yp * zq_3) % FP_CURVE
    sq = (yq * zp_3) % FP_CURVE
    if up == uq and sp != sq:
        jacobian_r = POINT_INFINITY_JACOBIAN
        result = jacobian_r
        assert is_on_curve_jacobian(result)
        return result
    if up == uq and sp == sq:
        jacobian_r = jacobian_point_doubling(jacobian_p)
        result = jacobian_r
        return result
    h = (uq - up) % FP_CURVE
    r = (sq - sp) % FP_CURVE
    h_2 = pow(h, 2, FP_CURVE)
    h_3 = pow(h, 3, FP_CURVE)
    up_h_2 = (up * h_2) % FP_CURVE
    xr = (pow(r, 2, FP_CURVE) - h_3 - 2 * up_h_2) % FP_CURVE
    yr = (r * (up_h_2 - xr) - sp * h_3) % FP_CURVE
    zr = (h * zp * zq) % FP_CURVE
    jacobian_r = (xr, yr, zr)
    result = jacobian_r
    assert is_on_curve_jacobian(result)
    return result


def fast_point_addition(point_p: Point, point_q: Point) -> Point:
    """
    Fast point addition on the elliptic curve over affine (x, y) to
    Jacobian coordinate (x, y, z).

    It adds Point-P with Point-Q.
    """
    assert is_on_curve(point_p)
    assert is_on_curve(point_q)
    if is_infinite(point_p):
        point_r = point_q
        result = point_r
        return result
    if is_infinite(point_q):
        point_r = point_p
        result = point_r
        return result
    jacobian_p = to_jacobian(point_p)
    jacobian_q = to_jacobian(point_q)
    jacobian_r = jacobian_point_addition_mixed(jacobian_p, jacobian_q)
    point_r = from_jacobian(jacobian_r)
    result = point_r
    assert is_on_curve(result)
    return result


def fast_scalar_multiplication(scalar: int, point: Point) -> Point:
    """
    Fast scalar multiplication of point on the elliptic curve over
    affine (x, y) to Jacobian coordinate (x, y, z).

    It doubles Point-P and adds Point-P with Point-Q.
    """
    assert is_on_curve(point)
    if scalar == 0 or is_infinite(point):
        new_point = POINT_INFINITY_CURVE
        result = new_point
        assert is_on_curve(result)
        return result
    if scalar == 1:
        result = point
        return result
    if scalar < 0 or scalar >= N_CURVE:
        new_point = fast_scalar_multiplication(scalar % N_CURVE, point)
        result = new_point
        return result
    scalar_binary = bin(scalar)[2:]
    jacobian = to_jacobian(point)
    current = jacobian
    for i in range(1, len(scalar_binary)):
        current = jacobian_point_doubling(current)
        if scalar_binary[i] == "1":
            current = jacobian_point_addition(jacobian, current)
    new_point = from_jacobian(current)
    result = new_point
    assert is_on_curve(result)
    return result


def int_from_hex(hex: str) -> int:
    """Converts a hexadecimal string to integer."""
    result = int("0x" + hex, 16)
    return result


def int_from_bytes(bytes: bytes) -> int:
    """Converts the bytes to integer."""
    result = int.from_bytes(bytes, byteorder="big")
    return result


def hex_from_int(x: int, output_length_bytes: int) -> str:
    """Converts an integer to hexadecimal string."""
    result = hex(x)[2:].zfill(output_length_bytes * 2)
    return result


def bytes_from_int(x: int) -> bytes:
    """Converts an integer to bytes."""
    result = x.to_bytes(32, byteorder="big")
    return result


def bytes_from_hex(hex: str) -> bytes:
    """Converts a hexadecimal string to bytes."""
    result = bytes.fromhex(hex)
    return result


def lift_x(xp: int) -> Point:
    """
    Return the unique point such that:

    {x(point) = x}

    and

    {y(point) = y} if {y % 2 = 0} or {y(point) = Fp - y} otherwise.
    """
    if not 0 < xp < FP_CURVE:
        result = POINT_INFINITY_CURVE
        return result
    y_sq = (pow(xp, 3, FP_CURVE) + 7) % FP_CURVE
    yp = pow(y_sq, (FP_CURVE + 1) // 4, FP_CURVE)
    if pow(yp, 2, FP_CURVE) != y_sq:
        result = POINT_INFINITY_CURVE
        return result
    point = (xp, yp)
    result = (x(point), y(point) if has_even_y(point) else FP_CURVE - y(point))
    return result


def tagged_hash(tag: str, message: str) -> bytes:
    """
    Where tag is a UTF-8 encoded tag name and message is an array of
    bytes in hexadecimal string, returning the 32-byte hash.
    """
    data = bytes_from_hex(message)
    tag_hash = sha256(tag.encode()).digest()
    result = sha256(tag_hash + tag_hash + data).digest()
    return result


def taproot_tweak_public_key(internal_public_key: str) -> str:
    """
    Internal public key tweaking procedure, returning the output public
    key.
    """
    t = int_from_bytes(tagged_hash("TapTweak", internal_public_key))
    if not 0 < t < N_CURVE:
        result = False
        return result  # type: ignore
    p = fast_scalar_multiplication(t, GENERATOR_POINT_CURVE)
    q = lift_x(int_from_hex(internal_public_key))
    tweaked_output_public_key = fast_point_addition(p, q)
    result = hex_from_int(x(tweaked_output_public_key), 32)  # type: ignore
    return result  # type: ignore


# Alphabet used for Base58 encoding.
BASE58_CHARSET: Final[str] = \
    "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def base58_from_hex(data: str) -> str:
    """Encoder from hexadecimal string to Base58."""
    count = 0
    val = 0
    for char in data:
        if char != "0":
            break
        count += 1
    count = count // 2
    n = int_from_hex(data)
    output = []
    while n > 0:
        n, remainder = divmod(n, 58)
        output.append(BASE58_CHARSET[remainder])
    while val < count:
        output.append(BASE58_CHARSET[0])
        val += 1
    result = "".join(output[::-1])
    return result


# Alphabet used for Bech32/Bech32m encoding.
BECH32_CHARSET: Final[str] = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"

# Constant required for Bech32 encoding.
BECH32_CONST: Final[int] = 1

# Constant required for Bech32m encoding.
BECH32M_CONST: Final[int] = 0x2bc830a3


class Encoding(Enum):
    """Enumeration type to list the various supported encodings."""
    BECH32 = 1
    BECH32M = 2


def bech32_polymod(values: list) -> int:
    """Internal function that computes the Bech32 checksum."""
    generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for value in values:
        top = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ value
        for i in range(5):
            chk ^= generator[i] if ((top >> i) & 1) else 0
    result = chk
    return result


def bech32_hrp_expand(hrp: str) -> list:
    """Expand the HRP into values for checksum computation."""
    result = [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]
    return result


def bech32_verify_checksum(hrp: str, data: list) -> object:
    """Verify a checksum given HRP and converted data characters."""
    check = bech32_polymod(bech32_hrp_expand(hrp) + data)
    if check == BECH32_CONST:
        result = Encoding.BECH32
        return result
    elif check == BECH32M_CONST:
        result = Encoding.BECH32M
        return result
    else:
        result = None  # type: ignore
        return result


def bech32_create_checksum(encoding: object, hrp: str, data: list) -> list:
    """Compute the checksum values given HRP and data."""
    values = bech32_hrp_expand(hrp) + data
    const = BECH32M_CONST if encoding == Encoding.BECH32M else BECH32_CONST
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ const
    result = [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]
    return result


def bech32_encode(encoding: object, hrp: str, data: list) -> str:
    """Compute a Bech32 or Bech32m string given HRP and data values."""
    combined = data + bech32_create_checksum(encoding, hrp, data)
    result = hrp + "1" + "".join([BECH32_CHARSET[d] for d in combined])
    return result


def bech32_decode(bech: str) -> tuple:
    """Validate a Bech32/Bech32m string, and determine HRP and data."""
    if ((any(ord(x) < 33 or ord(x) > 126 for x in bech)) or
            (bech.lower() != bech and bech.upper() != bech)):
        result = (None, None, None)
        return result
    bech = bech.lower()
    pos = bech.rfind("1")
    if pos < 1 or pos + 7 > len(bech) or len(bech) > 90:
        result = (None, None, None)
        return result
    if not all(x in BECH32_CHARSET for x in bech[pos + 1:]):
        result = (None, None, None)
        return result
    hrp = bech[:pos]
    data = [BECH32_CHARSET.find(x) for x in bech[pos + 1:]]
    encoding = bech32_verify_checksum(hrp, data)
    if encoding is None:
        result = (None, None, None)
        return result
    result = (encoding, hrp, data[:-6])  # type: ignore
    return result


def convertbits(data: Union[bytes, list], frombits: int, tobits: int,
                pad: bool = True) -> list:
    """General power-of-2 base conversion."""
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            result = None
            return result  # type: ignore
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        result = None
        return result  # type: ignore
    result = ret
    return result


def decode_segwit_address(hrp: str, addr: str) -> tuple:
    """Decode a segwit address."""
    encoding, hrpgot, data = bech32_decode(addr)
    if hrpgot != hrp:
        result = (None, None)
        return result
    decoded = convertbits(data[1:], 5, 8, False)
    if decoded is None or len(decoded) < 2 or len(decoded) > 40:
        result = (None, None)
        return result
    if data[0] > 16:
        result = (None, None)
        return result
    if data[0] == 0 and len(decoded) != 20 and len(decoded) != 32:
        result = (None, None)
        return result
    if (data[0] == 0 and encoding != Encoding.BECH32) or \
            (data[0] != 0 and encoding != Encoding.BECH32M):
        result = (None, None)
        return result
    result = (data[0], decoded)  # type: ignore
    return result


def encode_segwit_address(hrp: str, witver: int, witprog: bytes) -> str:
    """Encode a segwit address."""
    encoding = Encoding.BECH32 if witver == 0 else Encoding.BECH32M
    ret = bech32_encode(encoding, hrp, [witver] + convertbits(witprog, 8, 5))
    if decode_segwit_address(hrp, ret) == (None, None):
        result = None
        return result  # type: ignore
    result = ret
    return result


def hasher_pbkdf2_hmac(data: bytes, salt: bytes) -> bytes:
    """Get hash through PBKDF2 with HMAC_SHA3-512."""
    result = pbkdf2_hmac("sha3-512", data, salt, 2048, 64)
    return result


def hasher_hmac(data: bytes, salt: bytes) -> str:
    """Get hash through HMAC_SHA3-512."""
    result = hmac(salt, data, sha3_512).hexdigest()
    return result


def hasher_ripemd160(data: bytes) -> str:
    """Get hash through RIPEMD-160."""
    hash_obj = hash_function("ripemd160")
    hash_obj.update(data)
    result = hash_obj.hexdigest()
    return result


def hasher_single_sha256(data: str) -> bytes:
    """Get single hash through SHA-256."""
    data_bytes = bytes_from_hex(data)
    result = sha256(data_bytes).digest()
    return result


def hasher_double_sha256(data: str) -> str:
    """Get double hash through SHA-256."""
    data_bytes = bytes_from_hex(data)
    result = sha256(sha256(data_bytes).digest()).hexdigest()
    return result


def generate_private_key() -> str:
    """Secure generator of private key at 256-bit length."""
    while True:
        entropy_data = bytes_from_hex(hex_from_int(randbits(1536), 192))
        entropy_salt = bytes_from_hex(hex_from_int(randbits(128), 16))
        password = "Hattoshi Hanzōmoto - The Bitcoin master seed."
        entropy_salt = password.encode("utf-8") + entropy_salt
        master_seed = hasher_pbkdf2_hmac(entropy_data, entropy_salt)
        entropy_salt = bytes_from_hex(hex_from_int(randbits(128), 16))
        password = "Hattoshi Hanzōmoto - The Bitcoin master node."
        entropy_salt = password.encode("utf-8") + entropy_salt
        master_node = hasher_hmac(master_seed, entropy_salt)
        master_private_key = bytes_from_hex("00" + master_node[0:64])
        master_chain_code = bytes_from_hex(master_node[64:])
        index = bytes_from_int(pow(2, 31) + 263)
        hmac_master_pkix_cc = hasher_hmac(master_private_key + index,
                                          master_chain_code)
        scalar_add_mod = (int_from_hex(master_node[0:64]) +
                          int_from_hex(hmac_master_pkix_cc[0:64])) % N_CURVE
        result = hex_from_int(scalar_add_mod, 32)
        if not 0 < int_from_hex(result) < N_CURVE:
            continue
        break
    return result


def private_key_to_wif(private_key: str) -> Private_Keys:
    """
    Private key encoder to uncompressed and compressed WIF
    (Wallet Import Format), coded to main network.
    """
    version_byte = "80"
    compression_byte = ("", "01")
    extended = version_byte + private_key + compression_byte[0]
    checksum = hasher_double_sha256(extended)[0:8]
    private_key_wif_uncompressed = base58_from_hex(extended + checksum)
    extended = version_byte + private_key + compression_byte[1]
    checksum = hasher_double_sha256(extended)[0:8]
    private_key_wif_compressed = base58_from_hex(extended + checksum)
    result = (private_key_wif_uncompressed, private_key_wif_compressed)
    return result


def get_public_key_from_private_key(private_key: str) -> Public_Keys:
    """
    Gets the public key by multiplying (scalar multiplication on the
    elliptic curve) the private key with the generator point, thus
    returning uncompressed and compressed format of public key.
    """
    public_key = fast_scalar_multiplication(int_from_hex(private_key),
                                            GENERATOR_POINT_CURVE)
    public_key_uncompressed = "04" + \
        hex_from_int(x(public_key), 32) + hex_from_int(y(public_key), 32)
    if has_even_y(public_key):
        public_key_compressed = "02" + hex_from_int(x(public_key), 32)
    else:
        public_key_compressed = "03" + hex_from_int(x(public_key), 32)
    result = (public_key_uncompressed, public_key_compressed)
    return result


def public_key_to_address(public_keys: Public_Keys) -> Addresses:
    """
    Public keys encoder to all types of addresses, coded to main
    network.

    Public keys:
    - Tuple[public_key_uncompressed,
            public_key_compressed,
            output_public_key]

    Types of addresses:
    - P2PKH uncompressed (Pay-To-Public-Key-Hash uncompressed)
    - P2PKH compressed (Pay-To-Public-Key-Hash compressed)
    - P2SH-P2WPKH (Pay-To-Script-Hash)::(Pay-To-Witness-Public-Key-Hash)
    - P2WPKH (Pay-To-Witness-Public-Key-Hash)
    - P2TR (Pay-To-Taproot)
    """
    version_byte = "00"
    public_key_hash = hasher_ripemd160(hasher_single_sha256(public_keys[0]))
    checksum = hasher_double_sha256(version_byte + public_key_hash)[0:8]
    p2pkh_uncompressed = base58_from_hex(version_byte +
                                         public_key_hash +
                                         checksum)
    public_key_hash = hasher_ripemd160(hasher_single_sha256(public_keys[1]))
    checksum = hasher_double_sha256(version_byte + public_key_hash)[0:8]
    p2pkh_compressed = base58_from_hex(version_byte +
                                       public_key_hash +
                                       checksum)
    push_20 = "0014"
    script = push_20 + public_key_hash
    version_byte = "05"
    script_hash = hasher_ripemd160(hasher_single_sha256(script))
    checksum = hasher_double_sha256(version_byte + script_hash)[0:8]
    p2sh_p2wpkh = base58_from_hex(version_byte +
                                  script_hash +
                                  checksum)
    hrp_network_id = "bc"
    witness_version = 0
    witness_program = bytes_from_hex(public_key_hash)
    p2wpkh = encode_segwit_address(hrp_network_id,
                                   witness_version,
                                   witness_program)
    witness_version = 1
    output_public_key = public_keys[2]
    witness_program = bytes_from_hex(output_public_key)
    p2tr = encode_segwit_address(hrp_network_id,
                                 witness_version,
                                 witness_program)
    result = (p2pkh_uncompressed, p2pkh_compressed, p2sh_p2wpkh, p2wpkh, p2tr)
    return result


def get_balance(addresses: Addresses) -> Balances:
    """
    Get the Bitcoin balances, from the incoming addresses, using the
    online API for main network.
    """
    sleep(0.0)
    try:
        balances = []
        for address in addresses:
            response = get_from_api("https://blockstream.info/api/address/" +
                                    address)
            received = float(response.json()["chain_stats"]["funded_txo_sum"])
            spent = float(response.json()["chain_stats"]["spent_txo_sum"])
            balance = float((received - spent) / 100000000)
            balances.append(balance)
        result = tuple(balances)
        return result
    except Exception:
        try:
            balances = []
            for address in addresses:
                response = \
                    get_from_api("https://chain.so/api/v2/address/BTC/" +
                                 address)
                balance = float(response.json()["data"]["balance"])
                balances.append(balance)
            result = tuple(balances)
            return result
        except Exception:
            result = get_balance(addresses)
            return result


def data_export(queue: Queue) -> None:
    """
    Takes and organizes in the processing queue all necessary data
    related to each other, such as:
    - Attempt number
    - Private key in hexadecimal number
    - Private key encoded in WIF uncompressed and compressed to Base58
      over MainNet
    - Public key uncompressed and compressed in hexadecimal number
    - Internal public key in hexadecimal number
    - Output public key in hexadecimal number
    - Script public key in hexadecimal number
    - Addresses encoded to Base58 and Bech32/Bech32m over MainNet
    - Balances in floating point number
    """
    index = 0
    while True:
        private_key = generate_private_key()
        private_key_wif_uncompressed,  private_key_wif_compressed = \
            private_key_to_wif(private_key)
        public_key_uncompressed,  public_key_compressed = \
            get_public_key_from_private_key(private_key)
        internal_public_key = public_key_compressed[2:]
        output_public_key = taproot_tweak_public_key(internal_public_key)
        if not output_public_key:
            continue
        script_public_key = "5120" + output_public_key
        public_keys = (public_key_uncompressed,
                       public_key_compressed,
                       output_public_key)
        addresses = public_key_to_address(public_keys)
        balances = get_balance(addresses)
        index += 1
        attempt = str(index)
        data = (attempt.zfill(18),
                private_key.upper(),
                private_key_wif_uncompressed,
                private_key_wif_compressed,
                public_key_uncompressed.upper(),
                public_key_compressed.upper(),
                internal_public_key.upper(),
                output_public_key.upper(),
                script_public_key.upper(),
                addresses,
                balances)
        queue.put(data, block=False)


def worker(queue: Queue) -> None:
    """
    It receives the data from the processing queue, and conditionally
    tests whether the balances related to the Bitcoin addresses is
    positive or not, then present the result on the screen.
    """
    while True:
        if not queue.empty():
            data: BTC_Data = queue.get(block=True)
            balances = data[10]
            if not any(balances):
                clear()
                color_code = "91"
                license(color_code)
                result_to_screen(data, color_code)
            if any(balances):
                clear()
                color_code = "92"
                license(color_code)
                message = "- Bingo! Bitcoin address with a positive balance."
                result_to_screen(data, color_code, message)
                result_to_file(data, message)
                play_alert()


def result_to_screen(data: BTC_Data, color: str, message: str = "") -> None:
    """
    It will print all the information on the screen whether the Bitcoin
    addresses has a positive balances or not.
    """
    print(f"""\033[{color}m

                                            Attempt: [ {data[0]} ] {message}


                                   \33[1;7m[ PRIVATE KEYS ]\33[0m\033[{color}m
                         Private Key in Hexadecimal: {data[1]}
 Private Key in WIF (Base58) Uncompressed @ MainNet: {data[2]}
   Private Key in WIF (Base58) Compressed @ MainNet: {data[3]}

                                    \33[1;7m[ PUBLIC KEYS ]\33[0m\033[{color}m
             Public Key Uncompressed in Hexadecimal: {data[4][0:66]}
                                                       {data[4][66:]}
               Public Key Compressed in Hexadecimal: {data[5]}

                               \33[1;7m[ LEGACY ADDRESSES ]\33[0m\033[{color}m
      P2PKH Address (Base58) Uncompressed @ MainNet: {data[9][0]}
                                            Balance: {data[10][0]:.8f} BTC
        P2PKH Address (Base58) Compressed @ MainNet: {data[9][1]}
                                            Balance: {data[10][1]:.8f} BTC

                          \33[1;7m[ NESTED SEGWIT ADDRESS ]\33[0m\033[{color}m
             P2SH-P2WPKH Address (Base58) @ MainNet: {data[9][2]}
                                            Balance: {data[10][2]:.8f} BTC

                          \33[1;7m[ NATIVE SEGWIT ADDRESS ]\33[0m\033[{color}m
                  P2WPKH Address (Bech32) @ MainNet: {data[9][3]}
                                            Balance: {data[10][3]:.8f} BTC

                                \33[1;7m[ TAPROOT ADDRESS ]\33[0m\033[{color}m
            P2TR Internal Public Key in Hexadecimal: {data[6]}
              P2TR Output Public Key in Hexadecimal: {data[7]}
              P2TR Script Public Key in Hexadecimal: {data[8]}
                   P2TR Address (Bech32m) @ MainNet: {data[9][4]}
                                            Balance: {data[10][4]:.8f} BTC
\033[0m""")


def result_to_file(data: BTC_Data, message: str) -> None:
    """
    Finding any Bitcoin address with a positive balance, it will record
    all the information in a text file.
    """
    with open("found.txt", "a+") as file:
        file.write(f"""
                                            Attempt: [ {data[0]} ] {message}


                                   [ PRIVATE KEYS ]
                         Private Key in Hexadecimal: {data[1]}
 Private Key in WIF (Base58) Uncompressed @ MainNet: {data[2]}
   Private Key in WIF (Base58) Compressed @ MainNet: {data[3]}

                                    [ PUBLIC KEYS ]
             Public Key Uncompressed in Hexadecimal: {data[4][0:66]}
                                                       {data[4][66:]}
               Public Key Compressed in Hexadecimal: {data[5]}

                               [ LEGACY ADDRESSES ]
      P2PKH Address (Base58) Uncompressed @ MainNet: {data[9][0]}
                                            Balance: {data[10][0]:.8f} BTC
        P2PKH Address (Base58) Compressed @ MainNet: {data[9][1]}
                                            Balance: {data[10][1]:.8f} BTC

                          [ NESTED SEGWIT ADDRESS ]
             P2SH-P2WPKH Address (Base58) @ MainNet: {data[9][2]}
                                            Balance: {data[10][2]:.8f} BTC

                          [ NATIVE SEGWIT ADDRESS ]
                  P2WPKH Address (Bech32) @ MainNet: {data[9][3]}
                                            Balance: {data[10][3]:.8f} BTC

                                [ TAPROOT ADDRESS ]
            P2TR Internal Public Key in Hexadecimal: {data[6]}
              P2TR Output Public Key in Hexadecimal: {data[7]}
              P2TR Script Public Key in Hexadecimal: {data[8]}
                   P2TR Address (Bech32m) @ MainNet: {data[9][4]}
                                            Balance: {data[10][4]:.8f} BTC
\n\n\n
""")


def play_alert() -> None:
    """
    Plays this alert sound if any Bitcoin address with a positive
    balance is found.
    """
    AudioPlayer("alert.mp3").play(block=True)


def license(color: str) -> None:
    """Print the license information on the screen."""
    print(f"""\033[{color}m
            Bitcoin Wallet Hack  Copyright (C) 2021  Gustavo Madureira
            This program comes with ABSOLUTELY NO WARRANTY.
            
            

            \33[1;7m ***  *** \033[0m""")


def thread() -> Any:
    """CPU thread process for data_export() and worker()."""
    processes = []
    data: object = Queue()
    data_factory = Process(target=data_export, args=(data,))
    data_factory.daemon = True
    processes.append(data_factory)
    data_factory.start()
    work = Process(target=worker, args=(data,))
    work.daemon = True
    processes.append(work)
    work.start()
    data_factory.join()


if __name__ == "__main__":
    try:
        pool = ThreadPool(processes=cpu_count() * 2)
        pool.map(thread(), range(0, 1))  # Limit to single CPU thread.
    except Exception:
        pool.close()
        exit()

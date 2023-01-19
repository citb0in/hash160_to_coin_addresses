#/usr/bin/env python3
# by citb0in, 2023/Jan/19
import sys
import hashlib
import base58
import bech32

# example:
# --------
# privatekey=1
# hash=751e76e8199196d454941c45d1b3a323f1433bd6
# BTC legacy address = 1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH
# BTC native segwit (bech32) address = bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4

# fetch the hash160 via command-line argument or enter it manually here
h_hex = sys.argv[1]
#h = '751e76e8199196d454941c45d1b3a323f1433bd6'

h = bytes.fromhex(h_hex)

# version byte (for Bitcoin "00")
version_btc = b"\x00"
# version byte (for Dogecoin "1E")
version_doge = b"\x1E"
# version byte (for Litecoin "30")
version_ltc = b"\x30"

# witness program
wit_prog = h

# hash160 + version byte
h_btc = version_btc + h
h_doge = version_doge + h
h_ltc = version_ltc + h

# double-sha256
r_btc = hashlib.sha256(h_btc).digest()
r_doge = hashlib.sha256(h_doge).digest()
r_ltc = hashlib.sha256(h_ltc).digest()
r_btc = hashlib.sha256(r_btc).digest()
r_doge = hashlib.sha256(r_doge).digest()
r_ltc = hashlib.sha256(r_ltc).digest()

# first 4 bytes of sha256(sha256)
checksum_btc = r_btc[:4]
checksum_doge = r_doge[:4]
checksum_ltc = r_ltc[:4]

# hash160 + version byte + checksum
address_btc = h_btc + checksum_btc
address_doge = h_doge + checksum_doge
address_ltc = h_ltc + checksum_ltc

# base58
address_btc = base58.b58encode(address_btc)
address_doge = base58.b58encode(address_doge)
address_ltc = base58.b58encode(address_ltc)
# convert witness program to bech32 address with "bc1q" prefix
hrp_btc = 'bc'
hrp_ltc = 'ltc'
witver_btc = witver_ltc = 0

#witver_doge = '1E'
address_btc_bech32 = bech32.encode(hrp_btc, witver_btc, wit_prog)
address_ltc_bech32 = bech32.encode(hrp_ltc, witver_ltc, wit_prog)

print(f'\n\nHash160 = {h_hex}')
print(f'Bitcoin (BTC) address = {address_btc.decode()}')
print(f'Bitcoin (BTC) bech32 address = {address_btc_bech32}')
print(f'Dogecoin (DOGE) address = {address_doge.decode()}')
print(f'Litecoin (LTC) address = {address_ltc.decode()}')
print(f'Litecoin (LTC) bech32 address = {address_ltc_bech32}')

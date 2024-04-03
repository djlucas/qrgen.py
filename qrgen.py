# Fix lables in your 2FA tool:
# STDLIB
import argparse
import sys
from urllib import parse

# https://github.com/nayuki/QR-Code-generator/tree/master/python
from qrcodegen import QrCode, QrSegment


QREL = QrCode.Ecc.LOW

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--label",
                    type=str,
                    help="Text of the label",
                    metavar="STR")
parser.add_argument("-s", "--secret",
                    type=str,
                    help="text secret provided by the OTP auth generator",
                    metavar="SECRET")
args = parser.parse_args()

if args.label:
    OTP_Label = parse.quote(args.label)
else:
    sys.stderr.write("OTP_Label is required! Exiting...")
    exit(1)

if args.secret:
    OTP_secret = args.secret
else:
    sys.stderr.write("OTP_Secret is required! Exiting...")
    exit(1)

QREL = QrCode.Ecc.LOW
OTP_URI = "otpauth://totp/" + str(OTP_Label) + "?secret=" + str(OTP_Secret)

def to_svg_str(qr: QrCode, border: int) -> str:
	"""Returns a string of SVG code for an image depicting the given QR Code, with the given number
	of border modules. The string always uses Unix newlines (\n), regardless of the platform."""
	if border < 0:
		raise ValueError("Border must be non-negative")
	parts: List[str] = []
	for y in range(qr.get_size()):
		for x in range(qr.get_size()):
			if qr.get_module(x, y):
				parts.append(f"M{x+border},{y+border}h1v1h-1z")
	return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 {qr.get_size()+border*2} {qr.get_size()+border*2}" stroke="none">
	<rect width="100%" height="100%" fill="#FFFFFF"/>
	<path d="{" ".join(parts)}" fill="#000000"/>
</svg>
"""

def print_qr(qrcode: QrCode) -> None:
	"""Prints the given QrCode object to the console."""
	border = 4
	for y in range(-border, qrcode.get_size() + border):
		for x in range(-border, qrcode.get_size() + border):
			print("\u2588 "[1 if qrcode.get_module(x,y) else 0] * 2, end="")
		print()
	print()

QR = QrCode.encode_text(OTP_URI, QREL)
print_qr(QR)
print(to_svg_str(QR, 4))

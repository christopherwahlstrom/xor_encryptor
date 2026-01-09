from __future__ import annotations


import argparse
import sys
from pathlib import Path


def parse_key(key_str: str) -> bytes:
     """TOlkar nyckeln från terminalen till bytes.
     Hanterar tre format 
      1) Hexadecimal byte, som tex. 0x41
      2) Hexadecimal sträng,som tex. 41:42:43 eller 414243
      3) Vanlig textsträng, som tex. '"""

     s = key_str.strip()

     # 1. Här hanterar vi hexadecimal byte.
     if s.lower().startswith("0x"):
          value = int(s, 16)
          if not (0 <= value <= 255):
               raise ValueError("Hex key must be between 0x00 and 0xFF")
          return bytes([value])
     
     # 2. Här hanterar vi hexadecimal sträng.
     hex_candidate = s.replace(":", "").replace(" ", "")
     if (
          len(hex_candidate) > 0
          and len(hex_candidate) % 2 == 0
          and all(c in "0123456789abcdefABCDEF" for c in hex_candidate)
     ):
          

          return bytes.fromhex(hex_candidate)
     
     # 3. Här hanterar vi vanlig textsträng.
     return s.encode("utf-8")
     

def xor_bytes(data: bytes, key: bytes) -> bytes:

     """ Detta kodblock utför XOR-operationen mellan data och nyckeln.
     Efteersom XOR är symmetriskt används denna för både kryptering och dekryptering."""

     if not key:
          raise ValueError("Key must not be empty")
     
     # Här använder bi bytearray för kunna ändra värdena. 
     out = bytearray(len(data))
     klen = len(key) 

     for i, b in enumerate(data):
          # XOR-operation och Vi använder modulo för att repetera nyckeln.
          out[i] = b ^ key[i % klen]
     return bytes(out)
     
def format_python(data: bytes) -> str:
     
     # Här formateras bytes till en Python-variabel.

     return 'buf = b"' + "".join(f"\\x{b:02x}" for b in data) + '"\n'
     
def format_c(data:bytes, name: str = "buf", per_line: int = 16) -> str:

     # Här formateras bytes till en C-array för att användas i loaders.

     lines = []
     for i in range(0, len(data), per_line):
          chunk = data[i: i + per_line]
          lines.append("     " + ", ".join(f"0x{b:02x}" for b in chunk))
     body = ",\n".join(lines)
     return (
          f"unsigned char {name}[] = {{\n{body}\n}};\n"
          f"unsigned int {name}_len = {len(data)};\n"
     
     )
     
def build_parser() -> argparse.ArgumentParser:

     # Här byggs argument-parsen för CLI gränssnittet.

     p = argparse.ArgumentParser(description="XOR-transform a file and output raw/python/c views.")

     # Här definerar jag obligatoriska argument enligt uppgiftskraven.
     p.add_argument("--in", dest="in_path", required=True, help="Input file path (read as bytes).")
     p.add_argument("--out", dest="out_path", required=True, help="Output file path (raw bytes).")
     p.add_argument("--key", required=True, help="Key: 0x41 | 41:42:43 | 'textkey'")

     # Här definerar jag ett valfritt argument för utdataformat.
     p.add_argument("--format", choices=["raw", "python", "c"],default="raw", help="Output format: raw bytes, python bytes literal, or C array."
)

     return p


def main(argv: list[str]) -> int:
     args = build_parser().parse_args(argv)

     in_path = Path(args.in_path)
     out_path = Path(args.out_path)

     # Här läser vi in filen binärt
     data = in_path.read_bytes() 

     try: 
          key = parse_key(args.key)
     except ValueError as e:
          print(f"[!] Key error: {e}")
          return 1

     # Här utför vi kryptering/dekryptering
     transformed = xor_bytes(data, key) 

     # Här hanterar vi utdatans format och skriver till fil.
     fmt = args.format

     if fmt == "raw":
          out_path.write_bytes(transformed)

     elif fmt == "python":
          out_path.write_text(format_python(transformed), encoding="utf-8")

     elif fmt == "c":
          out_path.write_text(format_c(transformed, name="buf"), encoding="utf-8")


     print(f"[+] Read {len(data)} bytes from {in_path}")
     print(f"[+] Key length: {len(key)} bytes")
     print(f"[+] Wrote {len(transformed)} bytes to {out_path}")  

     return 0


if __name__ == "__main__":
     raise SystemExit(main(sys.argv[1:]))


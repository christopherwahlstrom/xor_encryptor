# XOR encryptor 

Uppgift i kursen Programmering för penetrationstestare

Ett CLI-verktyg för att XOR-obfuskerar en binär fil tex. raw  shellcode med en nyckel och kan skriva output i raw/python/c format. 

Verktyget kan läsa in binära filer , kryptera dom med valfri nyckel och spara resultatet bytes , c kod , python kod. Samma funktioner används för dekryptering.

## Användning

Raw bytes : 
python3 xorcrypt.py --in demo.bin --out encrypted.bin --key 0xAA


Python-format:

python3 xorcrypt.py --in pythondemo.bin --out pythonencrypted.bin --key 0xAA

Exempel output python: 

buf = b"\xfa\xd3\xde\xc2\xc5\xc4\x8a\xce\xcf\xc7\xc5"

C-format: 

python3 xorcrypt.py --in cdemo.bin --out payload.c --key 0xAA --format c

Exempel output C: 

unsigned char buf[] = {
     0xe9, 0x8a, 0xce, 0xcf, 0xc7, 0xc5
};
unsigned int buf_len = 6


Dekryptera (exempel kod): 

python3 xorcrypt.py --in encrypted.bin --out decrypted.bin --key 0xAA


## Verifiera

Jag kontrollerade output med xxd (hexdump) och såg att XOR är reversibelt genom att köra samma nyckel igen xxd visar offset till vänster , bytes i hex i mitten och ASCII till höger om det går att tolka.


## Kommentarer 

XOR är obfuskering inte kryptering.






# FRÅN LÄRARE NEDAN krav spec.

# Shellcode XOR Encryptor i Python

## Projektöversikt

I detta slutprojekt ska du skapa ett verktyg som XOR-krypterar shellcode i Python.  
Målet är att bygga ett praktiskt, realistiskt säkerhetsverktyg som används som del i en payload-kedja, där:

- **Python-verktyget obfuskerar shellcoden**
- **ett separat loader-program (ofta byggt i C) avkrypterar och kör den**

Detta motsvarar hur riktiga red-teamers, malwareutvecklare och säkerhetsforskare arbetar.

---

# Mål med projektet

Du ska skapa ett CLI-verktyg som:

1. läser rå shellcode från en fil (binärt eller textformat)
2. XOR-krypterar shellcoden med en nyckel (1 byte eller flera)
3. producerar krypterad shellcode i olika output-format:
   - rå bytes
   - python-array
   - C-array (vanligast i malware/loader-kod)
4. använder argparse för att hantera argument
5. har dokumentation och exempel

Verktyget behöver **inte** kunna dekryptera shellcode.  
Dekryptering sker i *target loadern*, inte här.

---

# Varför används XOR-kryptering på shellcode?

XOR används för:

- att kringgå signaturbaserade antivirus
- att undvika byte-sekvenser som EDR letar efter
- att obfuska payload inför transport eller lagring
- att minimera möjligheten att verktyg som strings, YARA och binwalk upptäcker shellcode

**Detta är inte säker kryptering — det är obfuskering.**  
Men det fungerar effektivt mot enklare detektioner.

---

# Projektkrav

## Funktionalitet

Programmet ska kunna:

- läsa en fil med shellcode (t.ex. `raw.bin`)
- använda en XOR-nyckel (1 byte eller fler)
- generera krypterad shellcode
- spara den till fil samt kunna skriva ut i olika format:

Exempel:

```
python xorcrypt.py --in raw.bin --out encrypted.bin --key 0x42 --format c
```

Output som C-array:

```
unsigned char buf[] = { 0x12, 0xA1, 0x4F };
```

## CLI-argument (argparse)

Exempel på argument:

| Flagga     | Beskrivning                       |
| ---------- | --------------------------------- |
| `--in`     | Inputfil med raw shellcode        |
| `--out`    | Outputfil med krypterad shellcode |
| `--key`    | XOR-nyckel (hex eller string)     |
| `--format` | output-format: raw, python, c     |

**Inga subkommandon behövs.**

---

# Kodstruktur

- `main()` för argparse
- docstrings  
- informativa kommentarer  


---

# README-krav

Din README ska innehålla:

- kort beskrivning av verktyget
- hur man kör det
- exempelkommandon
- exempel på output-format

---

# Inlämning

Lägg upp koden och readme på ditt github konto och lämna in länken
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
probe_decompress.py — быстрый тестер для "непонятно чем сжатых" файлов.

Usage:
  python probe_decompress.py input.bin
"""

import sys
import os
import io
import math
import zlib
import gzip
import bz2
import lzma
import binascii
import lz4.block
import lz4.frame

from collections import Counter

# Опциональные алгоритмы
opt = {}

for name, mod in [
    ("lz4", "lz4.frame"),
    ("zstd", "zstandard"),
    ("snappy", "snappy"),
]:
    try:
        opt[name] = __import__(mod, fromlist=["*"])
    except Exception:
        opt[name] = None

# ---- Утилиты ----

def save_output(base_path, method, data, idx=None):
    root, ext = os.path.splitext(base_path)
    tag = f"{root}.out.{method}" + (f".{idx}" if idx is not None else "")

    with open(tag, "wb") as f:
        f.write(data)

    print(f"[+] saved -> {tag} ({len(data)} bytes)")

def entropy(b: bytes, max_bytes=65536):

    if not b:
        return 0.0
    
    sample = b[:max_bytes]
    c = Counter(sample)
    n = len(sample)
    H = 0.0

    for cnt in c.values():
        p = cnt / n
        H -= p * math.log2(p)

    return H

MAGICS = {
    b"\x89PNG": "PNG",
    b"DDS ": "DDS",
    b"KTX ": "KTX",
    b"PK\x03\x04": "ZIP",
    b"\x1F\x8B": "GZIP",
    b"\xFF\xD8\xFF": "JPEG",
    b"RIFF": "RIFF\\WAV",
    b"OggS": "OGG",
    b"MZ": "PE/EXE",
    b"\x7FELF": "ELF",
    b"%PDF-": "PDF",
    b"\x89BIN": "BIN89?",  # редкая заглушка
}

def find_magics(b: bytes, extra=None, limit=20):
    res = []
    search_set = dict(MAGICS)

    if extra:
        search_set.update(extra)

    for sig, name in search_set.items():
        start = 0

        while True:
            i = b.find(sig, start)

            if i < 0: break

            res.append((i, name, sig))
            start = i + 1

            if len(res) >= limit:
                return sorted(res)
            
    return sorted(res)

def extract_ascii(b: bytes, min_len=6, limit=50):
    out = []
    cur = []

    for ch in b:

        if 32 <= ch <= 126 or ch in (9, 10, 13):
            cur.append(ch)
        else:

            if len(cur) >= min_len:
                out.append(bytes(cur).decode("ascii", "ignore"))

                if len(out) >= limit:
                    break

            cur = []

    if len(cur) >= min_len and len(out) < limit:
        out.append(bytes(cur).decode("ascii", "ignore"))

    return out

def try_call(name, func, save_base=None):

    try:
        data = func()

        if data is None:
            print(f"[-] {name}: no output")
            return False
        
        print(f"[+] {name}: OK, size={len(data)}, entropy={entropy(data):.2f}")
        mags = find_magics(data, limit=8)

        if mags:
            print("    found magics:", ", ".join(f"{n}@{i}" for i, n, _ in mags))

        ascii_snips = extract_ascii(data, min_len=12, limit=3)

        if ascii_snips:
            print("    ascii:", " | ".join(repr(s) for s in ascii_snips))

        if save_base:
            save_output(save_base, name, data)

        return True
    
    except Exception as e:
        print(f"[-] {name}: {type(e).__name__}: {e}")
        return False

def scan_zlib_at_offsets(blob: bytes, offsets, save_base=None, tag="zlib@"):
    successes = 0

    for off in offsets:

        if off >= len(blob):
            continue

        # Признаки возможного zlib-заголовка (CMF/FLG)
        if blob[off:off+1] != b"\x78" and blob[off:off+2] not in (b"\x78\x01", b"\x78\x9C", b"\x78\xDA"):
            # Дадим шанс редким вариантам, но в целом фильтруем
            pass

        def _f():
            return zlib.decompress(blob[off:])
        
        ok = try_call(f"{tag}{off}", _f, save_base)
        successes += int(ok)
    return successes

def scan_gzip_at_offsets(blob: bytes, save_base=None, tag="gzip@"):
    successes = 0
    start = 0
    while True:
        i = blob.find(b"\x1F\x8B", start)
        if i < 0:
            break
        def _f(i=i):
            bio = io.BytesIO(blob[i:])
            with gzip.GzipFile(fileobj=bio, mode="rb") as gf:
                return gf.read()
        ok = try_call(f"{tag}{i}", _f, save_base)
        successes += int(ok)
        start = i + 1
    return successes

# ---- Основная логика ----

def main(path):
    with open(path, "rb") as f:
        blob = f.read()

    print(f"[i] input: {path} ({len(blob)} bytes)")
    print(f"[i] head: {binascii.hexlify(blob[:32]).decode()}")
    print(f"[i] entropy ~ {entropy(blob):.2f} bits/byte")

    mags = find_magics(blob, limit=20)

    if mags:
        print("[i] magics in raw:", ", ".join(f"{n}@{i}" for i, n, _ in mags))
    else:
        print("[i] no known magics in raw")

    # Прямые попытки
    print("\n== direct attempts ==")
    try_call("zlib", lambda: zlib.decompress(blob), save_base=path)
    try_call("deflate(raw,-15)", lambda: zlib.decompress(blob, -15), save_base=path)
    try_call("gzip", lambda: gzip.decompress(blob), save_base=path)
    try_call("bz2", lambda: bz2.decompress(blob), save_base=path)
    try_call("lz4.block", lambda: lz4.block.decompress(blob, 1_048_576), save_base=path)
    try_call("lz4.frame", lambda: lz4.frame.decompress(blob, 1_048_576), save_base=path)

    # Перебор всех возможных (и нет) пареметров для ZLIB\Deflate
    for i in range(-16384, 16384):

        try:
            zlib.decompress(blob, i)
            print(f"[+] ZLIB or Deflate unpacked with parametr {i}!")
            break
        except zlib.error:
            pass

    else:
        print(f"[-] ZLIB or Deflate not worked!")

    try:
        try_call("lzma_auto", lambda: lzma.decompress(blob), save_base=path)
    except Exception as error:
        print(f"[-] lzma_auto: not supported in this Python? {error}")

    # Опциональные
    if opt["zstd"]:

        def _zstd():
            dctx = opt["zstd"].ZstdDecompressor()
            return dctx.decompress(blob)
        
        try_call("zstd", _zstd, save_base=path)

    if opt["snappy"]:
        try_call("snappy", lambda: opt["snappy"].decompress(blob), save_base=path)

    # Сканирование сигнатур и распаковка оттуда
    print("\n== scan for embedded streams ==")
    # zlib CMF/FLG часто 78 01 / 78 9C / 78 DA — пройдёмся по всем позициям этих сигнатур
    z_candidates = []

    for sig in (b"\x78\x01", b"\x78\x9C", b"\x78\xDA"):
        start = 0

        while True:
            i = blob.find(sig, start)

            if i < 0: break

            z_candidates.append(i)
            start = i + 1

    z_candidates = sorted(set(z_candidates))

    if z_candidates:
        print(f"[i] zlib-like headers at: {z_candidates[:30]}{'...' if len(z_candidates)>30 else ''}")
        scan_zlib_at_offsets(blob, z_candidates, save_base=path)
    else:
        print("[i] no zlib-like headers found")

    # gzip
    g_success = scan_gzip_at_offsets(blob, save_base=path)

    if g_success == 0:
        print("[i] no valid gzip members found (or all failed to decompress)")

    # Попытка "сдвига начала" (обрезка первых N байт)
    print("\n== trimmed head attempts (1..64 bytes) ==")

    for cut in range(1, 65):
        sub = blob[cut:]
        name = f"trim{cut}.zlib"

        if try_call(name, lambda sub=sub: zlib.decompress(sub)):
            save_output(path, name, zlib.decompress(sub))

        name = f"trim{cut}.deflate"

        if try_call(name, lambda sub=sub: zlib.decompress(sub, -15)):
            save_output(path, name, zlib.decompress(sub, -15))

        name = f"trim{cut}.gzip"

        if try_call(name, lambda sub=sub: gzip.decompress(sub)):
            save_output(path, name, gzip.decompress(sub))

    # Перебор XOR-ключа
    print("\n== XOR brute (1..255): search zlib/gzip inside ==")
    found_any = 0

    for key in range(1, 256):
        x = bytes(b ^ key for b in blob)
        # быстрые признаки: zlib/gzip внутри
        spots = []

        for sig in (b"\x78\x01", b"\x78\x9C", b"\x78\xDA"):
            start = 0

            while True:
                i = x.find(sig, start)

                if i < 0: break

                spots.append(i)
                start = i + 1
        gz_spots = []
        start = 0

        while True:
            i = x.find(b"\x1F\x8B", start)

            if i < 0: break

            gz_spots.append(i)
            start = i + 1

        if not spots and not gz_spots:
            continue

        # Попробовать распаковку с первого найденного места (несколько, но ограничим)
        tried = 0
        ok = False

        for off in sorted(set(spots))[:3]:

            try:
                data = zlib.decompress(x[off:])
                save_output(path, f"xor{key:02x}.zlib@{off}", data)
                print(f"[+] XOR {key:02x}: zlib@{off} OK (len={len(data)})")
                ok = True
                break
            except Exception:
                pass

            tried += 1

        if not ok:

            for off in sorted(set(gz_spots))[:3]:

                try:
                    bio = io.BytesIO(x[off:])

                    with gzip.GzipFile(fileobj=bio, mode="rb") as gf:
                        data = gf.read()

                    save_output(path, f"xor{key:02x}.gzip@{off}", data)
                    print(f"[+] XOR {key:02x}: gzip@{off} OK (len={len(data)})")
                    ok = True
                    break

                except Exception:
                    pass
        if ok:
            found_any += 1
            # не выходим — возможно, несколько ключей валидны, но чтобы не заспамить, оставим как есть

    if found_any == 0:
        print("[i] XOR brute produced no valid zlib/gzip members")

    # Поиск ASCII строк для эвристик
    print("\n== ASCII strings (first 10) ==")
    strings = extract_ascii(blob, min_len=8, limit=10)

    if strings:

        for s in strings:
            print("  >", repr(s[:120]))

    else:
        print("  (none)")

    print("\n== Done ==")

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python probe_decompress.py <input_file>")
    #     sys.exit(1)
    # main(sys.argv[1])
    main(r"D:\out\grimrock_dat\00000001.dat")

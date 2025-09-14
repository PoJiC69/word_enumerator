#!/usr/bin/env python3

from __future__ import annotations
import argparse
import itertools
import math
import secrets
import string
import sys
from typing import Generator, Iterable

DEFAULT_MAX = 1_000_000  # cap for full enumeration (change with caution)


def build_charset(use_lower: bool, use_upper: bool, use_digits: bool, use_special: bool, extra_special: str = "") -> str:
    parts = []
    if use_lower:
        parts.append(string.ascii_lowercase)
    if use_upper:
        parts.append(string.ascii_uppercase)
    if use_digits:
        parts.append(string.digits)
    if use_special:
        # conservative common special characters; user may extend via extra_special
        common_specials = "!@#$%^&*()-_=+[]{};:,.<>/?"
        parts.append(common_specials + extra_special)
    charset = "".join(parts)
    # remove duplicates while preserving order
    return "".join(dict.fromkeys(charset))


def total_combinations(charset_len: int, min_len: int, max_len: int) -> int:
    """Compute sum_{L=min_len..max_len} (charset_len ** L) safely."""
    if charset_len <= 0 or min_len < 1 or max_len < min_len:
        return 0
    # If min_len == max_len, it's simpler
    total = 0
    for L in range(min_len, max_len + 1):
        # use pow with int
        total += pow(charset_len, L)
        # early stop if grows beyond python int (but python int is unbounded)
    return total


def enumerate_all(charset: str, min_len: int, max_len: int) -> Generator[str, None, None]:
    """Yield every combination (ordered) for lengths in [min_len, max_len]."""
    if not charset:
        raise ValueError("Charset is empty. Enable at least one character class.")
    if min_len < 1 or max_len < min_len:
        raise ValueError("Invalid length range.")
    for L in range(min_len, max_len + 1):
        # itertools.product returns tuples of characters of length L
        for tup in itertools.product(charset, repeat=L):
            yield "".join(tup)


def sample_random(charset: str, length: int, count: int) -> list[str]:
    """Return 'count' cryptographically-random sample words of given length."""
    if not charset:
        raise ValueError("Charset is empty. Enable at least one character class.")
    return ["".join(secrets.choice(charset) for _ in range(length)) for __ in range(count)]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Safe word enumerator / generator.")
    group = p.add_mutually_exclusive_group(required=False)
    p.add_argument("--min", type=int, default=None, help="Minimum length (inclusive).")
    p.add_argument("--max", type=int, default=None, help="Maximum length (inclusive).")
    p.add_argument("--length", type=int, default=None, help="Exact length (shorthand for --min and --max equal).")
    p.add_argument("--lower", action="store_true", help="Include lowercase letters (a-z).")
    p.add_argument("--upper", action="store_true", help="Include uppercase letters (A-Z).")
    p.add_argument("--digits", action="store_true", help="Include digits (0-9).")
    p.add_argument("--special", action="store_true", help="Include special characters.")
    p.add_argument("--extra-special", type=str, default="", help="Extra special characters to include.")
    p.add_argument("--out", type=str, default=None, help="Write output to file instead of stdout.")
    p.add_argument("--sample", type=int, default=0, help="Do not enumerate; instead output N random sample words.")
    p.add_argument("--cap", type=int, default=DEFAULT_MAX, help=f"Enumeration cap (default {DEFAULT_MAX:,}).")
    p.add_argument("--force", action="store_true", help="Override cap and force enumeration (use responsibly).")
    p.add_argument("--show-stats", action="store_true", help="Show charset and total combinations and exit.")
    return p.parse_args()


def main():
    args = parse_args()

    # Resolve lengths
    if args.length is not None:
        min_len = max_len = args.length
    else:
        if args.min is None or args.max is None:
            print("Error: specify either --length or both --min and --max.", file=sys.stderr)
            return 1
        min_len = args.min
        max_len = args.max

    # Build charset
    charset = build_charset(args.lower, args.upper, args.digits, args.special, args.extra_special)

    if not charset:
        print("Error: No character classes selected. Use --lower, --upper, --digits, and/or --special.", file=sys.stderr)
        return 1

    total = total_combinations(len(charset), min_len, max_len)

    if args.show_stats:
        print(f"CHARSET ({len(charset)} chars): {charset}")
        print(f"LENGTH RANGE: {min_len} .. {max_len}")
        print(f"TOTAL COMBINATIONS: {total:,}")
        return 0

    # If sampling requested, produce random samples
    if args.sample > 0:
        if args.length is None:
            print("Error: --sample requires a single --length to be set.", file=sys.stderr)
            return 1
        samples = sample_random(charset, args.length, args.sample)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                for s in samples:
                    f.write(s + "\n")
            print(f"Wrote {len(samples)} samples to {args.out}")
        else:
            for s in samples:
                print(s)
        return 0

    # Check cap
    if total == 0:
        print("Nothing to do (zero total combinations).", file=sys.stderr)
        return 1

    if total > args.cap and not args.force:
        print(
            "Refusing to enumerate: total combinations = {:,} exceed cap {:,}.\n"
            "Use --show-stats to inspect the parameters, or use --sample N to get random samples.\n"
            "If you really want to force enumeration, rerun with --force (dangerous).".format(total, args.cap),
            file=sys.stderr,
        )
        return 1

    # Perform enumeration (streaming)
    out_f = None
    try:
        if args.out:
            out_f = open(args.out, "w", encoding="utf-8")
            writer = lambda s: out_f.write(s + "\n")
        else:
            writer = lambda s: print(s)

        i = 0
        for word in enumerate_all(charset, min_len, max_len):
            writer(word)
            i += 1
        if args.out:
            print(f"Enumeration complete. Wrote {i:,} items to {args.out}")
        else:
            # If writing to stdout, we won't summarize further to avoid messing streams
            pass
    finally:
        if out_f:
            out_f.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())

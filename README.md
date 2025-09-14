# Word Enumerator / Generator

A safe, configurable Python tool to **generate** or **enumerate** all possible words from selected character classes (lowercase, uppercase, digits, special characters) for a specified length or length range.

> ⚠️ **Safety first.** Generating *all* combinations grows exponentially and can easily produce extremely large outputs. This tool **refuses** to enumerate when the total number of combinations exceeds a configurable cap (default `1_000_000`). Do **not** use this for unauthorized access or as a brute-forcing tool. Use only for education, testing on systems you own, or small-scale datasets.

---

## Features

* Build a charset from: lowercase, uppercase, digits, and special characters (with optional extra specials).
* Enumerate every combination for lengths in a given range (streaming output).
* Produce cryptographically-random sample words instead of enumerating a huge space.
* Safety cap to prevent accidental huge enumerations; optional `--force` to override.
* Write output to stdout or a file.

---

## Requirements

* Python 3.8+ (should work on 3.8, 3.9, 3.10, 3.11, ...)

No external dependencies — only uses Python standard library (`argparse`, `itertools`, `secrets`, `string`, etc).

---

## Installation

1. Save the script as `word_enumerator.py` (or use the provided file).
2. Make it executable (optional):

```bash
chmod +x word_enumerator.py
```

---

## Usage

Basic CLI options:

```
usage: word_enumerator.py [--min MIN] [--max MAX] [--length LENGTH]
                          [--lower] [--upper] [--digits] [--special]
                          [--extra-special EXTRA_SPECIAL] [--out OUT]
                          [--sample SAMPLE] [--cap CAP] [--force]
                          [--show-stats]
```

Important flags:

* `--min` and `--max` — range of lengths (inclusive). Both required unless `--length` is used.
* `--length` — shorthand to set a single exact length.
* `--lower` / `--upper` / `--digits` / `--special` — include those character classes.
* `--extra-special` — additional special chars to append.
* `--out FILE` — write results to `FILE` instead of stdout.
* `--sample N` — output `N` random sample words (requires `--length`).
* `--cap N` — set the enumeration safety cap (default `1_000_000`).
* `--force` — override the cap and enumerate anyway (dangerous).
* `--show-stats` — show charset and total combinations and exit.

---

## Examples

1. Show stats for lowercase only, lengths 1..3:

```bash
python word_enumerator.py --min 1 --max 3 --lower --show-stats
```

2. Enumerate lowercase-only words length 1..3 (safe small space):

```bash
python word_enumerator.py --min 1 --max 3 --lower
```

3. Write all lowercase+digits length 1..4 to `all.txt` (may be large — check stats first):

```bash
python word_enumerator.py --min 1 --max 4 --lower --digits --out all.txt
```

4. Generate 100 random samples of length 12 using full charset:

```bash
python word_enumerator.py --length 12 --lower --upper --digits --special --sample 100
```

5. Inspect number of combinations before enumerating:

```bash
python word_enumerator.py --min 1 --max 5 --lower --upper --digits --show-stats
# If it's within the cap you can then run the actual enumeration.
```

6. Forcing enumeration (use with extreme caution):

```bash
python word_enumerator.py --min 1 --max 6 --lower --digits --force --out out.txt
```

---

## Small output example

Running:

```bash
python word_enumerator.py --min 1 --max 2 --lower
```

Will print:

```
a
b
c
...
z
aa
ab
ac
...
zz
```

---

## Implementation notes

* The enumerator streams output (does not store everything in memory).
* The safety cap defaults to `1_000_000` total combinations. You can change this with `--cap` or set `--force` to override.
* Random sampling uses `secrets.choice()` for cryptographic randomness (appropriate for password/passphrase generation, not for cracking).
* The special characters default set is conservative; add more with `--extra-special` if you need.

---

## Security & Ethics

This tool is provided for legitimate educational and testing purposes only. Do **not** use it to attempt unauthorized access to accounts, devices, or networks. The author disclaims any responsibility for misuse.

If you're trying to **create** strong passwords, prefer the random-sample mode or use a dedicated password manager. If you're performing security testing, ensure you have explicit permission from the system owner.

---

## License

MIT License — see `LICENSE` (or add the text below) for details.

---

## Contributing

Small fixes, improvements, and better CLI ergonomics are welcome. If you add features that increase risk (e.g., removing the cap), please also add stronger warnings and confirmation prompts.

---

## Contact / Credits

Created as a small educational utility. If you need a tailored variant (library API, progress indicator, GUI wrapper, or integration into tests), tell me what you need and I can help craft it.

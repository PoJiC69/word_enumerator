# word_enumerator
"""
word_enumerator.py

Generate ALL possible words from selected character sets for lengths in a given range.

Safe defaults: refuses to enumerate when total combinations > DEFAULT_MAX.

Usage examples:
  # list combinations (small space)
  python word_enumerator.py --min 1 --max 3 --lower

  # write combinations to file
  python word_enumerator.py --min 1 --max 4 --lower --digits --out all.txt

  # generate 100 random sample words from a large space without enumerating
  python word_enumerator.py --length 12 --lower --upper --digits --special --sample 100

  # force enumeration (dangerous)
  python word_enumerator.py --min 1 --max 6 --lower --digits --force --out out.txt
"""

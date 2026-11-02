#!/usr/bin/env python3
"""Word-frequency census of the text in the master image. Aggregator only -- it reads NO pixels.

usage: python3 -I word_census.py            writes word_census.tsv, prints the summary

Every string here comes from the existing census: brain_image_corpus.py's transcriptions
(slogan_lines.py's HEADLINE, the AMENDMENT copy, the RUSSIAN rune decodes, LATIN_MOTTOS,
CENSUS_MISC, DATES, MICROTEXT, WHITEPAPER) and census_crops.py's ELEMENTS/SCREENED element
list.
This script adds no new reading of the image and no new word.

[NOTE 2026-11-02] `census_crops.DRAWN` is now the machine-readable canvas census -- every
string measured as painted on the image, with box, status and provenance -- and it is what
`corpus_gate.py` reconciles against `brain_image_corpus.py`. ELEMENTS/SCREENED remain the
letter-substitution census; their first field is a human label, not a verbatim string, which
is why DRAWN had to exist. Section A below is DELIBERATELY unchanged: it still counts the 22
elements it always counted, so its word totals stay comparable with what this report has
published. The five elements admitted on 2 Nov (05.25.20, 11.03.20, UBI BENE IBI PATRIA,
BREATHE, CHR) are therefore in DRAWN and in the corpus but NOT in this word census. See
REPORT 1.8.

Three corrections are applied, because the corpus was built for hashing candidates and
therefore carries some canvas elements more than once. Counting it raw would inflate the
census:

  1. ONE ENTRY PER CANVAS ELEMENT. CENSUS_MISC repeats elements HEADLINE already holds --
     "I can't BREATHE" vs "I CAN NOT BREATHE" are two transcriptions of ONE painted
     element (brain_image_corpus.py says so at line 113), as are "ONLY real BITCOIN",
     "PAY FOR THE FUTURE." and "THIS IS THE FIRST PREDICTION.". Each element is counted once,
     under the transcription named in ELEMENT_SOURCE below.
  2. LONGEST FORM OF THE RUSSIAN LINE ONLY. RUSSIAN carries the right-edge inscription three
     times, truncated before the unreadable glyph X, so the corpus could avoid containing a
     string nobody can read. Those truncations are prefixes of one line, not three lines.
  3. CANVAS TEXT ONLY. LATIN_MOTTOS carries two phrases that are NOT painted: "Esse quam
     videri" (the canonical phrase the niger line plays on) and "Felix qui potuit rerum
     cognoscere causas" (the full Virgil line whose tail the ring quotes). Both are reference
     strings for a solver to try. They are excluded.

COVERAGE WARNING, section B. The micro-text filling the big letters was never fully
transcribed. census_crops.py screens the whitepaper caption (~115 chars) and the 13th
Amendment copy (~179 chars) as blocks because at 5-8 px "a letter-sized object would be
unidentifiable". What section B counts is only the two fragments the census did transcribe:
the E-of-BRAVE text (REPORT 1.4) and the WHITEPAPER constant. Section B is therefore a sample,
not a census, and its totals are a floor. bitcoin.txt in the solver directory is the
whitepaper DOWNLOADED from bitcoin.org (note.txt: wget + pdftotext), not a reading of the
canvas, so it is deliberately not used here -- substituting it would invent counts for text
nobody read off the image.
"""
import os, re, sys, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brain_image_corpus as C

WORD = re.compile(r"[^\W\d_]+", re.UNICODE)
BIP39 = C.bip39_words() if callable(getattr(C, "bip39_words", None)) else set()

# ---------------------------------------------------------------- section A: display text
# (element label, text, source constant) -- one entry per painted element.
ELEMENT_SOURCE = [
    # the slogan transcription (slogan_lines.py via HEADLINE) covers these elements:
    ("FIND THE SEED PHRASE / IN THE THIS PICTURE", "FIND THE SEED PHRASE IN THE THIS PICTURE", "HEADLINE"),
    ("statue base caption",                        "Order and stability",                      "HEADLINE"),
    ("COVID sign",                                 "COVID IS A HOAX IS THE KILLER",            "HEADLINE"),
    ("I CAN NOT BREATHE",                          "I CAN NOT BREATHE",                        "HEADLINE"),
    ("BLACK LIVES MATTER ... NOT ONE MORE",         C.BLOCK,                                   "HEADLINE/BLOCK"),
    ("WELCOME TO THE / BRAVE / NEW WORLD",         "WELCOME TO THE BRAVE NEW WORLD",           "HEADLINE"),
    ("ONLY real BITCOIN / PAY FOR THE FUTURE. / THIS IS THE FIRST PREDICTION.",
     "ONLY REAL BITCOIN PAY FOR THE FUTURE THIS IS THE FIRST PREDICTION",                      "HEADLINE"),
    ("FUCK THIS SHIT",                             "FUCK THIS SHIT",                           "HEADLINE"),
    # elements HEADLINE does not cover:
    ("STOP (Liberty, O -> fist)",                  "STOP",                                     "census_crops ELEMENTS"),
    ("BLM (card)",                                 "BLM",                                      "CENSUS_MISC"),
    (".VS. (ambigram)",                            ".VS.",                                     "CENSUS_MISC"),
    ("clock hand (minute)",                        "TOWER",                                    "CENSUS_MISC"),
    ("clock hand (second)",                        "MOON",                                     "CENSUS_MISC"),
    ("vial label",                                 "CVD19",                                    "CENSUS_MISC"),
    ("seal ring (mirror-written)",                 "RERUM COGNOSCERE CAUSAS",                  "LATIN_MOTTOS"),
    ("pyramid base",                               "FIAT JUSTITIA ET PEREAT MUNDUS",           "LATIN_MOTTOS"),
    ("bottom Latin line",                          "Esse quam niger es, sic dixit caccabus ollae", "LATIN_MOTTOS"),
    ("13th Amendment copy",                         C.AMENDMENT,                               "AMENDMENT"),
    ("clock caption (rune)",                       "Сумма двух чисел",                         "RUSSIAN"),
    ("right-edge line (rune), longest transcribed form",
     "здесь зашифрованы биткоины на чёрный день номер",                                        "RUSSIAN"),
    ("rune fragment",                              "Я надеюсь",                                "RUSSIAN"),
    ("rune fragment",                              "будут присылать",                          "RUSSIAN"),
]
# Not words: recorded for completeness, excluded from the word tables.
NON_WORD = [("target address (letters of 34 chars)", C.TARGET_ADDR), ("dates", "1865 / 2020 / 1865-202?")]

# ---------------------------------------------------------------- section B: micro-text
MICRO_SOURCE = [
    ("E of BRAVE (REPORT 1.4), as transcribed incl. the typo `introdue`", C.MICROTEXT, "MICROTEXT"),
    ("whitepaper micro-text fragment",                                   C.WHITEPAPER, "WHITEPAPER"),
]


def count(entries):
    c = collections.Counter()
    for _, text, _ in entries:
        c.update(w.lower() for w in WORD.findall(text))
    return c


def table(c):
    return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))


def mark(w):
    return "BIP39" if w in BIP39 else ""


A, B = count(ELEMENT_SOURCE), count(MICRO_SOURCE)

with open("word_census.tsv", "w") as f:
    f.write("# Word census of the master image, sha256 d0b04378f75d63997b8034ec2ef1bdd108178e4546de78237bd35abf4189a782\n")
    f.write("# Aggregated from the existing census; no pixels read. See word_census.py for the three\n")
    f.write("# de-duplication rules and the section B coverage warning (B is a SAMPLE, not a census).\n")
    f.write("section\tword\tcount\tbip39\n")
    for name, c in (("A_display", A), ("B_microtext", B)):
        for w, n in table(c):
            f.write(f"{name}\t{w}\t{n}\t{mark(w)}\n")
    f.write("\n# elements counted, section A (one line per painted element)\n")
    for label, text, src in ELEMENT_SOURCE:
        f.write(f"#   {label}\t[{src}]\t{len(WORD.findall(text))} words\n")
    f.write("# elements counted, section B\n")
    for label, text, src in MICRO_SOURCE:
        f.write(f"#   {label}\t[{src}]\t{len(WORD.findall(text))} words\n")
    f.write("# not words, excluded from the tables\n")
    for label, text in NON_WORD:
        f.write(f"#   {label}\t{text}\n")

for name, c in (("A. DISPLAY TEXT", A), ("B. WHITEPAPER MICRO-TEXT (sample)", B)):
    once = [w for w, n in c.items() if n == 1]
    print(f"\n== {name}: {sum(c.values())} words, {len(c)} distinct, "
          f"{sum(1 for w in c if w in BIP39)} distinct are BIP39, {len(once)} appear exactly once "
          f"({sum(1 for w in once if w in BIP39)} of those BIP39)")
    for w, n in table(c):
        print(f"   {n:3d}  {w:<14s} {mark(w)}")

both = sorted(set(A) & set(B))
print(f"\n== in BOTH sections: {len(both)}")
for w in both:
    print(f"   {w:<14s} A={A[w]:<3d} B={B[w]:<3d} {mark(w)}")
print(f"\nwritten: word_census.tsv")

"""Load the puzzle image as float32 greyscale -- and only the exact file measured.

Every number in the image-measurement scripts is a property of one specific PNG
(md5 7710323461a924987eb35c77055e59f6, 1600x1200 RGBA). A re-encoded or resized
copy would change them silently, so a mismatch stops the run instead.

Lookup: $BLM_IMAGE, else 0.2-btc-puzzle.png in the cwd, next to this file, or
one directory up.
"""
import hashlib
import os

import numpy as np
from PIL import Image

MD5 = "7710323461a924987eb35c77055e59f6"
NAME = "0.2-btc-puzzle.png"


def image_path():
    env = os.environ.get("BLM_IMAGE")
    if env:
        return env
    here = os.path.dirname(os.path.abspath(__file__))
    for d in (os.getcwd(), here, os.path.dirname(here)):
        p = os.path.join(d, NAME)
        if os.path.exists(p):
            return p
    raise SystemExit("cannot find %s; set BLM_IMAGE=/path/to/it" % NAME)


def load_gray():
    p = image_path()
    with open(p, "rb") as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    if md5 != MD5:
        raise SystemExit("%s has md5 %s, expected %s: these measurements are for that exact file"
                         % (p, md5, MD5))
    return np.asarray(Image.open(p).convert("L")).astype(np.float32)

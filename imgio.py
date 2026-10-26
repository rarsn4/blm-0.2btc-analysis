"""Load the puzzle image as float32 greyscale -- and only the exact file measured.

Every number in the image-measurement scripts is a property of one specific PNG
(sha256 d0b04378f75d63997b8034ec2ef1bdd108178e4546de78237bd35abf4189a782, 1600x1200 RGBA,
the file served at i.redd.it/n1x7g8ceaur51.png). A re-encoded, resized or overlaid copy
would change them silently, so image_path() itself refuses any other file: every caller,
including those that open the path directly, gets only the master.

Lookup: $BLM_IMAGE, else 0.2-btc-puzzle.png in the cwd, next to this file, or
one directory up.
"""
import hashlib
import os

import numpy as np
from PIL import Image

SHA256 = "d0b04378f75d63997b8034ec2ef1bdd108178e4546de78237bd35abf4189a782"
NAME = "0.2-btc-puzzle.png"


def verified(p):
    with open(p, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    if h != SHA256:
        raise SystemExit("%s has sha256 %s, expected %s: these measurements are for that exact file"
                         % (p, h, SHA256))
    return p


def image_path():
    env = os.environ.get("BLM_IMAGE")
    if env:
        return verified(env)
    here = os.path.dirname(os.path.abspath(__file__))
    for d in (os.getcwd(), here, os.path.dirname(here)):
        p = os.path.join(d, NAME)
        if os.path.exists(p):
            return verified(p)
    raise SystemExit("cannot find %s; set BLM_IMAGE=/path/to/it" % NAME)


def load_gray():
    return np.asarray(Image.open(image_path()).convert("L")).astype(np.float32)

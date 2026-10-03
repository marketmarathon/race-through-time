"""RTT-003 (IQ-10): turn the downloaded Commons originals into bar icons.

    python scripts/rtt003_prepare_pictures.py PRIVATE/assets/rtt-003

Reads PRIVATE/assets/rtt-003/manifest.csv and originals/, writes PRIVATE/assets/rtt-003/icons/<id>.png
(RGBA, background transparent, trimmed to the console, longest side at most 480 px) and
icons/manifest.csv (icon SHA-256, the original's SHA-1 and SHA-256, what was done). The pictures
themselves live only in the private repo (DEC-006, DEC-060); this script is code only.

What is done to each picture (no picture is swapped or retouched):
  - Evan-Amos photographs on plain white: the white background connected to the picture's edge is
    made transparent (flood fill on near-white, then a 1 px soft edge). White parts INSIDE the
    console are kept, because only background connected to the border is removed.
  - Files that are already transparent (PNG with alpha): kept as they are.
  - Xbox Series X|S (CC BY 2.0, Ian Hughes): the console is cut out of the room along a hand-traced
    six-point outline of the box (checked against the photo at 2x zoom at every corner and edge,
    2 Oct 2026); the controller, which the photo's bottom edge cuts off, is left out. The credit
    line says "background removed".
Needs Pillow, numpy and OpenCV (opencv-python-headless).
"""
import csv
import hashlib
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageOps

MAX_SIDE = 480
# Hand-traced outline of the Xbox Series X in the EXIF-rotated original (3024 x 4032), in px.
XBOX_SERIES_OUTLINE = [(84, 62), (578, 60), (799, 137), (624, 1050), (199, 1121), (96, 152)]
XBOX_SERIES_OUTLINE = [(x / 0.4 + 600, y / 0.4 + 150) for x, y in XBOX_SERIES_OUTLINE]


def sha(path, algo):
    h = hashlib.new(algo)
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def polygon_cutout(im, pts, ss=4):
    w, h = im.size
    m = Image.new('L', (w * ss, h * ss), 0)
    ImageDraw.Draw(m).polygon([(x * ss, y * ss) for x, y in pts], fill=255)
    m = m.resize((w, h), Image.LANCZOS)               # anti-aliased edge
    out = im.convert('RGBA'); out.putalpha(m)
    return out, 'cut out along a hand-traced outline of the console (controller and room removed)'


# Consoles whose cables or controllers enclose patches of the white background (checked by eye on
# the contact sheet, 2 Oct 2026); for these, enclosed pure-white patches are background too. Not used
# for white consoles (Dreamcast, Wii, Xbox 360, PlayStation 5), whose own surfaces are pure white.
HOLES = {'master_system', 'mega_drive', 'nes', 'snes', 'nintendo_64', 'gamecube', 'xbox', 'playstation_2',
         'playstation_4', 'xbox_one', 'nintendo_switch', 'saturn', 'atari_2600'}


def white_cutout(im, holes=False, thr=250, min_hole=0.0015):
    """Evan-Amos photographs sit on pure white (255). Background = pixels with every channel >= thr
    connected to the picture's border (4-connected); with holes, also enclosed pure-white patches of
    at least min_hole of the picture. Then a 1 px soft edge."""
    rgb = np.asarray(im.convert('RGB'))
    h, w, _ = rgb.shape
    white = (rgb.min(axis=2) >= thr).astype(np.uint8)
    n, lab = cv2.connectedComponents(white, connectivity=4)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    keep = set(border)
    if holes:
        counts = np.bincount(lab.ravel())
        keep |= {k for k in range(1, n) if counts[k] >= min_hole * h * w}
    bg = np.isin(lab, list(keep)).astype(np.uint8)
    bg = cv2.morphologyEx(bg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    fg = cv2.GaussianBlur((1 - bg).astype(np.float32), (3, 3), 0.8)
    out = im.convert('RGBA')
    out.putalpha(Image.fromarray((fg * 255).round().astype(np.uint8)))
    return out, 'white background connected to the edge made transparent' + ('; white patches enclosed by cables too' if holes else '')


def trim_and_scale(im):
    a = np.asarray(im.split()[-1])
    ys, xs = np.where(a > 8)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    s = min(1.0, MAX_SIDE / max(im.size))
    if s < 1:
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    return im


def main(root):
    rows = [r for r in csv.DictReader(open(os.path.join(root, 'manifest.csv'), encoding='utf-8')) if r['kind'] == 'console']
    os.makedirs(os.path.join(root, 'icons'), exist_ok=True)
    out = []
    for r in rows:
        src = os.path.join(root, r['file'])
        assert sha(src, 'sha256') == r['sha256'], r['id'] + ': original SHA-256 does not match the manifest'
        im = ImageOps.exif_transpose(Image.open(src))
        if r['id'] == 'xbox_series':
            im, how = polygon_cutout(im.convert('RGB'), XBOX_SERIES_OUTLINE)
        elif im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
            im = im.convert('RGBA')
            a = np.asarray(im.split()[-1])
            if a.min() < 250:
                how = 'already transparent; kept'
            else:
                im, how = white_cutout(im, r['id'] in HOLES)
        else:
            im, how = white_cutout(im, r['id'] in HOLES)
        im = trim_and_scale(im)
        dst = os.path.join(root, 'icons', r['id'] + '.png')
        im.save(dst, optimize=True)
        out.append({'id': r['id'], 'icon': 'icons/' + r['id'] + '.png', 'width': im.width, 'height': im.height,
                    'aspect': f'{im.width / im.height:.2f}', 'icon_sha256': sha(dst, 'sha256'),
                    'original': r['file'], 'original_sha1': r['sha1'], 'original_sha256': r['sha256'],
                    'licence': r['licence'], 'credit_line': r['credit_line'], 'done': how + f'; trimmed; longest side <= {MAX_SIDE} px'})
        print(f"{r['id']}: {im.width}x{im.height} {how}")
    with open(os.path.join(root, 'icons', 'manifest.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)


if __name__ == '__main__':
    main(sys.argv[1])

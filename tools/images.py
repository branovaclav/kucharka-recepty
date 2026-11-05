#!/usr/bin/env python3
"""Prepare photos for a recipe (run by a human/agent when adding or replacing photos; needs Pillow).

  python3 tools/images.py <slug> [--force]

Reads content/img/originals/<file> (the photo as downloaded from the credited source) for every image the recipe uses
(front matter hero.image + body ![…](img/…)) and writes:
  content/img/<file>          web-ready copy that build.py embeds as base64 (hero: ≤720 px q86, step photos: ≤720 px q70)
  images/thumbs/<slug>.jpg    index card 480×360 centre crop q74 (from the hero)
  images/covers/<slug>.jpg    Notion page cover ≤1200 px q80 (from the hero)
Existing outputs are kept unless --force (so the build stays byte-stable). The GitHub Action never runs this.
"""
import os, re, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recipe_md import split
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def save(src, out, width, q, force):
    if os.path.exists(out) and not force: return
    im = Image.open(src).convert('RGB')
    if im.width > width: im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    os.makedirs(os.path.dirname(out), exist_ok=True); im.save(out, 'JPEG', quality=q, optimize=True, progressive=True); print('wrote', out)

def thumb(src, out, force, w=480, h=360):
    if os.path.exists(out) and not force: return
    im = Image.open(src).convert('RGB'); r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    os.makedirs(os.path.dirname(out), exist_ok=True); im.crop((l, t, l + w, t + h)).save(out, 'JPEG', quality=74, optimize=True, progressive=True); print('wrote', out)

def run(slug, force=False):
    fm, body = split(open(os.path.join(ROOT, 'content', slug + '.md'), encoding='utf-8').read())
    C = os.path.join(ROOT, 'content'); orig = lambda rel: os.path.join(C, 'img', 'originals', os.path.basename(rel))
    hero = fm['hero']['image']
    save(orig(hero), os.path.join(C, hero), 720, 86, force)
    thumb(orig(hero), os.path.join(ROOT, 'images', 'thumbs', slug + '.jpg'), force)
    save(orig(hero), os.path.join(ROOT, 'images', 'covers', slug + '.jpg'), 1200, 80, force)
    for rel in re.findall(r'!\[[^\]]*\]\((img/[^)\s]+)', body): save(orig(rel), os.path.join(C, rel), 720, 70, force)

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    for s in a or sorted(f[:-3] for f in os.listdir(os.path.join(ROOT, 'content')) if f.endswith('.md')): run(s, '--force' in sys.argv)

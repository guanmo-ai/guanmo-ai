"""svgkit — tiny toolkit for building GitHub-safe SVGs.

Why: GitHub renders README SVGs through <img>, so the SVG cannot load
external fonts/images or run JS. Everything here is self-contained:
  * text is shaped with HarfBuzz and converted to outlined glyph <path>s
    (defined once in <defs>, reused with <use>), so it looks identical on
    every machine, with no font dependency;
  * raster images are embedded as base64 JPEG/PNG;
  * motion uses CSS @keyframes inside the SVG (GitHub allows it), and
    `prefers-reduced-motion` turns it off.
"""
from __future__ import annotations

import base64
import io
import os
from dataclasses import dataclass, field

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from PIL import Image


def _n(v: float, nd: int = 1) -> str:
    """Compact number formatting."""
    s = f"{v:.{nd}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# --------------------------------------------------------------------------- fonts
class Font:
    """One font file at one weight (variable fonts are pinned to `wght`)."""

    def __init__(self, key: str, path: str, wght: float | None = None, index: int = 0):
        self.key = key
        self.path = path
        self.tt = TTFont(path, fontNumber=index, lazy=True)
        self.upm = self.tt["head"].unitsPerEm
        loc = {"wght": wght} if (wght is not None and "fvar" in self.tt) else None
        self.gs = self.tt.getGlyphSet(location=loc) if loc else self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.cmap = self.tt.getBestCmap()
        face = hb.Face(hb.Blob.from_file_path(path), index)
        self.hb = hb.Font(face)
        if loc:
            self.hb.set_variations(loc)
        self._paths: dict[int, str] = {}

    def has(self, ch: str) -> bool:
        return ord(ch) in self.cmap

    def path_d(self, gid: int) -> str:
        if gid not in self._paths:
            pen = SVGPathPen(self.gs, ntos=lambda v: "%d" % round(v))
            self.gs[self.order[gid]].draw(pen)
            self._paths[gid] = pen.getCommands()
        return self._paths[gid]

    def shape(self, text: str, features: dict | None = None):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, features or {"kern": True, "liga": True})
        return [
            (i.codepoint, p.x_advance, p.x_offset, p.y_offset)
            for i, p in zip(buf.glyph_infos, buf.glyph_positions)
        ]


@dataclass
class Style:
    fonts: list  # [primary, fallback, ...]
    size: float
    fill: str = "#fff"
    tracking: float = 0.0  # em
    features: dict | None = None
    opacity: float | None = None

    def but(self, **kw) -> "Style":
        d = dict(self.__dict__)
        d.update(kw)
        return Style(**d)


def _runs(text: str, fonts: list):
    """Split text into runs by the first font that covers each char."""
    runs: list[list] = []
    for ch in text:
        f = next((f for f in fonts if f.has(ch)), fonts[0])
        if ch in " \u00a0\u3000" and runs:
            f = runs[-1][0]
        if runs and runs[-1][0] is f:
            runs[-1][1] += ch
        else:
            runs.append([f, ch])
    return runs


def layout(text: str, st: Style):
    """Return (items, width). items = [(font, gid, x_px, y_units, scale)]."""
    items = []
    pen = 0.0
    track = st.tracking * st.size
    for f, chunk in _runs(text, st.fonts):
        sc = st.size / f.upm
        for gid, adv, xo, yo in f.shape(chunk, st.features):
            items.append((f, gid, pen + xo * sc, yo, sc))
            pen += adv * sc + track
    width = pen - (track if items else 0)
    return items, width


def measure(text: str, st: Style) -> float:
    return layout(text, st)[1]


# --------------------------------------------------------------------------- doc
@dataclass
class Doc:
    w: int
    h: int
    title: str = ""
    css: list = field(default_factory=list)
    defs: list = field(default_factory=list)
    body: list = field(default_factory=list)
    _glyphs: dict = field(default_factory=dict)
    _uid: int = 0

    def uid(self, p="i") -> str:
        self._uid += 1
        return f"{p}{self._uid}"

    def add(self, s: str):
        self.body.append(s)
        return s

    def glyph_id(self, f: Font, gid: int) -> str | None:
        k = (f.key, gid)
        if k not in self._glyphs:
            d = f.path_d(gid)
            self._glyphs[k] = (f"{f.key}{gid:x}", d) if d else (None, None)
        return self._glyphs[k][0]

    def text(self, s: str, st: Style, x: float, y: float, anchor: str = "start",
             cls: str | None = None, attrs: str = "") -> str:
        """Outlined text; returns the SVG string (not added). y = baseline."""
        items, width = layout(s, st)
        x0 = x - (width if anchor == "end" else width / 2 if anchor == "middle" else 0)
        groups: list[list] = []
        for f, gid, xp, yo, sc in items:
            gidref = self.glyph_id(f, gid)
            if not gidref:
                continue
            if not groups or groups[-1][0] is not f:
                groups.append([f, sc, []])
            ux = xp / sc
            groups[-1][2].append(f'<use href="#{gidref}" x="{_n(ux, 0)}"' + (f' y="{yo}"' if yo else "") + "/>")
        inner = "".join(
            f'<g transform="translate({_n(x0, 2)} {_n(y, 2)}) scale({_n(sc, 5)} {_n(-sc, 5)})">{"".join(u)}</g>'
            for f, sc, u in groups
        )
        a = f' fill="{st.fill}"'
        if st.opacity is not None:
            a += f' opacity="{st.opacity}"'
        if cls:
            a += f' class="{cls}"'
        if attrs:
            a += " " + attrs
        return f"<g{a}>{inner}</g>"

    def render(self) -> str:
        gl = "".join(f'<path id="{i}" d="{d}"/>' for i, d in self._glyphs.values() if i)
        css = "".join(self.css) + "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
        t = self.title.replace("&", "&amp;").replace("<", "&lt;")
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" role="img" aria-labelledby="t">'
            f'<title id="t">{t}</title><style>{css}</style>'
            f'<defs>{gl}{"".join(self.defs)}</defs>{"".join(self.body)}</svg>'
        )

    def save(self, path: str) -> int:
        data = self.render()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(data)
        return len(data.encode())


# --------------------------------------------------------------------------- images
def cover(im: Image.Image, w: int, h: int, focus=(0.5, 0.5)) -> Image.Image:
    """Crop-to-fill like CSS object-fit: cover."""
    im = im.convert("RGB")
    sw, sh = im.size
    s = max(w / sw, h / sh)
    nw, nh = round(sw * s), round(sh * s)
    im = im.resize((nw, nh), Image.LANCZOS)
    left = round((nw - w) * focus[0])
    top = round((nh - h) * focus[1])
    return im.crop((left, top, left + w, top + h))


def jpeg_uri(im: Image.Image, quality: int = 80) -> str:
    b = io.BytesIO()
    im.convert("RGB").save(b, "JPEG", quality=quality, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def png_uri(im: Image.Image) -> str:
    b = io.BytesIO()
    im.save(b, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()


def grain_tile(size: int = 128, strength: int = 34, seed: int = 7) -> Image.Image:
    """Transparent film-grain tile (light + dark specks)."""
    import random

    rnd = random.Random(seed)
    im = Image.new("LA", (size, size))
    px = im.load()
    for yy in range(size):
        for xx in range(size):
            r = rnd.random()
            if r < 0.5:
                px[xx, yy] = (255 if r < 0.25 else 0, int(rnd.random() * strength))
            else:
                px[xx, yy] = (128, 0)
    return im

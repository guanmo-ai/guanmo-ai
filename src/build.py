#!/usr/bin/env python3
"""Build every asset of the GUANMO cinematic GitHub profile.

    python3 src/build.py            # build assets/*.svg + README.md

All copy / numbers / links live in src/config.json.
"""
from __future__ import annotations

import argparse
import json
from math import ceil, cos, sin, pi
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent / "lib"))
from svgkit import Doc, Font, Style, cover, jpeg_uri, measure, _n  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
IMG = SRC / "images"
FONTS = ROOT / "fonts"
OUT = ROOT / "assets"

# ----------------------------------------------------------------- palette
INK = "#050607"       # frame black
IVORY = "#EDE6D6"     # title cream
MUTE = "#B4AC9C"      # secondary text on dark (≈ 8:1 on INK)
DIM = "#7E786C"       # tertiary text on dark (≈ 4.6:1 on INK)
GOLD = "#E8B867"      # horizon gold (sampled from the hero frame)
RED = "#E5412F"       # REC / documentary accent
W = 1280

# ----------------------------------------------------------------- fonts
def load_fonts():
    need = ["NotoSerifSC-VF.ttf", "NotoSansSC-VF.ttf", "Jost-VF.ttf", "JetBrainsMono-VF.ttf",
            "InstrumentSerif-Regular.ttf", "InstrumentSerif-Italic.ttf"]
    missing = [n for n in need if not (FONTS / n).exists()]
    if missing:
        sys.exit("缺少字体 / missing fonts: " + ", ".join(missing) + "\n→ 先运行 bash scripts/fetch_fonts.sh")
    f = {}
    serif = FONTS / "NotoSerifSC-VF.ttf"
    sans = FONTS / "NotoSansSC-VF.ttf"
    f["serif_black"] = Font("a", str(serif), 900)
    f["serif_bold"] = Font("b", str(serif), 700)
    f["serif_med"] = Font("c", str(serif), 500)
    f["sans"] = Font("d", str(sans), 400)
    f["sans_med"] = Font("e", str(sans), 500)
    f["sans_bold"] = Font("f", str(sans), 700)
    f["sans_semi"] = Font("v", str(sans), 600)
    f["jost_light"] = Font("g", str(FONTS / "Jost-VF.ttf"), 300)
    f["jost"] = Font("h", str(FONTS / "Jost-VF.ttf"), 400)
    f["jost_semi"] = Font("k", str(FONTS / "Jost-VF.ttf"), 600)
    f["mono"] = Font("m", str(FONTS / "JetBrainsMono-VF.ttf"), 400)
    f["mono_b"] = Font("n", str(FONTS / "JetBrainsMono-VF.ttf"), 600)
    f["iserif"] = Font("p", str(FONTS / "InstrumentSerif-Regular.ttf"))
    f["iserif_i"] = Font("q", str(FONTS / "InstrumentSerif-Italic.ttf"))
    return f


F = load_fonts()


def S(name, size, fill=IVORY, tracking=0.0, fallback="sans", **kw):
    fonts = [F[name]] + ([F[fallback]] if fallback and fallback != name else [])
    return Style(fonts, size, fill, tracking, **kw)


def corners(x, y, w, h, arm=22, stroke=IVORY, sw=1.5, op=0.55):
    p = (
        f"M{x} {y+arm}V{y}H{x+arm}M{x+w-arm} {y}H{x+w}V{y+arm}"
        f"M{x+w} {y+h-arm}V{y+h}H{x+w-arm}M{x+arm} {y+h}H{x}V{y+h-arm}"
    )
    return f'<path d="{p}" fill="none" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>'


# ================================================================= HERO
def build_hero(cfg):
    H, TOP, IH = 624, 40, 544
    BOT = TOP + IH
    d = Doc(W, H, title=f"{cfg['name_zh']} {cfg['name_en']} · {cfg['tagline_zh']} {cfg['tagline_en']}")
    im = cover(Image.open(IMG / "hero.jpg"), 1600, 680)
    d.defs.append(
        f'<clipPath id="fr"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
        f'<clipPath id="pic"><rect y="{TOP}" width="{W}" height="{IH}"/></clipPath>'
        '<linearGradient id="shL" x1="0" x2="1" y1="0" y2="0">'
        '<stop offset="0" stop-color="#02070A" stop-opacity=".9"/><stop offset=".34" stop-color="#02070A" stop-opacity=".62"/>'
        '<stop offset=".62" stop-color="#02070A" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="shB" x1="0" x2="0" y1="0" y2="1">'
        '<stop offset="0" stop-color="#000" stop-opacity=".35"/><stop offset=".22" stop-color="#000" stop-opacity="0"/>'
        '<stop offset=".7" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></linearGradient>'
        '<radialGradient id="vig" cx=".55" cy=".5" r=".8"><stop offset=".55" stop-color="#000" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#000" stop-opacity=".6"/></radialGradient>'
        f'<linearGradient id="rule" x1="0" x2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity="0"/>'
        f'<stop offset=".05" stop-color="{GOLD}" stop-opacity=".95"/><stop offset=".45" stop-color="{GOLD}" stop-opacity=".55"/>'
        f'<stop offset=".62" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="flare" x1="0" x2="1"><stop offset="0" stop-color="#FFE3A8" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#FFF6E2"/><stop offset="1" stop-color="#FFE3A8" stop-opacity="0"/></linearGradient>'
        f'<radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".9"/>'
        f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="leak" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FF9A4A" stop-opacity=".55"/>'
        '<stop offset="1" stop-color="#FF6A2A" stop-opacity="0"/></radialGradient>'
        '<filter id="blur6" x="-20%" y="-400%" width="140%" height="900%"><feGaussianBlur stdDeviation="3"/></filter>'
    )
    d.css.append(
        # slow push-in toward the astronaut
        "@keyframes kb{from{transform:scale(1)}to{transform:scale(1.06)}}"
        ".kb{transform-box:fill-box;transform-origin:72% 42%;animation:kb 32s ease-in-out infinite alternate}"
        # Titles stay readable from the first paint.
        "@keyframes ign{0%,25%{transform:scaleX(0)}100%{transform:scaleX(1)}}"
        ".ign{transform-box:fill-box;transform-origin:left center;animation:ign 2.4s cubic-bezier(.6,0,.2,1) both}"
        # anamorphic flare sweeping along the horizon
        "@keyframes fl{0%{transform:translateX(0);opacity:0}6%{opacity:1}38%{transform:translateX(1800px);opacity:1}39%,100%{transform:translateX(1800px);opacity:0}}"
        ".fl{animation:fl 9s cubic-bezier(.55,0,.35,1) 2.2s infinite both;mix-blend-mode:screen}"
        "@keyframes br{0%,100%{opacity:.35}50%{opacity:.85}}.br{animation:br 5s ease-in-out infinite}"
        "@keyframes lk{0%,100%{opacity:0;transform:translateX(0)}50%{opacity:1;transform:translateX(-160px)}}"
        ".lk{animation:lk 14s ease-in-out infinite;mix-blend-mode:screen}"
        "@keyframes rec{0%,55%{opacity:1}56%,100%{opacity:.18}}.rec{animation:rec 1.2s steps(1) infinite}"
        # autofocus lock-on
        "@keyframes af{0%,40%{opacity:0;transform:scale(1.35)}55%{opacity:1;transform:scale(1)}62%{opacity:.25}70%,100%{opacity:1;transform:scale(1)}}"
        ".af{transform-box:fill-box;transform-origin:center;animation:af 3.4s ease-out both}"
    )
    b = d.add
    b('<g clip-path="url(#fr)">')
    b(f'<rect width="{W}" height="{H}" fill="{INK}"/>')
    b(f'<g clip-path="url(#pic)"><g class="kb"><image href="{jpeg_uri(im, 80)}" x="0" y="{TOP}" width="{W}" height="{IH}" preserveAspectRatio="xMidYMid slice"/></g>')
    b(f'<g class="lk"><ellipse cx="1330" cy="{TOP+10}" rx="300" ry="190" fill="url(#leak)" opacity=".7"/></g>')
    b(f'<rect y="{TOP}" width="{W}" height="{IH}" fill="url(#shL)"/><rect y="{TOP}" width="{W}" height="{IH}" fill="url(#shB)"/>')
    b(f'<rect y="{TOP}" width="{W}" height="{IH}" fill="url(#vig)"/>')
    hz = 287
    b(f'<g class="br"><ellipse cx="1010" cy="{hz}" rx="330" ry="9" fill="url(#glow)"/></g>')
    b(f'<g class="ign"><rect x="0" y="{hz-0.8}" width="{W}" height="1.6" fill="url(#rule)"/></g>')
    b(f'<g class="fl"><rect x="-460" y="{hz-3}" width="460" height="6" rx="3" fill="url(#flare)" filter="url(#blur6)"/>'
      f'<rect x="-300" y="{hz-0.9}" width="300" height="1.8" fill="url(#flare)"/></g>')
    b('</g>')
    # viewfinder + autofocus
    b(corners(28, TOP + 22, W - 56, IH - 44, arm=26, op=0.5))
    fx, fy, fw, fh = 852, 206, 142, 128
    b(f'<g class="af">{corners(fx, fy, fw, fh, arm=16, stroke=GOLD, sw=1.6, op=0.95)}'
      + d.text("AF·C", S("mono_b", 12, GOLD, 0.12), fx, fy - 9) + "</g>")
    # letterbox bars
    b(f'<rect width="{W}" height="{TOP}" fill="{INK}"/><rect y="{BOT}" width="{W}" height="{H-BOT}" fill="{INK}"/>')
    hud = S("mono", 13, MUTE, 0.14)
    b(d.text(f"{cfg['name_zh']} {cfg['name_en']}", hud, 28, 24.6))
    b(d.text("SELECTED PROJECTS", hud, W - 28, 24.6, anchor="end"))
    b(d.text("WATCH CLOSELY · BUILD QUIETLY", hud, 28, BOT + 24.8))
    b(d.text("AI MOTION  ·  DESIGN STYLE  ·  X GROWTH", hud, W / 2, BOT + 24.6, anchor="middle"))
    b(d.text(f"x.com/{cfg['x_handle']}", S("mono_b", 13, GOLD, 0.1), W - 28, BOT + 24.6, anchor="end"))
    # title block
    x = 72
    b(d.text(cfg["role_en"], S("mono_b", 23, GOLD, 0.2), x, 104))
    b(f'<g class="r r2">' + d.text(cfg["name_zh"], S("serif_black", 150, IVORY, 0.02, fallback=None), x - 6, 252) + "</g>")
    b(f'<g class="r r3">' + d.text(cfg["name_en"], S("jost_light", 30, IVORY, 0.78), x, 334) + "</g>")
    b(f'<g class="r r4">' + d.text(cfg["tagline_zh"], S("serif_bold", 34, IVORY, 0.04, fallback=None), x, 398) + "</g>")
    b(f'<g class="r r5">' + d.text(cfg["tagline_en"], S("iserif_i", 26, MUTE, 0.01), x, 436) + "</g>")
    b("</g>")
    return d


# ================================================================= shared card chrome
def slate(d: Doc, x, y, no, kind_zh, kind_en, accent=GOLD):
    """REEL label:  ▌REEL 01  策展长片 · FEATURE"""
    lab = S("mono_b", 14, accent, 0.28)
    t1 = d.text(f"REEL {no}", lab, x + 14, y)
    w1 = measure(f"REEL {no}", lab)
    t2 = d.text(f"{kind_zh} · {kind_en}", S("sans_med", 14, MUTE, 0.16), x + 14 + w1 + 18, y)
    return f'<rect x="{x}" y="{y-13}" width="3" height="16" fill="{accent}"/>' + t1 + t2


def frame_defs(d: Doc, H, bg):
    d.defs.append(f'<clipPath id="fr"><rect width="{W}" height="{H}" rx="18"/></clipPath>')
    d.add(f'<g clip-path="url(#fr)"><rect width="{W}" height="{H}" fill="{bg}"/>')


def frame_end(d: Doc, H):
    d.add(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="17.5" fill="none" stroke="#fff" stroke-opacity=".07"/></g>')


# ================================================================= REEL 01 · Awesome AI Motion
def build_reel_motion(cfg):
    r = cfg["reels"]["motion"]
    H, BG = 540, "#100D12"
    d = Doc(W, H, title=f"REEL 01 · {' '.join(r['title'])} — {''.join(r['lines_zh'])}")
    FW, FH, GAP, BAND = 256, 144, 12, 26
    PITCH = FW + GAP
    frames = sorted((IMG / "frames").glob("*.jpg"))
    half = len(frames) // 2
    L = PITCH * half
    holes = (f'<pattern id="sp" width="22" height="{BAND}" patternUnits="userSpaceOnUse">'
             f'<rect x="5" y="8.5" width="12" height="9" rx="2.2" fill="#D8CDB8" fill-opacity=".42"/></pattern>')
    d.defs.append(holes)
    for k, chunk in (("sA", frames[:half]), ("sB", frames[half:])):
        g = [f'<g id="{k}"><rect width="{L}" height="{FH+2*BAND}" fill="#17130F"/>'
             f'<rect width="{L}" height="{BAND}" fill="url(#sp)"/><rect y="{FH+BAND}" width="{L}" height="{BAND}" fill="url(#sp)"/>']
        for i, fp in enumerate(chunk):
            im = cover(Image.open(fp), 384, 216)
            g.append(f'<image href="{jpeg_uri(im, 70)}" x="{i*PITCH+GAP/2}" y="{BAND}" width="{FW}" height="{FH}" preserveAspectRatio="xMidYMid slice"/>')
        g.append("</g>")
        d.defs.append("".join(g))
    d.defs.append(
        f'<linearGradient id="fadeL" x1="0" x2="1"><stop offset="0" stop-color="{BG}"/><stop offset=".38" stop-color="{BG}" stop-opacity=".97"/>'
        f'<stop offset=".56" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
        f'<linearGradient id="fadeR" x1="0" x2="1"><stop offset=".86" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}" stop-opacity=".85"/></linearGradient>'
        '<radialGradient id="tealG" cx=".78" cy=".45" r=".6"><stop offset="0" stop-color="#59414C" stop-opacity=".4"/><stop offset="1" stop-color="#59414C" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="orgG" cx=".05" cy="1" r=".55"><stop offset="0" stop-color="#FF8A3D" stop-opacity=".22"/><stop offset="1" stop-color="#FF8A3D" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="beam" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFE2B0" stop-opacity=".16"/><stop offset="1" stop-color="#FFE2B0" stop-opacity="0"/></radialGradient>'
    )
    d.css.append(
        f"@keyframes mvL{{to{{transform:translateX(-{L}px)}}}}.mvL{{animation:mvL 90s linear infinite}}"
        f"@keyframes mvR{{to{{transform:translateX({L}px)}}}}.mvR{{animation:mvR 90s linear infinite}}"
        "@keyframes pls{0%,100%{opacity:1}50%{opacity:.25}}.pls{animation:pls 1.6s ease-in-out infinite}"
        "@keyframes flk{0%,100%{opacity:.0}10%{opacity:.5}12%{opacity:.15}40%{opacity:.6}70%{opacity:.3}}.flk{animation:flk 4s steps(1) infinite}"
    )
    frame_defs(d, H, BG)
    b = d.add
    b(f'<rect width="{W}" height="{H}" fill="url(#tealG)"/><rect width="{W}" height="{H}" fill="url(#orgG)"/>')
    # two counter-moving 35mm strips, tilted
    b('<g transform="rotate(-7 900 270)">')
    b(f'<g transform="translate(430 58)"><g class="mvL"><use href="#sA"/><use href="#sA" x="{L}"/></g></g>')
    b(f'<g transform="translate(430 292)"><g class="mvR"><use href="#sB" x="-{L}"/><use href="#sB"/></g></g>')
    b("</g>")
    b(f'<g class="flk" opacity=".3"><ellipse cx="930" cy="270" rx="520" ry="300" fill="url(#beam)"/></g>')
    b(f'<rect width="{W}" height="{H}" fill="url(#fadeL)"/><rect width="{W}" height="{H}" fill="url(#fadeR)"/>')
    x = 64
    b(slate(d, x, 78, "01", r["kind_zh"], r["kind_en"]))
    ttl = S("iserif", 92, IVORY, -0.005)
    b(d.text(r["title"][0], ttl, x - 3, 172))
    b(d.text(r["title"][1], ttl, x - 3, 252))
    body = S("sans", 20, MUTE, 0.02)
    b(d.text(r["lines_zh"][0], body, x, 306))
    b(d.text(r["lines_zh"][1], body, x, 338))
    # box office
    num = S("jost", 46, IVORY, 0.0)
    lab = S("sans_med", 13, MUTE, 0.12)
    cols = [(r["works"], "收录作品 · WORKS"), (r["genres"], "创作方向 · GENRES")]
    cx = x
    for i, (n, l) in enumerate(cols):
        b(d.text(n, num, cx, 424))
        b(d.text(l, lab, cx, 450))
        wcol = max(measure(n, num), measure(l, lab))
        cx += wcol + 30
        if i < len(cols) - 1:
            b(f'<rect x="{cx-15}" y="388" width="1" height="64" fill="#fff" opacity=".14"/>')
    site = r["site"].replace("https://", "").rstrip("/")
    b(d.text(f"▶  {site}", S("mono_b", 14, GOLD, 0.06), x, 502))
    # now showing tag
    tag = S("mono_b", 12, IVORY, 0.22)
    tw = measure("NOW SHOWING · 正在上映", tag)
    b(f'<rect x="{W-48-tw-30}" y="30" width="{tw+30+16}" height="30" rx="15" fill="#000" fill-opacity=".62" stroke="#fff" stroke-opacity=".14"/>')
    b(f'<circle class="pls" cx="{W-48-tw-12}" cy="45" r="4" fill="{RED}"/>')
    b(d.text("NOW SHOWING · 正在上映", tag, W - 40, 49.5, anchor="end"))
    frame_end(d, H)
    return d


# ================================================================= REEL 02 · Design Style
def build_reel_design(cfg):
    r = cfg["reels"]["design"]
    H, BG = 540, "#12100E"
    BRED, BYEL, BBLU = "#DB3A26", "#F2B419", "#1F4FA3"
    d = Doc(W, H, title=f"REEL 02 · Design Style — {r['subtitle_zh']} · {r['motto_zh']}")
    d.defs.append(
        '<filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#000" flood-opacity=".6"/></filter>'
        '<radialGradient id="warm" cx=".22" cy=".5" r=".55"><stop offset="0" stop-color="#5A3A1E" stop-opacity=".55"/><stop offset="1" stop-color="#5A3A1E" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="spot" cx=".5" cy="0" r=".9"><stop offset="0" stop-color="#FFE7C2" stop-opacity=".10"/><stop offset="1" stop-color="#FFE7C2" stop-opacity="0"/></radialGradient>'
    )
    d.css.append(
        "@keyframes f1{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}.f1{animation:f1 7s ease-in-out infinite}"
        "@keyframes f2{0%,100%{transform:translateY(0)}50%{transform:translateY(7px)}}.f2{animation:f2 7s ease-in-out infinite}"
        "@keyframes ci{0%,100%{transform:scale(1)}50%{transform:scale(.72)}}.ci{transform-box:fill-box;transform-origin:center;animation:ci 3s ease-in-out infinite}"
        "@keyframes sq{0%,20%{transform:rotate(0)}50%,100%{transform:rotate(90deg)}}.sq{transform-box:fill-box;transform-origin:center;animation:sq 3s cubic-bezier(.7,0,.3,1) infinite}"
        "@keyframes tr{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}.tr{animation:tr 3s ease-in-out .4s infinite}"
        "@keyframes nx{0%,100%{opacity:1}50%{opacity:.2}}.nx{animation:nx 1.4s ease-in-out infinite}"
        "@keyframes hl{0%,30%{transform:translateY(0)}36%,63%{transform:translateY(50px)}69%,100%{transform:translateY(0)}}"
    )
    frame_defs(d, H, BG)
    b = d.add
    b(f'<rect width="{W}" height="{H}" fill="url(#warm)"/><rect width="{W}" height="{H}" fill="url(#spot)"/>')
    # posters (their own work)
    bento = cover(Image.open(IMG / "posters" / "bento.png"), 524, 655)
    bauh = cover(Image.open(IMG / "posters" / "bauhaus.png"), 572, 715)
    b(f'<g class="f2"><g transform="rotate(6 372 262)" filter="url(#sh)"><image href="{jpeg_uri(bento, 80)}" x="{372-131}" y="{262-164}" width="262" height="328"/>'
      f'<rect x="{372-131}" y="{262-164}" width="262" height="328" fill="none" stroke="#fff" stroke-opacity=".12"/></g></g>')
    b(f'<g class="f1"><g transform="rotate(-5 236 284)" filter="url(#sh)"><image href="{jpeg_uri(bauh, 80)}" x="{236-143}" y="{284-179}" width="286" height="358"/></g></g>')
    x = 620
    b(slate(d, x, 72, "02", r["kind_zh"], r["kind_en"]))
    # bauhaus trio
    tx = W - 64
    b(f'<g class="tr"><polygon points="{tx-11},{88} {tx+11},{88} {tx},{67}" fill="{BYEL}"/></g>')
    b(f'<g class="sq"><rect x="{tx-46}" y="67" width="21" height="21" fill="{BRED}"/></g>')
    b(f'<g class="ci"><circle cx="{tx-70}" cy="77.5" r="10.5" fill="{BBLU}"/></g>')
    b(d.text(r["title"][0], S("iserif", 84, IVORY, -0.005), x - 3, 158))
    b(d.text(r["subtitle_zh"], S("serif_bold", 30, IVORY, 0.06, fallback=None), x, 214))
    b(d.text(r["motto_zh"], S("sans_med", 18, GOLD, 0.06), x, 256))
    b(d.text(r["line_zh"], S("sans", 16, MUTE, 0.02), x, 283))
    # episode guide
    gy = 326
    b(d.text("EPISODE GUIDE · 节目单", S("mono_b", 12, DIM, 0.24), x, gy))
    b(f'<rect x="{x}" y="{gy+12}" width="{W-64-x}" height="1" fill="#fff" opacity=".16"/>')
    rowh = 46
    for i, ep in enumerate(r["episodes"]):
        y = gy + 44 + i * rowh
        live = ep["state"] == "live"
        b(d.text(ep["no"], S("mono_b", 15, GOLD if live else DIM, 0.08), x, y))
        b(d.text(ep["name"], S("sans_med", 20, IVORY if live else MUTE, 0.02), x + 76, y))
        b(d.text(ep["era"], S("mono", 14, MUTE if live else DIM, 0.04), x + 340, y))
        if live:
            b(d.text("▶ 已上映", S("sans_med", 15, IVORY, 0.06), W - 64, y, anchor="end"))
        else:
            ww = measure("NEXT · 计划中", S("sans_med", 15, IVORY, 0.06))
            b(f'<circle class="nx" cx="{W-64-ww-12}" cy="{y-5}" r="4.5" fill="{BRED}"/>')
            b(d.text("NEXT · 计划中", S("sans_med", 15, MUTE, 0.06), W - 64, y, anchor="end"))
        b(f'<rect x="{x}" y="{y+16}" width="{W-64-x}" height="1" fill="#fff" opacity=".08"/>')
    site = r["site"].replace("https://", "").rstrip("/")
    b(d.text(f"▶  {site}", S("mono_b", 14, GOLD, 0.06), x, 512))
    frame_end(d, H)
    return d


# ================================================================= REEL 03 · Awesome X Growth
def build_reel_xgrowth(cfg):
    r = cfg["reels"]["xgrowth"]
    H, BG = 540, "#0B0B0B"
    d = Doc(W, H, title=f"REEL 03 · {' '.join(r['title'])} — {''.join(r['lines_zh'])}")
    d.defs.append(
        '<radialGradient id="lamp" cx=".74" cy=".42" r=".55"><stop offset="0" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
    )
    cw, chh, gap = 270, 148, 18
    gx0, gy0 = W - 64 - (2 * cw + gap), 112
    pos = [(gx0 + (i % 2) * (cw + gap), gy0 + (i // 2) * (chh + gap)) for i in range(4)]
    kf = []
    for i, (px, py) in enumerate(pos):
        a, z = i * 25, i * 25 + 22
        kf.append(f"{a}%,{z}%{{transform:translate({px-pos[0][0]}px,{py-pos[0][1]}px)}}")
    kf.append("100%{transform:translate(0,0)}")
    d.css.append(
        "@keyframes ch{" + "".join(kf) + "}.ch{animation:ch 10s cubic-bezier(.7,0,.25,1) infinite}"
        "@keyframes cur{0%,49%{opacity:1}50%,100%{opacity:0}}.cur{animation:cur 1s steps(1) infinite}"
        "@keyframes scr{0%{transform:translateX(0);opacity:.0}9%{opacity:.35}10%{transform:translateX(420px);opacity:0}"
        "35%{transform:translateX(160px);opacity:.25}37%{opacity:0}61%{transform:translateX(780px);opacity:.3}63%{opacity:0}100%{opacity:0}}"
        ".scr{animation:scr 3.1s steps(1) infinite}"
        "@keyframes fk{0%,100%{opacity:0}31%{opacity:.07}33%{opacity:0}72%{opacity:.05}74%{opacity:0}}.fk{animation:fk 2.3s steps(1) infinite}"
        "@keyframes stp{0%{opacity:0;transform:scale(1.6) rotate(-9deg)}60%{opacity:1;transform:scale(.96) rotate(-9deg)}100%{opacity:1;transform:scale(1) rotate(-9deg)}}"
        ".stp{transform-box:fill-box;transform-origin:center;transform:rotate(-9deg);animation:stp .5s cubic-bezier(.2,.8,.2,1) 1.2s both}"
    )
    frame_defs(d, H, BG)
    b = d.add
    b(f'<rect width="{W}" height="{H}" fill="url(#lamp)"/>')
    # giant faint 94
    x = 64
    b(slate(d, x, 78, "03", r["kind_zh"], r["kind_en"], accent=RED))
    ttl = S("iserif", 88, IVORY, -0.005)
    b(d.text(r["title"][0], ttl, x - 3, 170))
    b(d.text(r["title"][1], ttl, x - 3, 248))
    body = S("sans", 20, MUTE, 0.02)
    b(d.text(r["lines_zh"][0], body, x, 300))
    b(d.text(r["lines_zh"][1], body, x, 332))
    # "based on true stories" typewriter
    tws = S("mono_b", 21, IVORY, 0.06)
    line = f"{r['articles']} SOURCED WRITE-UPS."
    tw = measure(line, tws)
    n = len(line)
    ty = 410
    b(d.text(line, tws, x, ty))
    d.css.append(
        f"@keyframes typ{{0%{{transform:scaleX(1)}}45%,100%{{transform:scaleX(0)}}}}"
        f".typ{{transform-box:fill-box;transform-origin:right center;transform:scaleX(0);animation:typ 7s steps({n}) infinite}}"
        f"@keyframes tcu{{0%{{transform:translateX(0)}}45%,100%{{transform:translateX({_n(tw+4,1)}px)}}}}"
        f".tcu{{transform:translateX({_n(tw+4,1)}px);animation:tcu 7s steps({n}) infinite}}"
    )
    b(f'<rect class="typ" x="{x-2}" y="{ty-24}" width="{tw+6}" height="34" fill="{BG}"/>')
    b(f'<g class="tcu"><rect class="cur" x="{x}" y="{ty-19}" width="11" height="23" fill="{RED}"/></g>')
    b(d.text(f"整理 {r['articles']} 篇创作者经验 · 保留作者与原文链接", S("serif_med", 17, MUTE, 0.04, fallback=None), x, ty + 36))
    site = r["site"].replace("https://", "").rstrip("/")
    b(d.text(f"▶  {site}", S("mono_b", 14, IVORY, 0.06), x, 502))
    # chapter cards
    for i, ((px, py), chap) in enumerate(zip(pos, r["chapters"])):
        b(f'<rect x="{px}" y="{py}" width="{cw}" height="{chh}" rx="10" fill="#111" stroke="#fff" stroke-opacity=".12"/>')
        b(d.text(f"CHAPTER {chap[0]}", S("mono_b", 12, DIM, 0.26), px + 22, py + 34))
        lines = chap[1:]
        for j, ln in enumerate(lines):
            b(d.text(ln, S("serif_bold", 24, IVORY, 0.03, fallback=None), px + 22, py + 76 + j * 33))
        b(d.text("¹ 原文 ↗", S("sans", 12, DIM, 0.1), px + cw - 22, py + chh - 20, anchor="end"))
    hx, hy = pos[0]
    b(f'<g class="ch"><rect x="{hx-1.5}" y="{hy-1.5}" width="{cw+3}" height="{chh+3}" rx="11" fill="none" stroke="{RED}" stroke-width="2"/>'
      f'<rect x="{hx+22}" y="{hy-1.5}" width="40" height="3" fill="{RED}"/></g>')
    # footnote row
    fy = gy0 + 2 * chh + gap + 44
    b(d.text("作者 · 原文链接 · 原图 · 核验日期 —— 一样不少", S("sans", 15, MUTE, 0.04), gx0, fy))
    # stamp
    st = S("mono_b", 13, RED, 0.2)
    sw = measure("SOURCED · 有出处", st) + 28
    sx, sy = W - 64 - sw, fy - 22
    b(f'<g class="stp"><rect x="{sx}" y="{sy}" width="{sw}" height="32" rx="4" fill="none" stroke="{RED}" stroke-width="2"/>'
      + d.text("SOURCED · 有出处", st, sx + sw / 2, sy + 21, anchor="middle") + "</g>")
    frame_end(d, H)
    return d



# ================================================================= REELS 03–04 · Three Atlas / Awesome Agent MCP
def build_reel_atlas(cfg, mobile=False):
    r = cfg["reels"]["atlas"]
    width, height = (720, 660) if mobile else (W, 540)
    d = Doc(width, height, title="Three Atlas · 三维图鉴 · 三个世界的循环预告")
    d.defs.append(
        f'<clipPath id="atlas-frame"><rect width="{width}" height="{height}" rx="18"/></clipPath>'
        '<linearGradient id="atlas-shade"><stop stop-color="#070912"/><stop offset=".31" stop-color="#070912" stop-opacity=".98"/>'
        '<stop offset=".58" stop-color="#070912" stop-opacity=".22"/><stop offset="1" stop-color="#070912" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="atlas-vertical" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#070912" stop-opacity=".8"/>'
        '<stop offset=".22" stop-color="#070912" stop-opacity="0"/><stop offset=".63" stop-color="#070912" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#070912" stop-opacity=".98"/></linearGradient>'
        '<linearGradient id="atlas-flare"><stop stop-color="#B69BFF" stop-opacity="0"/><stop offset=".5" stop-color="#F6E4FF"/>'
        '<stop offset="1" stop-color="#B69BFF" stop-opacity="0"/></linearGradient>'
    )
    d.css.append(
        '.shot{opacity:0}.shot0{opacity:1}'
        '@keyframes world{0%,26%{opacity:1}33%,92%{opacity:0}100%{opacity:1}}'
        '.shot{animation:world 18s linear infinite}.shot1{animation-delay:-12s}.shot2{animation-delay:-6s}'
        '@keyframes camera{0%{transform:translate(14px,8px) scale(.98)}100%{transform:translate(-24px,-13px) scale(1.15)}}'
        '.camera{transform-box:fill-box;transform-origin:70% 48%;animation:camera 18s ease-in-out infinite alternate}'
        '.camera1{animation-direction:alternate-reverse}.camera2{animation-delay:-9s}'
        '@keyframes near{0%{transform:translate(22px,14px);opacity:0}15%,80%{opacity:.8}100%{transform:translate(-60px,-30px);opacity:0}}'
        '.near{animation:near 9s ease-in-out infinite}'
        '@keyframes flare{0%,35%{transform:translateX(-600px);opacity:0}43%{opacity:.8}56%{transform:translateX(1450px);opacity:0}100%{opacity:0}}'
        '.flare{animation:flare 6s ease-in-out infinite}'
        '@keyframes dolly{0%,100%{transform:translateX(10px)}50%{transform:translateX(-14px)}}.contact{animation:dolly 12s ease-in-out infinite}'
        '@keyframes playhead{0%{transform:scaleX(0)}100%{transform:scaleX(1)}}.playhead{transform-box:fill-box;transform-origin:left;animation:playhead 6s linear infinite}'
    )
    d.add(f'<g clip-path="url(#atlas-frame)"><rect width="{width}" height="{height}" fill="#070912"/>')
    scenes = r["scenes"]
    for i, scene in enumerate(scenes):
        im = cover(Image.open(IMG / scene["image"]), 1200, 750)
        d.defs.append(f'<image id="world{i}" href="{jpeg_uri(im, 85)}" width="1200" height="750"/>')
        ix, iy, iw, ih = (0, 215, 744, 465) if mobile else (398, -7, 930, 581)
        d.add(f'<g class="shot shot{i}"><g class="camera camera{i}"><svg x="{ix}" y="{iy}" width="{iw}" height="{ih}" viewBox="0 0 1200 750"><use href="#world{i}"/></svg></g></g>')
    if not mobile:
        d.add(f'<rect width="{width}" height="{height}" fill="url(#atlas-shade)"/>')
    d.add(f'<rect x="0" y="{210 if mobile else 0}" width="{width}" height="{450 if mobile else height}" fill="url(#atlas-vertical)"/>')
    # Sparse foreground points move faster than the scene to suggest depth.
    for i in range(13):
        sx = (i*137+561) % width
        sy = (i*83+120) % (height-120)+60
        if not mobile and sx < 550:
            sx += 550
        if mobile:
            sy = 310+(sy % 250)
        d.add(f'<g class="near" style="animation-delay:-{i*.61:.2f}s"><circle cx="{sx}" cy="{sy}" r="{1.2+(i%3)*.6}" fill="#E2CBFF" opacity=".6"/></g>')
    d.add(f'<g class="flare"><rect x="-300" y="{359 if mobile else 318}" width="550" height="1.4" fill="url(#atlas-flare)"/></g>')
    x = 48 if mobile else 64
    d.add(slate(d, x, 60 if mobile else 78, "03", r["kind_zh"], r["kind_en"], accent="#C1AAF4"))
    if mobile:
        d.add(d.text("Three Atlas", S("iserif", 76, IVORY), x-2, 145))
        d.add(d.text(r["lines_zh"][0], S("sans_med", 29, MUTE), x, 205))
    else:
        for i, line in enumerate(r["title"]):
            d.add(d.text(line, S("iserif", 100, IVORY), x-3, 180+i*90))
        for i, line in enumerate(r["lines_zh"]):
            d.add(d.text(line, S("sans", 21, MUTE), x, 330+i*34))
        d.add(d.text("A WORLD OF WORLDS.", S("mono", 16, "#C1AAF4", .12), x, 438))
        d.add(d.text("▶  " + r["site"].replace("https://", "").rstrip("/"), S("mono_b", 14, GOLD, .04), x, 502))
    # A moving contact sheet gives each world a visible place in the trailer.
    tx, ty, tw, th, gap = (48, 539, 194, 79, 19) if mobile else (688, 401, 158, 80, 18)
    d.add('<g class="contact">')
    for i, scene in enumerate(scenes):
        px = tx+i*(tw+gap)
        d.defs.append(f'<clipPath id="thumb{i}"><rect x="{px}" y="{ty}" width="{tw}" height="{th}" rx="5"/></clipPath>')
        d.add(f'<g clip-path="url(#thumb{i})"><svg x="{px}" y="{ty}" width="{tw}" height="{th}" viewBox="0 75 1200 600" preserveAspectRatio="xMidYMid slice"><use href="#world{i}"/></svg><rect x="{px}" y="{ty}" width="{tw}" height="{th}" fill="#070912" opacity=".23"/></g>')
        d.add(f'<rect x="{px}" y="{ty}" width="{tw}" height="{th}" rx="5" fill="none" stroke="#DBCFFF" stroke-opacity=".26"/>')
        d.add(f'<g class="shot shot{i}"><rect x="{px}" y="{ty}" width="{tw}" height="{th}" rx="5" fill="none" stroke="#E2CBFF" stroke-width="2"/><rect class="playhead" x="{px}" y="{ty+th+5}" width="{tw}" height="2" fill="#D7C2FF"/></g>')
    d.add('</g>')
    for i, scene in enumerate(scenes):
        cx, cy = (48, 506) if mobile else (688, 372)
        d.add(d.text(f"0{i+1} / {scene['label']}", S("mono_b", 19 if mobile else 14, IVORY, .07), cx, cy, cls=f"shot shot{i}"))
    d.add(f'<rect width="{width}" height="18" fill="#050607"/><rect y="{height-18}" width="{width}" height="18" fill="#050607"/>')
    d.add(corners(28, 28, width-56, height-56, arm=15, stroke="#D6C5FF", sw=1, op=.3))
    d.add(f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="17.5" fill="none" stroke="#fff" stroke-opacity=".1"/></g>')
    return d


def build_reel_agent(cfg, mobile=False):
    r = cfg["reels"]["agent"]
    width, height = (720, 660) if mobile else (W, 540)
    d = Doc(width, height, title="Awesome Agent MCP · 连接真实世界 · 动态片头")
    d.defs.append(
        f'<clipPath id="agent-frame"><rect width="{width}" height="{height}" rx="18"/></clipPath>'
        '<radialGradient id="core-glow"><stop stop-color="#E49E48" stop-opacity=".3"/><stop offset=".35" stop-color="#B47434" stop-opacity=".11"/><stop offset="1" stop-color="#07101B" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="agent-floor" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#273444" stop-opacity="0"/><stop offset="1" stop-color="#8CA8CF" stop-opacity=".45"/></linearGradient>'
        '<linearGradient id="agent-beam"><stop stop-color="#E8B867" stop-opacity="0"/><stop offset=".5" stop-color="#FFF2CA"/><stop offset="1" stop-color="#E8B867" stop-opacity="0"/></linearGradient>'
    )
    d.css.append(
        '@keyframes orbit{to{transform:rotate(360deg)}}.orbit{animation:orbit 24s linear infinite}.reverse{animation-direction:reverse;animation-duration:36s}'
        '@keyframes tilt{0%,100%{transform:scaleX(.34) rotate(-18deg)}50%{transform:scaleX(.95) rotate(18deg)}}.tilt{animation:tilt 9s ease-in-out infinite}'
        '@keyframes core{0%,100%{transform:rotate(-7deg) translateY(5px)}50%{transform:rotate(11deg) translateY(-9px)}}.core{animation:core 7s ease-in-out infinite}'
        '.orbit,.tilt,.core{transform-box:fill-box;transform-origin:center}'
        '@keyframes packet{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}.packet{animation:packet 3s linear infinite}'
        '@keyframes beacon{0%,100%{opacity:.3}50%{opacity:1}}.beacon{animation:beacon 3s ease-in-out infinite}'
        '@keyframes ripple{0%{transform:scale(.7);opacity:0}20%{opacity:.5}100%{transform:scale(1.45);opacity:0}}.ripple{transform-box:fill-box;transform-origin:center;animation:ripple 6s ease-out infinite}'
        '@keyframes node{0%,100%{transform:translateY(-5px)}50%{transform:translateY(6px)}}.node{animation:node 7s ease-in-out infinite}'
        '@keyframes floor{to{transform:translateY(52px)}}.floor{animation:floor 4s linear infinite}'
        '@keyframes beam{0%,28%{transform:translateX(-900px);opacity:0}36%{opacity:.8}66%,100%{transform:translateX(1400px);opacity:0}}.beam{animation:beam 8s ease-in-out infinite}'
    )
    d.add(f'<g clip-path="url(#agent-frame)"><rect width="{width}" height="{height}" fill="#090E16"/>')
    # The entire scene has a floor, rotating apparatus and separately moving foreground nodes.
    ox, oy = (0, 300) if mobile else (560, 0)
    cx, cy, radius = 360, (166 if mobile else 265), (108 if mobile else 151)
    d.add(f'<g transform="translate({ox} {oy})">')
    d.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{radius*2.2}" ry="{radius*1.8}" fill="url(#core-glow)"/>')
    horizon, floor_bottom = cy+40, (380 if mobile else 580)
    for i in range(11):
        bx = -200+i*110
        d.add(f'<path d="M{cx+(bx-cx)*.11} {horizon}L{bx} {floor_bottom}" fill="none" stroke="url(#agent-floor)" stroke-width="1"/>')
    d.add('<g class="floor" opacity=".16">')
    for i in range(5):
        fy = horizon+15+i*52
        d.add(f'<path d="M0 {fy}H720" stroke="#7599C8" stroke-width="1"/>')
    d.add('</g>')
    top_node = 42 if mobile else 80
    nodes = [(90, top_node, "出行生活", "LIFE"), (624, top_node, "设计创作", "DESIGN"),
             (70, cy, "办公协作", "WORK"), (650, cy, "云与开发", "CLOUD"),
             (100, cy+134 if mobile else 449, "搜索内容", "SEARCH"),
             (620, cy+134 if mobile else 449, "支付金融", "PAYMENT")]
    for i, (nx, ny, zh, en) in enumerate(nodes):
        # Beams visibly travel into the core instead of just shifting a dashed line.
        path = f'M{nx} {ny}C{(nx+cx)/2} {ny} {(nx+cx)/2} {cy} {cx} {cy}'
        d.add(f'<path d="{path}" fill="none" stroke="#7693B5" stroke-opacity=".24" stroke-width="1"/>')
        d.add(f'<path class="packet" style="animation-delay:-{i*.47:.2f}s" d="{path}" pathLength="100" fill="none" stroke="{GOLD}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="2 98"/>')
        d.add(f'<g class="node" style="animation-delay:-{i*.8:.1f}s"><circle cx="{nx}" cy="{ny}" r="5" fill="#E6BB77"/>'
              f'<circle class="beacon" style="animation-delay:-{i*.47:.2f}s" cx="{nx}" cy="{ny}" r="12" fill="none" stroke="{GOLD}" stroke-opacity=".65"/>')
        anchor = "start" if nx < cx else "end"
        label_x = nx-18 if nx < cx else nx+18
        d.add(d.text(zh, S("sans_med", 22 if mobile else 20, IVORY), label_x, ny-26, anchor=anchor))
        if not mobile:
            d.add(d.text(en, S("mono", 10, "#8096B1", .2), label_x, ny+29, anchor=anchor))
        d.add('</g>')
    d.add(f'<circle class="ripple" cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{GOLD}" stroke-width="1"/>')
    d.add(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="#0C131D" fill-opacity=".75" stroke="#B68D51" stroke-opacity=".55" stroke-width="1"/>')
    d.add('<g class="orbit">')
    for i in range(48):
        angle = i*pi/24
        inside = radius-(11 if i%4==0 else 5)
        d.add(f'<path d="M{cx+inside*cos(angle):.2f} {cy+inside*sin(angle):.2f}L{cx+(radius+2)*cos(angle):.2f} {cy+(radius+2)*sin(angle):.2f}" stroke="{GOLD}" stroke-opacity="{.75 if i%4==0 else .3}" stroke-width="1"/>')
    d.add(f'<circle cx="{cx}" cy="{cy}" r="{radius-21}" fill="none" stroke="{GOLD}" stroke-width="2" stroke-dasharray="84 28 10 28" stroke-opacity=".75"/></g>')
    d.add(f'<g class="orbit reverse"><circle cx="{cx}" cy="{cy}" r="{radius-34}" fill="none" stroke="#8DA9D1" stroke-width="1" stroke-dasharray="5 11" stroke-opacity=".55"/></g>')
    d.add(f'<g class="tilt"><circle cx="{cx}" cy="{cy}" r="{radius-10}" fill="none" stroke="#AFC3DE" stroke-width="1.2" stroke-opacity=".8"/></g>')
    # Isometric translucent core; slow roll gives the machinery an independent rhythm.
    s = 49 if mobile else 62
    d.add('<g class="core">')
    d.add(f'<path d="M{cx} {cy-s}L{cx+s*.87} {cy-s*.5}L{cx} {cy}L{cx-s*.87} {cy-s*.5}Z" fill="#EDBD76" fill-opacity=".26" stroke="#E5C89A" stroke-width="1.5"/>')
    d.add(f'<path d="M{cx-s*.87} {cy-s*.5}L{cx} {cy}V{cy+s}L{cx-s*.87} {cy+s*.5}Z" fill="#7C9CC9" fill-opacity=".12" stroke="#9BADC8" stroke-width="1.1"/>')
    d.add(f'<path d="M{cx} {cy}L{cx+s*.87} {cy-s*.5}V{cy+s*.5}L{cx} {cy+s}Z" fill="#DCA158" fill-opacity=".15" stroke="#E5C89A" stroke-width="1.1"/>')
    d.add(f'<circle class="beacon" cx="{cx}" cy="{cy}" r="5" fill="#FFF2D9"/></g>')
    d.add(d.text("AGENT", S("mono_b", 13 if mobile else 17, IVORY, .2), cx, cy+radius+29, anchor="middle"))
    d.add('</g>')
    d.add(f'<g class="beam"><rect x="-400" y="{oy+cy}" width="600" height="1.5" fill="url(#agent-beam)"/></g>')
    x = 48 if mobile else 64
    d.add(slate(d, x, 60 if mobile else 78, "04", r["kind_zh"], r["kind_en"]))
    for i, line in enumerate(r["title"]):
        d.add(d.text(line, S("iserif", 72 if mobile else 88, IVORY), x-3, (140 if mobile else 178)+i*(72 if mobile else 84)))
    if mobile:
        d.add(d.text(r["lines_zh"][0], S("sans_med", 28, MUTE), x, 276))
    else:
        for i, line in enumerate(r["lines_zh"]):
            d.add(d.text(line, S("sans", 21, MUTE), x, 328+i*34))
        d.add(d.text("MCP  /  SKILL  /  CLI", S("mono_b", 24, GOLD, .1), x, 438))
        d.add(d.text("▶  " + r["site"].replace("https://", "").rstrip("/"), S("mono_b", 14, GOLD, .03), x, 502))
    d.add(f'<rect width="{width}" height="18" fill="#050607"/><rect y="{height-18}" width="{width}" height="18" fill="#050607"/>')
    d.add(corners(28, 28, width-56, height-56, arm=15, stroke=GOLD, sw=1, op=.3))
    d.add(f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="17.5" fill="none" stroke="#fff" stroke-opacity=".1"/></g>')
    return d


# ================================================================= END CREDITS
def build_footer(cfg, mobile=False):
    width, height = (720, 230) if mobile else (1280, 230)
    d = Doc(width, height, title="观默 · 感谢观看 · X @" + cfg["x_handle"])
    d.defs.append(f'<linearGradient id="line"><stop stop-color="{GOLD}" stop-opacity="0"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>')
    d.add(f'<rect width="{width}" height="{height}" rx="18" fill="{INK}"/>')
    d.add(f'<rect x="40" y="1" width="{width-80}" height="1" fill="url(#line)"/>')
    d.add(d.text("The End", S("iserif_i", 60, IVORY), width/2, 91, anchor="middle"))
    d.add(d.text(cfg["tagline_zh"], S("serif_med", 28 if mobile else 26, MUTE), width/2, 144, anchor="middle"))
    d.add(d.text(f"x.com/{cfg['x_handle']}", S("mono", 22 if mobile else 18, GOLD, .08), width/2, 192, anchor="middle"))
    return d


# ================================================================= DIVIDERS (light + dark)
THEMES = {
    "dark": {"line": "#30363D", "text": "#8B949E", "accent": GOLD},
    "light": {"line": "#D0D7DE", "text": "#57606A", "accent": "#A0702A"},
}


def build_divider(no, kind_zh, kind_en, theme):
    t = THEMES[theme]
    H = 84
    d = Doc(W, H, title="")
    cy = 42
    lab = S("mono_b", 15, t["accent"], 0.3)
    sub = S("sans_med", 15, t["text"], 0.16)
    s1 = f"REEL {no}"
    s2 = f"{kind_zh} · {kind_en}"
    w = 30 + measure(s1, lab) + 18 + measure(s2, sub)
    x0 = W / 2 - w / 2
    d.css.append(
        "@keyframes rot{to{transform:rotate(360deg)}}.rot{transform-box:view-box;transform-origin:%spx %spx;animation:rot 2.4s linear infinite}" % (_n(x0 + 10, 2), cy)
        + "@keyframes ln{0%{transform:translateX(0)}70%,100%{transform:translateX(1700px)}}.ln{animation:ln 5s cubic-bezier(.45,0,.25,1) infinite}"
    )
    d.defs.append(
        f'<linearGradient id="lL" x1="0" x2="1"><stop offset="0" stop-color="{t["line"]}" stop-opacity="0"/><stop offset="1" stop-color="{t["line"]}"/></linearGradient>'
        f'<linearGradient id="lR" x1="0" x2="1"><stop offset="0" stop-color="{t["line"]}"/><stop offset="1" stop-color="{t["line"]}" stop-opacity="0"/></linearGradient>'
        f'<linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="{t["accent"]}" stop-opacity="0"/><stop offset=".5" stop-color="{t["accent"]}"/><stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="ln"><rect x="0" y="{cy-2}" width="{x0-24}" height="4"/><rect x="{x0+w+24}" y="{cy-2}" width="{W-(x0+w+24)}" height="4"/></clipPath>'
    )
    d.add(f'<rect x="0" y="{cy-0.75}" width="{x0-24}" height="1.5" fill="url(#lL)"/>')
    d.add(f'<rect x="{x0+w+24}" y="{cy-0.75}" width="{W-(x0+w+24)}" height="1.5" fill="url(#lR)"/>')
    d.add(f'<g clip-path="url(#ln)"><g class="ln"><rect x="-300" y="{cy-1.5}" width="300" height="3" fill="url(#sw)"/></g></g>')
    # film-leader dial
    cx = x0 + 10
    d.add(f'<circle cx="{_n(cx,2)}" cy="{cy}" r="10" fill="none" stroke="{t["accent"]}" stroke-width="1.5"/>')
    d.add(f'<path d="M{_n(cx-14,2)} {cy}H{_n(cx+14,2)}M{_n(cx,2)} {cy-14}V{cy+14}" stroke="{t["accent"]}" stroke-width="1" opacity=".5"/>')
    d.add(f'<g class="rot"><path d="M{_n(cx,2)} {cy}V{cy-10}A10 10 0 0 1 {_n(cx+8.66,2)} {cy-5}Z" fill="{t["accent"]}" opacity=".55"/></g>')
    d.add(d.text(s1, lab, x0 + 30, cy + 5.5))
    d.add(d.text(s2, sub, x0 + 30 + measure(s1, lab) + 18, cy + 5.5))
    return d


# ================================================================= BUTTONS (2x; display at height=28)
def build_button(kind, zh, en, theme=None):
    H = 56
    d = Doc(10, H, title=f"{zh} {en}".strip())
    zst = S("sans_bold", 21, IVORY, 0.08)
    est = S("jost_semi", 19, GOLD, 0.2)
    wz = measure(zh, zst) if zh else 0
    we = measure(en, est)
    pad = 22
    icon_w = 56
    w = icon_w + pad + wz + (16 if zh else 0) + we + pad
    d.w = int(round(w))
    b = d.add
    b(f'<rect width="{d.w}" height="{H}" rx="6" fill="#0B0B0C"/>')
    b(f'<rect x=".75" y=".75" width="{d.w-1.5}" height="{H-1.5}" rx="5.25" fill="none" stroke="{GOLD}" stroke-opacity=".38" stroke-width="1.5"/>')
    if kind == "x":
        b(f'<path d="M6 0h50v56H6a6 6 0 0 1-6-6V6a6 6 0 0 1 6-6z" fill="{IVORY}"/>')
        b('<g transform="translate(16 16) scale(1)"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z" fill="#0B0B0C"/></g>')
    else:
        b(f'<path d="M6 0h50v56H6a6 6 0 0 1-6-6V6a6 6 0 0 1 6-6z" fill="{GOLD}"/>')
        b('<path d="M22 17.5v21l17-10.5z" fill="#0B0B0C"/>')
    x = icon_w + pad
    if zh:
        b(d.text(zh, zst, x, 35.5))
        x += wz + 16
    b(d.text(en, est, x, 35))
    return d



# ================================================================= Mobile artwork
def mobile_frame(title, bg=INK, height=640):
    d = Doc(720, height, title=title)
    d.defs.append(f'<clipPath id="mf"><rect width="720" height="{height}" rx="18"/></clipPath>')
    d.add(f'<g clip-path="url(#mf)"><rect width="720" height="{height}" fill="{bg}"/>')
    return d


def mobile_end(d):
    d.add(f'<rect x=".5" y=".5" width="719" height="{d.h-1}" rx="17.5" fill="none" stroke="#fff" stroke-opacity=".1"/></g>')
    return d


def build_mobile_hero(cfg):
    d = mobile_frame("观默 GUANMO · AI 工程师", height=620)
    im = cover(Image.open(IMG / "hero.jpg"), 1080, 930, focus=(.82, .5))
    d.defs.append('<linearGradient id="mh"><stop stop-color="#030609" stop-opacity=".9"/><stop offset=".6" stop-color="#030609" stop-opacity=".55"/><stop offset="1" stop-color="#030609" stop-opacity=".08"/></linearGradient>')
    d.add(f'<image href="{jpeg_uri(im, 84)}" width="720" height="620"/>')
    d.add('<rect width="720" height="620" fill="url(#mh)"/>')
    d.add(d.text(cfg["role_en"], S("mono_b", 25, GOLD, .18), 48, 70))
    d.add(d.text(cfg["name_zh"], S("serif_black", 138, IVORY, .02, fallback=None), 42, 235))
    d.add(d.text(cfg["name_en"], S("jost_light", 33, IVORY, .5), 48, 302))
    d.add(f'<rect x="48" y="332" width="624" height="1" fill="{GOLD}" opacity=".6"/>')
    d.add(d.text(cfg["tagline_zh"], S("serif_bold", 31, IVORY), 48, 388))
    d.add(d.text("See the great work.", S("iserif_i", 28, MUTE), 48, 438))
    d.add(d.text("Learn the method behind it.", S("iserif_i", 28, MUTE), 48, 474))
    d.add(d.text(f"x.com/{cfg['x_handle']}", S("mono", 22, GOLD, .03), 48, 573))
    return mobile_end(d)


def build_mobile_reel(cfg, key):
    r = cfg["reels"][key]
    no = {"motion": "01", "design": "02", "xgrowth": "03"}[key]
    bg = {"motion": "#100D12", "design": "#12100E", "xgrowth": "#0B0B0B"}[key]
    d = mobile_frame(" ".join(r["title"]) + " · " + r["desc_zh_bold"], bg, height=660)
    accent = RED if key == "xgrowth" else GOLD
    d.add(d.text(f"REEL {no} / {r['kind_en']}", S("mono_b", 22, accent, .13), 48, 60))
    if key == "motion":
        d.add(d.text("Awesome AI", S("iserif", 76, IVORY), 46, 145))
        d.add(d.text("Motion", S("iserif", 76, IVORY), 46, 222))
        d.add(d.text(f"{r['works']} 个作品 · {r['genres']} 个创作方向", S("sans_med", 29, MUTE), 48, 279))
        frames = sorted((IMG / "frames").glob("*.jpg"))
        for i, index in enumerate([0, 4, 9, 10, 13, 17]):
            x, y = 40 + (i % 3) * 216, 320 + (i // 3) * 146
            im = cover(Image.open(frames[index]), 392, 220)
            d.add(f'<rect x="{x}" y="{y}" width="208" height="138" rx="3" fill="#28221B"/>')
            for hole in range(8):
                d.add(f'<rect x="{x+8+hole*25}" y="{y+4}" width="12" height="6" rx="1" fill="#B4AC9C" opacity=".6"/>')
            d.add(f'<image href="{jpeg_uri(im, 78)}" x="{x+4}" y="{y+14}" width="200" height="112"/>')
        d.add(d.text("原作 · 源码 · 提示词 · 制作过程", S("sans", 25, GOLD), 48, 634))
    elif key == "design":
        d.add(d.text("Design Style", S("iserif", 76, IVORY), 46, 147))
        d.add(d.text("面向设计师与 AI 的设计风格库", S("sans_med", 30, MUTE), 48, 204))
        for x, name, label in [(66, "bauhaus.png", "包豪斯 · Bauhaus"), (398, "bento.png", "便当盒 · Bento")]:
            im = cover(Image.open(IMG / "posters" / name), 460, 574)
            d.add(f'<image href="{jpeg_uri(im, 84)}" x="{x}" y="254" width="256" height="320"/>')
            d.add(d.text(label, S("sans_med", 24, IVORY), x, 614))
    else:
        d.add(d.text("Awesome", S("iserif", 76, IVORY), 46, 142))
        d.add(d.text("X Growth", S("iserif", 76, IVORY), 46, 219))
        d.add(d.text(f"{r['articles']} 篇创作者经验 · 每篇都有出处", S("sans_med", 28, MUTE), 48, 278))
        for i, chapter in enumerate(r["chapters"]):
            x, y = 48 + (i % 2) * 324, 330 + (i // 2) * 146
            d.add(f'<rect x="{x}" y="{y}" width="300" height="126" rx="10" fill="#151313" stroke="#fff" stroke-opacity=".14"/>')
            d.add(d.text(f"CHAPTER {chapter[0]}", S("mono", 18, RED, .09), x+20, y+30))
            for j, line in enumerate(chapter[1:]):
                d.add(d.text(line, S("serif_bold", 28, IVORY, fallback=None), x+20, y+70+j*35))
        d.add(d.text("原创导读 · 有限摘录 · 原文链接", S("sans", 25, MUTE), 48, 634))
    return mobile_end(d)


# ================================================================= Profile layout components
def build_profile_separator(theme):
    line = "#D8DEE4" if theme == "light" else "#3D444D"
    accent = "#A87D3D" if theme == "light" else "#E8B867"
    d = Doc(1280, 24, title="项目分隔 / Project separator")
    d.add(f'<path d="M0 12H617M663 12H1280" stroke="{line}" stroke-width="1"/>')
    d.add(f'<circle cx="640" cy="12" r="7" fill="none" stroke="{accent}" stroke-width="1.25"/>')
    d.add(f'<path d="M629 12H651M640 1V23" stroke="{accent}" stroke-width=".8" opacity=".7"/>')
    return d


def build_profile_button(zh, en, primary=False, theme="light"):
    accent = "#A87D3D" if theme == "light" else "#E8B867"
    cn = Style([F["sans_semi"]], 21, "#EDE6D6" if primary else accent, .04)
    latin = Style([F["mono_b"]], 17.5, "#E8B867" if primary else accent, .04)
    slash = Style([F["mono_b"]], 15, "#E8B867" if primary else accent, .02)
    x = 64
    slash_x = x + measure(zh, cn) + 10
    latin_x = slash_x + measure("/", slash) + 10
    w = ceil(latin_x + measure(en, latin) + 34)
    d = Doc(w, 56, title=f"{zh} / {en}")
    fill = "#0B0B0C" if primary else "none"
    stroke = "#B88B48" if primary else accent
    d.add(f'<rect x=".75" y=".75" width="{w-1.5}" height="54.5" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    if primary:
        d.add('<path d="M6 0H48V56H6A6 6 0 0 1 0 50V6A6 6 0 0 1 6 0Z" fill="#E8B867"/>')
        d.add('<path d="M19 18V38L35 28Z" fill="#0B0B0C"/>')
    else:
        d.add(f'<path d="M23 19L14 28L23 37M33 19L42 28L33 37" fill="none" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
    d.add(d.text(zh, cn, x, 36))
    d.add(d.text("/", slash, slash_x, 35))
    d.add(d.text(en, latin, latin_x, 35))
    arrow = "#E8B867" if primary else accent
    d.add(f'<path d="M{w-27} 33L{w-18} 24M{w-26} 24H{w-18}V32" fill="none" stroke="{arrow}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>')
    return d


# ================================================================= README
def responsive_image(name, alt):
    from html import escape
    return (f'<picture><source media="(max-width: 767px)" srcset="assets/mobile/{name}.svg">'
            f'<img src="assets/{name}.svg" width="100%" alt="{escape(alt, quote=True)}"></picture>')


def build_readme(cfg):
    from html import escape

    u = cfg["user"]
    lines = [f"<!-- {cfg['name_zh']} {cfg['name_en']} · cinematic profile README. Generated by src/build.py — edit src/config.json, then rebuild. -->", ""]
    for i, key in enumerate(cfg["featured_reels"], 1):
        item = cfg["reels"][key]
        text = item["profile"]
        repo = f"https://github.com/{u}/{item['repo']}"
        if i > 1:
            lines.extend(['<picture><source media="(prefers-color-scheme: dark)" srcset="assets/separator-dark.svg"><img src="assets/separator-light.svg" width="100%" alt=""></picture>', ""])
        lines.extend([f'<h3>0{i} / {escape(" ".join(item["title"]))}</h3>', ""])
        lines.extend([f'<a href="{repo}">' + responsive_image(f"reel-0{i}-{key}", " ".join(item["title"])) + "</a>", ""])
        zh = f'<b>{escape(text["zh_lead"])}</b><br>{escape(text["zh"])}'
        en = f'<b>{escape(text["en_lead"])}</b> {escape(text["en"])}'
        lines.extend([f'<p align="left" lang="zh-CN">{zh}</p>', "", f'<p align="left" lang="en">{en}</p>', ""])
        primary = f'<a href="{item["site"]}"><img src="assets/button-{key}.svg" height="36" alt="{escape(text["cta_zh"])} / {escape(text["cta_en"])}"></a>'
        source = f'<a href="{repo}"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/button-repo-dark.svg"><img src="assets/button-repo-light.svg" height="36" alt="仓库 / Repository"></picture></a>'
        lines.extend([f'<p align="left">{primary} {source}</p>', ""])
    lines.extend([f'<a href="{cfg["x_url"]}">' + responsive_image("footer", f'The End · X @{cfg["x_handle"]}') + "</a>", ""])
    (ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="构建观默 GitHub 主页。")
    parser.add_argument("assets", nargs="*", help="可选：只重建指定图片，例如 hero 或 mobile/hero。")
    args = parser.parse_args()
    cfg = json.loads((SRC / "config.json").read_text(encoding="utf-8"))
    only = set(args.assets)
    R = cfg["reels"]
    builders = {"hero": build_hero, "reel-01-motion": build_reel_motion, "reel-02-design": build_reel_design,
                "reel-03-xgrowth": build_reel_xgrowth, "footer": build_footer,
                "reel-03-atlas": build_reel_atlas, "reel-04-agent": build_reel_agent}
    builders.update({
        "mobile/hero": build_mobile_hero,
        "mobile/reel-01-motion": lambda c: build_mobile_reel(c, "motion"),
        "mobile/reel-02-design": lambda c: build_mobile_reel(c, "design"),
        "mobile/reel-03-xgrowth": lambda c: build_mobile_reel(c, "xgrowth"),
        "mobile/reel-03-atlas": lambda c: build_reel_atlas(c, mobile=True),
        "mobile/reel-04-agent": lambda c: build_reel_agent(c, mobile=True),
        "mobile/footer": lambda c: build_footer(c, mobile=True),
    })
    for i, k in enumerate(cfg["featured_reels"], 1):
        for th in THEMES:
            builders[f"divider-0{i}-{th}"] = (lambda c, i=i, k=k, th=th: build_divider(f"0{i}", R[k]["kind_zh"], R[k]["kind_en"], th))
    for k in cfg["featured_reels"]:
        builders[f"btn-{k}"] = (lambda c, k=k: build_button("play", R[k]["cta_zh"], R[k]["cta_en"]))
    builders["btn-x"] = lambda c: build_button("x", "关注", "@" + c["x_handle"])
    for theme in THEMES:
        builders[f"separator-{theme}"] = lambda c, theme=theme: build_profile_separator(theme)
        builders[f"button-repo-{theme}"] = lambda c, theme=theme: build_profile_button("仓库", "REPO", theme=theme)
    for key in cfg["featured_reels"]:
        builders[f"button-{key}"] = lambda c, key=key: build_profile_button(c["reels"][key]["profile"]["cta_zh"], c["reels"][key]["profile"]["cta_en"], primary=True)

    unknown = only - builders.keys()
    if unknown:
        parser.error("未知图片名称：" + ", ".join(sorted(unknown)))
    for name, fn in builders.items():
        if only and name not in only:
            continue
        d = fn(cfg)
        size = d.save(str(OUT / f"{name}.svg"))
        d.css.append("*{animation:none!important}")
        d.save(str(ROOT / "preview" / "static" / f"{name}.svg"))
        print(f"{name}.svg  {size/1024:.0f} KB")
    if not only:
        build_readme(cfg)
        print("README.md")


if __name__ == "__main__":
    main()

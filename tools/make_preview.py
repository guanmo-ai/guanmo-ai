#!/usr/bin/env python3
"""生成本地预览；控制栏不进入 GitHub README。"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREV = ROOT / "preview"
cfg = json.loads((ROOT / "src/config.json").read_text())
profile = json.loads((ROOT / "docs/profile-snapshot.json").read_text())
md = (ROOT / "README.md").read_text()
out = []
for chunk in re.split(r"\n\s*\n", md.strip()):
    c = chunk.strip()
    out.append(c if c.startswith(("<!--", "<p", "<h", "<table", "<details", "</details")) or c in ("<br>", "<br/>") else f"<p>{c}</p>")
body = "\n".join(out)
body = body.replace('src="assets/', 'src="../assets/').replace('srcset="assets/', 'srcset="../assets/')
body = body.replace('href="docs/', 'href="../docs/')
body = body.replace('<a href=', '<a target="_blank" rel="noopener noreferrer" href=')
name = html.escape(profile.get("name") or cfg["name_zh"])
user = html.escape(cfg["user"])
bio = f'<p class="bio">{html.escape(cfg["profile_bio"])}</p>'

page = '''<!doctype html>
<html lang="zh-CN" data-theme="dark"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>观默 · GitHub 主页</title>
<link rel="stylesheet" href="github-markdown.css">
<style>
:root{color-scheme:dark;--bg:#0d1117;--bg2:#010409;--fg:#f0f6fc;--mute:#9198a1;--bd:#3d444d;--acc:#4493f8}
:root[data-theme="light"]{color-scheme:light;--bg:#fff;--bg2:#f6f8fa;--fg:#1f2328;--mute:#59636e;--bd:#d1d9e0;--acc:#0969da}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
header{background:var(--bg2);border-bottom:1px solid var(--bd);padding:16px 32px 0}
.top{display:flex;gap:14px;align-items:center;height:32px}.top svg{fill:var(--fg)}
.search{margin-left:auto;width:300px;height:32px;border:1px solid var(--bd);border-radius:6px;padding:5px 12px;color:var(--mute);font-size:13px}
nav{display:flex;gap:20px;margin-top:12px;white-space:nowrap;overflow:auto;scrollbar-width:none}nav::-webkit-scrollbar{display:none}nav span{padding:8px 0 12px}nav .on{border-bottom:2px solid #d5a66c;font-weight:600}nav i{font-style:normal;background:var(--bd);border-radius:20px;padding:1px 6px;font-size:12px;margin-left:4px}
.wrap{max-width:1280px;margin:auto;padding:24px 32px;display:flex;gap:24px}
aside{width:296px;flex:none}aside img{width:296px;height:296px;border-radius:50%;border:1px solid var(--bd)}
.name{font-size:24px;font-weight:600;line-height:1.25;margin-top:16px}.user{font-size:20px;font-weight:300;color:var(--mute)}
.follow{display:block;text-align:center;border:1px solid var(--bd);background:var(--bg2);border-radius:6px;padding:5px;margin:16px 0;color:var(--fg);font-weight:500}
.stats{color:var(--mute);margin:16px 0}.aside-note{font-size:12px;color:var(--mute);margin-top:24px;padding-top:16px;border-top:1px solid var(--bd)}
main{flex:1;min-width:0}.readme{border:1px solid var(--bd);border-radius:6px;padding:24px}.rh{font-size:12px;font-family:ui-monospace,monospace;color:var(--mute);margin-bottom:16px}
body .markdown-body{background:transparent;color:var(--fg);--fgColor-default:var(--fg);--fgColor-muted:var(--mute);--fgColor-accent:var(--acc);--bgColor-default:var(--bg);--bgColor-muted:var(--bg2);--borderColor-default:var(--bd);--borderColor-muted:var(--bd)}
.markdown-body a{color:var(--acc)}.markdown-body img{background:transparent}
.note{margin:20px 0;color:var(--mute);font-size:12px}
@media(max-width:767px){header{padding:12px 16px 0}.search{display:none}nav{gap:20px}.wrap{display:block;padding:16px}aside{width:auto;display:grid;grid-template-columns:72px 1fr;gap:0 16px;align-items:center}aside img{width:72px;height:72px}.name{margin:0}.follow,.stats,.bio{grid-column:1/3}.aside-note{display:none}.stats{margin:0 0 16px}.readme{padding:16px}.markdown-body{font-size:14px}.note{margin:16px 0}}
</style></head><body>
<header><div class="top"><svg width="30" height="30" viewBox="0 0 16 16" aria-label="GitHub"><path d="M8 0a8 8 0 0 0-2.53 15.59c.4.07.55-.17.55-.38v-1.49c-2.23.48-2.7-1.08-2.7-1.08-.36-.92-.89-1.17-.89-1.17-.73-.5.05-.49.05-.49.8.06 1.22.82 1.22.82.72 1.22 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.65-.89-3.65-3.95 0-.88.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.22 2.2.82a7.65 7.65 0 0 1 4 0c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.74.54 1.49v2.21c0 .21.15.46.55.38A8 8 0 0 0 8 0Z"/></svg><b>__USER__</b><div class="search">Type / to search</div></div>
<nav><span class="on">Overview</span><span>Repositories<i>__REPOS__</i></span><span>Projects</span><span>Packages</span><span>Stars</span></nav></header>
<div class="wrap"><aside><img src="avatar.png" alt="观默的 GitHub 头像"><div><div class="name">__NAME__</div><div class="user">__USER__</div></div><a class="follow" href="https://github.com/__USER__" target="_blank" rel="noopener noreferrer">Follow</a>__BIO__<div class="stats">__FOLLOWERS__ followers · __FOLLOWING__ following</div></aside>
<main><div class="readme"><div class="rh">__USER__ / README.md</div><article class="markdown-body">__BODY__</article></div><p class="note">GitHub 布局模拟 · 最终外观以 GitHub 实际渲染为准。关注数为本次核对时的快照。</p></main></div>
<script>
const params=new URLSearchParams(location.search);
document.documentElement.dataset.theme=params.get('theme')==='light'?'light':'dark';
for(const source of document.querySelectorAll('picture source[media*="prefers-color-scheme"]'))source.media=document.documentElement.dataset.theme==='dark'?'all':'not all';
if(params.get('motion')==='off')for(const el of document.querySelectorAll('img[src^="../assets/"],source[srcset^="../assets/"]')){const attr=el.tagName==='SOURCE'?'srcset':'src';el.setAttribute(attr,el.getAttribute(attr).replace('../assets/','static/'));}
</script></body></html>'''
for token, value in {"__USER__":user,"__NAME__":name,"__BIO__":bio,"__BODY__":body,"__REPOS__":str(profile["public_repos"]),"__FOLLOWERS__":str(profile["followers"]),"__FOLLOWING__":str(profile["following"])}.items():
    page = page.replace(token,value)
(PREV / "profile.html").write_text(page)

(PREV / "index.html").write_text('''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>观默 · 主页预览</title>
<style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#191817;color:#ede6d6;font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.toolbar{position:sticky;top:0;z-index:2;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:14px 24px;background:#191817f5;border-bottom:1px solid #454038;backdrop-filter:blur(12px)}.brand{display:flex;align-items:baseline;gap:12px}.brand b{font-size:17px;letter-spacing:2px}.brand span{font-size:12px;color:#b5ad9d}.controls{display:flex;gap:8px;flex-wrap:wrap}button{background:#282520;border:1px solid #5f5445;border-radius:6px;color:#ede6d6;padding:7px 12px;font:inherit;cursor:pointer}button[aria-pressed="true"]{background:#e8b867;color:#211a12;border-color:#e8b867}button:focus-visible{outline:2px solid #e8b867;outline-offset:3px}.stage{padding:20px 12px 48px}iframe{display:block;width:100%;max-width:1280px;min-height:900px;border:1px solid #454038;border-radius:8px;margin:auto;background:#0d1117;transition:max-width .2s}.hint{max-width:1280px;margin:0 auto 14px;padding:0 4px;color:#b5ad9d;font-size:12px}.hint a{color:#e8b867}body.mobile iframe{max-width:390px}body.light{background:#e6e1d8}body.light .hint{color:#5b5144}body.light .hint a{color:#765426}@media(max-width:600px){.toolbar{padding:12px 16px}.brand span{font-size:11px}.controls{gap:6px}button{padding:6px 9px;font-size:12px}.stage{padding:12px 6px 32px}}
</style></head><body><div class="toolbar"><div class="brand"><b>观默 GUANMO</b><span>GitHub 主页预览</span></div><div class="controls" role="group" aria-label="预览设置"><button id="dark" aria-pressed="true">深色</button><button id="light" aria-pressed="false">浅色</button><button id="desktop" aria-pressed="true">桌面</button><button id="mobile" aria-pressed="false">手机</button><button id="motion" aria-pressed="false">暂停动效</button></div></div><div class="stage"><p class="hint">可切换主题、屏幕尺寸与动效状态，向下滚动查看四个项目。 <a href="../README.md" target="_blank" rel="noopener">查看主页文案 ↗</a></p><iframe id="preview" title="观默 GitHub 主页预览" src="profile.html?theme=dark"></iframe></div>
<script>
const frame=document.getElementById('preview');let theme='dark',motion=true;
function pressed(id,value){document.getElementById(id).setAttribute('aria-pressed',String(value));}
function size(){try{const h=Math.max(900,Math.ceil(frame.contentDocument.body.getBoundingClientRect().height)+4);if(Math.abs(frame.getBoundingClientRect().height-h)>2)frame.style.height=h+'px';}catch{}}
function refresh(){frame.src='profile.html?theme='+theme+'&motion='+(motion?'on':'off');}
for(const mode of ['dark','light'])document.getElementById(mode).onclick=()=>{theme=mode;document.body.classList.toggle('light',mode==='light');pressed('dark',mode==='dark');pressed('light',mode==='light');refresh();};
for(const mode of ['desktop','mobile'])document.getElementById(mode).onclick=()=>{document.body.classList.toggle('mobile',mode==='mobile');pressed('desktop',mode==='desktop');pressed('mobile',mode==='mobile');};
document.getElementById('motion').onclick=()=>{motion=!motion;pressed('motion',!motion);document.getElementById('motion').textContent=motion?'暂停动效':'播放动效';refresh();};
frame.onload=()=>{size();try{new ResizeObserver(size).observe(frame.contentDocument.body);}catch{}};
new ResizeObserver(size).observe(frame);
</script></body></html>''')
print("预览已生成：", PREV / "index.html")

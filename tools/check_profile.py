#!/usr/bin/env python3
"""检查 GitHub 主页所需资源、SVG 安全边界与响应式回退。"""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.mobile = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "source" and attrs.get("media") == "(max-width: 767px)":
            self.mobile += 1
        for attr in ("src", "srcset", "href"):
            ref = attrs.get(attr, "")
            if ref.startswith(("assets/", "docs/")):
                self.refs.append(ref)


def check(root):
    errors = []
    parser = Images()
    parser.feed((root / "README.md").read_text())
    cfg = json.loads((root / "src/config.json").read_text())
    if parser.mobile != len(cfg["featured_reels"]) + 1:
        errors.append("每个展示项目与片尾应各有手机专用图。")
    for ref in parser.refs:
        if not (root / ref).is_file():
            errors.append(f"本地引用不存在：{ref}")
    svgs = list((root / "assets").rglob("*.svg"))
    for path in svgs:
        try:
            tree = ET.parse(path).getroot()
        except ET.ParseError as e:
            errors.append(f"{path.name}：XML 无效：{e}")
            continue
        ids = {node.get("id") for node in tree.iter() if node.get("id")}
        for node in tree.iter():
            if node.tag.rsplit("}", 1)[-1] in ("script", "foreignObject"):
                errors.append(f"{path.name}：存在脚本或 HTML。")
            for attr, value in node.attrib.items():
                if attr.lower().startswith("on"):
                    errors.append(f"{path.name}：存在事件处理器。")
                if attr.endswith("href"):
                    if value.startswith("#"):
                        if value[1:] not in ids:
                            errors.append(f"{path.name}：未定义的引用 {value}")
                    elif not value.startswith("data:image/"):
                        errors.append(f"{path.name}：依赖外部资源 {value}")
                for target in re.findall(r"url\(#([^)]+)\)", value):
                    if target not in ids:
                        errors.append(f"{path.name}：未定义的效果 {target}")
        if path.stat().st_size >= 1024 * 1024:
            errors.append(f"{path.name}：超过 1 MiB。")
        if "prefers-reduced-motion" not in path.read_text():
            errors.append(f"{path.name}：缺少减少动态效果支持。")
    return errors, len(svgs)


if __name__ == "__main__":
    errors, count = check(ROOT)
    for error in errors:
        print("失败：", error)
    if errors:
        raise SystemExit(1)
    print(f"通过：{count} 个 SVG，自包含资源、局部引用、手机图片与减少动态效果规则有效。")

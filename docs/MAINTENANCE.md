# 主页维护

这是 GitHub 账号 `guanmo-ai` 的主页 README 与构建源码。

## 修改与预览

文案、数字与展示顺序在 `src/config.json`（`featured_reels`）；每个项目的 `profile` 字段维护中英文介绍与双语入口。图片与主页排版在 `src/build.py`，字体许可证保留在 `fonts/`。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
bash scripts/fetch_fonts.sh
.venv/bin/python src/build.py
.venv/bin/python tools/make_preview.py
python3 tools/check_profile.py
python3 -m http.server 4197 --bind 127.0.0.1
```

打开 [本地预览](http://127.0.0.1:4197/preview/index.html)，可切换深浅色、桌面与手机尺寸、动态与静态画面。动态 SVG 使用减弱动态效果媒体查询；预览里的静态切换使用 `preview/static/` 下的静态 SVG。

生成器使用 HarfBuzz 排版并将字形转为 SVG 路径，图片以内嵌数据保存，因此成品不依赖外部字体或第三方徽章服务。手机使用 `assets/mobile/` 中的专用构图。作品数和文章数是人工核验的快照，更新时修改配置后重建；主页不烘焙 Star 数。

Python 依赖已固定版本；字体下载固定到 Google Fonts 的一个提交，并按 `fonts/SHA256SUMS.txt` 校验。校验失败时停止构建，核对上游与许可证后再更新。

## 发布范围

按 GitHub 的 [主页 README 规则](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)，公开仓库 `guanmo-ai/guanmo-ai` 的根目录 `README.md` 会展示在账号主页。

2026-10-22，用户已授权删除正文副标题后推送至公开主页仓库 `guanmo-ai/guanmo-ai`。发布前核验当前认证账号与远程状态。主页 README 与账号资料是分别维护的；本仓库的发布不修改账号简介、仓库置顶或定时自动化。

主页运行所需：`README.md`、`assets/`、`docs/SOURCES.md`。建议同时保留构建源码、字体许可证、字体下载脚本和预览工具。无需上传大字体、截图、录屏、虚拟环境或原始调研数据。

## 素材

头图、胶片画面、海报与头像沿用用户提供的交接包。已去除程序叠加的颗粒和划痕，并补充 [画面来源](SOURCES.md)。字体均保留原始 OFL 许可证。封面素材沿用交接包，SVG 由本仓库源码重建。

## 当前首页结构

四个项目按 Awesome AI Motion、Design Style、Three Atlas、Awesome Agent MCP 排列，均使用编号标题、原有展示图、左对齐中英文介绍与 36px 高双语按钮。项目之间使用紧凑的取景器细线分隔；各项目图、手机专用构图与片尾保留。主页不显示“画面来源 / Artwork sources”入口；来源记录保留在 `docs/SOURCES.md`。个人品牌头图、顶部关注按钮、个人副标题与重复身份文字不进入正文。GitHub 自带的 README 文件标题由平台显示。

2026-11-09，按用户要求将第 3 个项目改为 Three Atlas，第 4 个项目设为 Awesome Agent MCP。Awesome X Growth 的配置、构建函数与旧资源保留，当前不进入主页展示。Three Atlas 使用真实作品封面，Agent MCP 使用本仓库绘制的服务连接示意图；本次不修改账号资料或仓库置顶。

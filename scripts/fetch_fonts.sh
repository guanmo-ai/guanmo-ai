#!/usr/bin/env bash
# 下载构建所需字体（全部为 SIL Open Font License）。
# 小字体（Jost / JetBrains Mono / Instrument Serif）已随包附带；Noto 中文字体体积大（~42MB），用本脚本拉取。
#   bash scripts/fetch_fonts.sh          # 只补齐缺失的字体
#   bash scripts/fetch_fonts.sh --all    # 全部重新下载
set -euo pipefail
cd "$(dirname "$0")/../fonts"
BASE="https://raw.githubusercontent.com/google/fonts/47d54ca1ebb14fd864695f1d39dc734f39017c33/ofl"
get() { # get <local-name> <remote-path>
  if [[ "${1:-}" != "" && ( "${ALL:-0}" == "1" || ! -s "$1" ) ]]; then
    echo "↓ $1"; curl -fL --retry 3 -o "$1.part" "$BASE/$2" && mv "$1.part" "$1"
  else echo "✓ $1"; fi
}
[[ "${1:-}" == "--all" ]] && ALL=1
get NotoSerifSC-VF.ttf          "notoserifsc/NotoSerifSC%5Bwght%5D.ttf"
get NotoSansSC-VF.ttf           "notosanssc/NotoSansSC%5Bwght%5D.ttf"
get Jost-VF.ttf                 "jost/Jost%5Bwght%5D.ttf"
get JetBrainsMono-VF.ttf        "jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf"
get InstrumentSerif-Regular.ttf "instrumentserif/InstrumentSerif-Regular.ttf"
get InstrumentSerif-Italic.ttf  "instrumentserif/InstrumentSerif-Italic.ttf"
python3 - <<'PY'
from pathlib import Path
import hashlib
for line in Path("SHA256SUMS.txt").read_text().splitlines():
    expected, name = line.split(maxsplit=1)
    path = Path(name.strip())
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"字体校验失败：{path.name}")
print("字体 SHA-256 校验通过。")
PY
echo "fonts ready."

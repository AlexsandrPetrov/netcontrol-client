#!/bin/bash
# Генерирует все иконки res/ из brand/icon.svg и brand/tray.svg.
#
# Запускать на машине с inkscape и ImageMagick (на боевом сервере их нет,
# поэтому генерируем локально и копируем результат). Из корня форка:
#     brand/gen_icons.sh
#
# Размеры не выдуманы - сняты с оригинальных файлов upstream, чтобы упаковка
# (deb/rpm/msi, macOS bundle, трей) получала ровно то, что ожидает.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BRAND="$REPO_ROOT/brand"
RES="$REPO_ROOT/res"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

render() {  # <svg> <размер> <выходной файл>
    inkscape --export-type=png --export-filename="$3" -w "$2" -h "$2" "$1" >/dev/null 2>&1
}

echo "==> иконка приложения"
for size in 16 24 32 48 64 128 256; do
    render "$BRAND/icon.svg" "$size" "$TMP/app_$size.png"
done

cp "$TMP/app_32.png"  "$RES/32x32.png"
cp "$TMP/app_64.png"  "$RES/64x64.png"
cp "$TMP/app_128.png" "$RES/128x128.png"
cp "$TMP/app_256.png" "$RES/128x128@2x.png"
cp "$TMP/app_256.png" "$RES/icon.png"
cp "$TMP/app_256.png" "$RES/mac-icon.png"

# .ico собираем через Pillow, а не ImageMagick: IM здесь пишет несжатые
# BMP-кадры и один icon.ico раздувается до ~370 КБ вместо ~30 КБ.
python3 - "$TMP/app_256.png" "$RES/icon.ico" "$RES/tray-icon.ico" <<'PY'
import sys
from PIL import Image

src, app_ico, tray_ico = sys.argv[1:4]
img = Image.open(src).convert('RGBA')
img.save(app_ico, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
img.save(tray_ico, sizes=[(16, 16), (24, 24), (32, 32), (48, 48)])
PY

echo "==> логотип в боковой панели клиента"
# flutter/assets/logo_*.png - тот логотип, который виден в самом окне
# программы. Он НЕ берётся из icon.svg, это отдельные файлы, и upstream
# глушит все *png в .gitignore - поэтому в репозиторий они попадают только
# через git add -f. Забыть про них легко: окно останется со старым знаком,
# хотя иконка в меню уже новая.
render "$BRAND/icon.svg" 120 "$TMP/logo_120.png"
cp "$TMP/logo_120.png" "$BRAND/logo_120.png"
cp "$TMP/logo_120.png" "$REPO_ROOT/flutter/assets/logo_dark.png"
cp "$TMP/logo_120.png" "$REPO_ROOT/flutter/assets/logo_light.png"

echo "==> иконки трея (одноцветные силуэты)"
# dark-вариант рисуется тёмным (для светлой строки меню), light - белым.
sed 's/TRAYCOLOR/#000000/g' "$BRAND/tray.svg" > "$TMP/tray-dark.svg"
sed 's/TRAYCOLOR/#FFFFFF/g' "$BRAND/tray.svg" > "$TMP/tray-light.svg"
render "$TMP/tray-dark.svg"  44 "$RES/mac-tray-dark-x2.png"
render "$TMP/tray-light.svg" 44 "$RES/mac-tray-light-x2.png"

echo "==> готово:"
ls -l "$RES/32x32.png" "$RES/64x64.png" "$RES/128x128.png" "$RES/128x128@2x.png" \
      "$RES/icon.png" "$RES/mac-icon.png" "$RES/icon.ico" "$RES/tray-icon.ico" \
      "$RES/mac-tray-dark-x2.png" "$RES/mac-tray-light-x2.png"

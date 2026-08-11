#!/bin/bash
# Обновляет вендоренный libs/hbb_common до версии, на которую указывает
# submodule в upstream/master, и заново накладывает брендинг.
#
# Зачем вообще вендоринг: upstream держит hbb_common отдельным submodule, а нам
# нужен один репозиторий - AGPL обязывает публиковать исходники всего, что мы
# раздаём. Ручное слияние этого каталога при каждом обновлении - ровно та
# работа, из-за которой затею бросили в августе. Теперь это одна команда.
#
# Запуск из корня форка, после git fetch upstream --tags:
#     brand/vendor_hbb_common.sh          # по умолчанию - тег 1.4.9
#     brand/vendor_hbb_common.sh 1.5.0    # при переходе на новый релиз
#     brand/vendor_hbb_common.sh upstream/master
#
# База по умолчанию - РЕЛИЗНЫЙ ТЕГ, а не master: 2026-09-05 сборка с master
# упала (bridge_generated.rs зовёт plugin_install/plugin_list_reload, которых
# нет без фичи plugin_framework) - в master попадают неготовые изменения.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

REF="${1:-1.4.9}"
SHA="$(git ls-tree "$REF" libs/hbb_common | awk '{ print $3 }')"
if [ -z "$SHA" ]; then
    echo "Не удалось прочитать указатель submodule из $REF" >&2
    exit 1
fi
echo "==> $REF указывает на hbb_common $SHA"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --quiet https://github.com/rustdesk/hbb_common.git "$TMP/src"
git -C "$TMP/src" checkout --quiet "$SHA"
rm -rf "$TMP/src/.git"

rm -rf libs/hbb_common
mkdir -p libs/hbb_common
cp -a "$TMP/src/." libs/hbb_common/
echo "==> файлы обновлены"

"$REPO_ROOT/local/brand_hbb_common.sh"
echo "==> готово. Проверьте git diff, затем закоммитьте."

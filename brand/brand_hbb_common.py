#!/usr/bin/env python3
"""
Накладывает брендинг NetControl на свежевендоренный libs/hbb_common.

Правок всего четыре, и все - подмена константы. Отдельным патчем их держать
нельзя: upstream часто двигает соседние строки, и патч перестаёт применяться,
а поиск по точной строке переживает это спокойно. Если строка не найдена,
скрипт падает с внятной ошибкой: значит upstream переименовал константу и
брендинг надо пересмотреть, а не молча собрать неотбрендированный клиент.
"""
import re
import sys
from pathlib import Path

CONFIG = Path(__file__).resolve().parent.parent / 'libs' / 'hbb_common' / 'src' / 'config.rs'

EDITS = [
    (
        'pub static ref PROD_RENDEZVOUS_SERVER: RwLock<String> = RwLock::new("".to_owned());',
        '// Ребрендинг: значение по умолчанию НЕ пустое - тогда\n'
        '    // get_custom_rendezvous_server()/get_api_server_() в src/common.rs по всей\n'
        '    // цепочке (адресная книга, API, проверка "публичный ли сервер") считают наш\n'
        '    // адрес настроенным пользователем, а не только там, где патчили точечно.\n'
        '    pub static ref PROD_RENDEZVOUS_SERVER: RwLock<String> = RwLock::new("PLACEHOLDER_SERVER".to_owned());',
        'адрес relay-сервера по умолчанию',
    ),
    (
        'pub static ref APP_NAME: RwLock<String> = RwLock::new("RustDesk".to_owned());',
        '// Ребрендинг: только ASCII - значение уходит в пути (папки логов и\n'
        '    // конфига), в имя службы Windows и в ярлыки, где кириллица рискованна.\n'
        '    pub static ref APP_NAME: RwLock<String> = RwLock::new("NetControl".to_owned());',
        'имя приложения',
    ),
    (
        'pub static ref BUILTIN_SETTINGS: RwLock<HashMap<String, String>> = Default::default();',
        '// Ребрендинг: hide-powered-by-me включён по умолчанию. У upstream эта\n'
        '    // опция ставится только через подписанный custom-client конфиг, которым мы\n'
        '    // не пользуемся; убирает виджет "Основано на RustDesk" и ссылку на\n'
        '    // rustdesk.com (см. flutter/lib/common.dart::loadPowered()).\n'
        '    pub static ref BUILTIN_SETTINGS: RwLock<HashMap<String, String>> = RwLock::new(HashMap::from([("hide-powered-by-me".to_owned(), "Y".to_owned())]));',
        'встроенные настройки (скрытие "powered by")',
    ),
]

# Реальный адрес и ключ в публикуемый репозиторий не попадают - подставляются
# перед сборкой (local/apply_local_server.sh), как local_settings.py в Django.
REGEX_EDITS = [
    (
        re.compile(r'pub const RENDEZVOUS_SERVERS: &\[&str\] = &\[[^\]]*\];'),
        'pub const RENDEZVOUS_SERVERS: &[&str] = &["PLACEHOLDER_SERVER"];',
        'список relay-серверов',
    ),
    (
        re.compile(r'pub const RS_PUB_KEY: &str = "[^"]*";'),
        'pub const RS_PUB_KEY: &str = "PLACEHOLDER_PUB_KEY";',
        'публичный ключ сервера',
    ),
]


def main():
    if not CONFIG.exists():
        sys.exit('Не найден %s' % CONFIG)
    text = CONFIG.read_text(encoding='utf-8')
    applied = []

    for needle, replacement, label in EDITS:
        if needle not in text:
            if replacement.split('\n')[-1].strip() in text:
                applied.append('%s: уже наложено' % label)
                continue
            sys.exit(
                'НЕ НАЙДЕНА строка для правки "%s".\n'
                'Искали: %s\n'
                'Upstream изменил эту константу - брендинг надо пересмотреть вручную.'
                % (label, needle)
            )
        text = text.replace(needle, replacement, 1)
        applied.append('%s: ок' % label)

    for pattern, replacement, label in REGEX_EDITS:
        text, n = pattern.subn(replacement, text, count=1)
        if not n:
            sys.exit('НЕ НАЙДЕНА константа "%s" - брендинг надо пересмотреть вручную.' % label)
        applied.append('%s: ок' % label)

    CONFIG.write_text(text, encoding='utf-8')
    for line in applied:
        print('   ' + line)
    print('==> брендинг hbb_common наложен')


if __name__ == '__main__':
    main()

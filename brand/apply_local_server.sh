#!/bin/sh
# Подставляет РЕАЛЬНЫЙ адрес/ключ вашего relay-сервера в config.rs перед
# сборкой - НЕ коммитится (см. /local/ в .gitignore), аналог
# local_settings.py в Django-проекте. Запускать из корня репозитория:
#   ./local/apply_local_server.sh <host> <public_key>
set -e
HOST="${1:?usage: apply_local_server.sh <host> <public_key>}"
PUB_KEY="${2:?usage: apply_local_server.sh <host> <public_key>}"
CONFIG_RS="libs/hbb_common/src/config.rs"

sed -i "s/pub const RENDEZVOUS_SERVERS: &\[&str\] = &\[\"[^\"]*\"\];/pub const RENDEZVOUS_SERVERS: \&[\&str] = \&[\"$HOST\"];/" "$CONFIG_RS"
sed -i "s/pub const RS_PUB_KEY: &str = \"[^\"]*\";/pub const RS_PUB_KEY: \&str = \"$PUB_KEY\";/" "$CONFIG_RS"
sed -i "s/PROD_RENDEZVOUS_SERVER: RwLock<String> = RwLock::new(\"[^\"]*\".to_owned());/PROD_RENDEZVOUS_SERVER: RwLock<String> = RwLock::new(\"$HOST\".to_owned());/" "$CONFIG_RS"

echo "OK: RENDEZVOUS_SERVERS, RS_PUB_KEY, PROD_RENDEZVOUS_SERVER -> $HOST"

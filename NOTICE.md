# NOTICE

This is a modified version of [RustDesk](https://github.com/rustdesk/rustdesk),
originally created by Purslane Tech Pte. Ltd. and the RustDesk contributors,
licensed under the GNU Affero General Public License v3.0 (see `LICENCE`).

## Modifications made in this fork (2026-08-11)

- Application name and branding changed from "RustDesk" to "MoyaInfra"
  (`libs/hbb_common/src/config.rs`: `APP_NAME`).
- Default rendezvous/relay server changed to a self-hosted server instead of
  RustDesk's public network (`libs/hbb_common/src/config.rs`:
  `RENDEZVOUS_SERVERS`, `RS_PUB_KEY`, `PROD_RENDEZVOUS_SERVER`). The real
  server address/key are applied at build time via `local/apply_local_server.sh`
  and are intentionally excluded from this repository (see `.gitignore`);
  the values committed here are placeholders.
- All application icons, tray icons, and the desktop launcher entry
  (`res/*.png`, `res/*.ico`, `res/scalable.svg`, `res/rustdesk.desktop`,
  `flutter/assets/icon.svg`) replaced with the operator's own logo.
- Added an in-app logo (`flutter/assets/logo_light.png`,
  `flutter/assets/logo_dark.png`) shown in the desktop client's side panel.
- Accent/button color palette changed throughout the Flutter UI
  (`flutter/lib/common.dart`'s `MyTheme` class, and a handful of additional
  hardcoded gradient/border colors in `flutter/lib/desktop/`) from RustDesk's
  default blue to the operator's brand color (`#2E7CF6`).
- Removed links to `rustdesk.com` (Website, Privacy Statement, public-server
  upsell banner) from the Settings/About screen and the connection page.
- Added a "Source Code (AGPL-3.0)" link on the About screen pointing to this
  repository, to satisfy AGPL-3.0 §13 (network use) and §6 (conveying).
- Upstream copyright notices and the AGPL-3.0 license text (`LICENCE`) were
  **not** modified or removed.

No changes were made to the core remote-desktop protocol, encryption, or
connection logic beyond the default server address above.

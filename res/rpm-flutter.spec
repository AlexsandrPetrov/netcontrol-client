Name:       netcontrol
Version:    1.4.9
Release:    0
Summary:    Удалённый доступ NetControl
License:    AGPL-3.0
URL:        https://tehalex.ru
Vendor:     NetControl
Requires:   gtk3 libxcb libXfixes alsa-lib libva pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
Клиент удалённого доступа NetControl.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/netcontrol" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/netcontrol"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/netcontrol.service -t "%{buildroot}/usr/share/netcontrol/files"
install -Dm 644 $HBB/res/netcontrol.desktop -t "%{buildroot}/usr/share/netcontrol/files"
install -Dm 644 $HBB/res/netcontrol-link.desktop -t "%{buildroot}/usr/share/netcontrol/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/netcontrol.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/netcontrol.svg"

%files
/usr/share/netcontrol/*
/usr/share/netcontrol/files/netcontrol.service
/usr/share/icons/hicolor/256x256/apps/netcontrol.png
/usr/share/icons/hicolor/scalable/apps/netcontrol.svg
/usr/share/netcontrol/files/netcontrol.desktop
/usr/share/netcontrol/files/netcontrol-link.desktop

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop netcontrol || true
  ;;
esac

%post
cp /usr/share/netcontrol/files/netcontrol.service /etc/systemd/system/netcontrol.service
cp /usr/share/netcontrol/files/netcontrol.desktop /usr/share/applications/
cp /usr/share/netcontrol/files/netcontrol-link.desktop /usr/share/applications/
ln -sf /usr/share/netcontrol/netcontrol /usr/bin/netcontrol
systemctl daemon-reload
systemctl enable netcontrol
systemctl start netcontrol
update-desktop-database
gtk-update-icon-cache -f -t /usr/share/icons/hicolor >/dev/null 2>&1 || true

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop netcontrol || true
    systemctl disable netcontrol || true
    rm /etc/systemd/system/netcontrol.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/bin/netcontrol || true
    rmdir /usr/lib/netcontrol || true
    rmdir /usr/local/netcontrol || true
    rmdir /usr/share/netcontrol || true
    rm /usr/share/applications/netcontrol.desktop || true
    rm /usr/share/applications/netcontrol-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/netcontrol || true
    rmdir /usr/local/netcontrol || true
  ;;
esac

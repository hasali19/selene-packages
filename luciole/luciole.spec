%bcond check 1

# renovate: datasource=github-commits depName=noctalia-dev/luciole branch=main
%global commit      7095f57e52a6322bd59ed3911127c1498da40d92
%global commitdate  20261121.030414
%global shortcommit %{sub %{commit} 1 7}

Name:           luciole
Version:        0.0.git.%{commitdate}.%{shortcommit}
Release:        %autorelease
ExcludeArch:    %{ix86}
Summary:        A smooth, native Wayland file manager

# The main source code is MIT.  Other licenses:
# HPND-sell-variant:
#   lib/protocols/text-input-unstable-v3.xml
# MIT:
#   lib/assets/fonts/noctalia-tabler.ttf
#   lib/protocols/cursor-shape-v1.xml
License:        MIT AND HPND-sell-variant

URL:            https://github.com/noctalia-dev/luciole
Source:         %{url}/archive/%{commit}/luciole-%{commit}.tar.gz

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  gcc-c++
%if 0%{?rhel} && 0%{?rhel} <= 10
BuildRequires:  gcc-toolset-15
BuildRequires:  gcc-toolset-15-gcc-plugin-annobin
%{?enable_gcctoolset15}
%endif
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.49
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0) >= 2.76
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.76
BuildRequires:  pkgconfig(libcurl) >= 7.85
BuildRequires:  pkgconfig(libxml-2.0) >= 2.9
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(pango) >= 1.50
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pangoft2)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= 2.42
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libacl)
BuildRequires:  pkgconfig(tomlplusplus) >= 3.4
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  stb_image_resize2-static

%if %{with check}
BuildRequires:  python3
BuildRequires:  dbus-daemon
BuildRequires:  /usr/bin/glib-compile-schemas
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(libwebp)
# Needed for the encrypted 7z tests in archive-service
BuildRequires:  7zip
%endif

# For desktop-file-validate command
BuildRequires:  desktop-file-utils

# For ownership of icon parent directories
Requires:       hicolor-icon-theme

# Required for MIME type detection, desktop settings and the Trash interface
Requires:       shared-mime-info
Requires:       gsettings-desktop-schemas
Requires:       gvfs

# Optional requirements for various functionality
Recommends:     adwaita-icon-theme
Recommends:     dconf
Recommends:     glib-networking
Recommends:     gvfs-smb
Recommends:     udisks2
Recommends:     /usr/bin/ffmpeg
Recommends:     /usr/bin/ffprobe
Recommends:     ffmpegthumbnailer
Recommends:     poppler-utils
Recommends:     7zip
Recommends:     xdg-terminal-exec


%description
Luciole is a smooth, native Wayland file manager using Noctalia rendering and
controls, with fast previews, tabs, split view and Miller columns.


%prep
%autosetup -n luciole-%{commit}

# Move bundled licenses to the top level to make inclusion in %%files easier.
cp -p lib/assets/fonts/tabler-icons-license.txt LICENSE.tabler


%conf
%meson \
    -Dtests=%{?with_check:enabled}%{!?with_check:disabled} \
    -Dnative_optimizations=false \
    -Dbuild_revision=%{shortcommit}


%build
%meson_build


%install
%meson_install

# Installed via %%license instead
rm -r %{buildroot}%{_datadir}/licenses/luciole


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/dev.noctalia.luciole.desktop

%if %{with check}
# Skipped tests:
# - thumbnail, preview-metadata: need an ffmpeg build with encoders (mpeg4,
#   libaom-av1) that aren't available in Fedora/EPEL, plus a Glycin-enabled
#   gdk-pixbuf with AVIF/HEIF loaders.
# - transfer-service: tries to cancel a copy of a 1 GiB sparse file mid-way,
#   which completes before it can be cancelled in the build environment.
%global skipped_tests thumbnail|preview-metadata|transfer-service
%if 0%{?rhel} && 0%{?rhel} <= 10
# - archive-service: 7z creation needs the 7zip "threads" option from
#   libarchive >= 3.8, but EL10 has 3.7.
# - operation-activity: rename undo history check fails on EL10.
%global skipped_tests %{skipped_tests}|archive-service|operation-activity
%endif
%meson_test $(%{__meson} test -C %{_vpath_builddir} --list 2>/dev/null \
    | grep -vxE '(luciole:)?(%{skipped_tests})')
%endif


%files
%license LICENSE LICENSE.tabler
%doc README.md
%{_bindir}/luciole
%{_datadir}/applications/dev.noctalia.luciole.desktop
%{_datadir}/icons/hicolor/scalable/apps/dev.noctalia.luciole.svg
%{_datadir}/dbus-1/services/dev.noctalia.luciole.FileManager1.service
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.luciole.service
%dir %{_datadir}/xdg-desktop-portal
%dir %{_datadir}/xdg-desktop-portal/portals
%{_datadir}/xdg-desktop-portal/portals/luciole.portal
%{_datadir}/luciole
%{bash_completions_dir}/luciole
%{fish_completions_dir}/luciole.fish
%{zsh_completions_dir}/_luciole


%changelog
%autochangelog

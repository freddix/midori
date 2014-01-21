%bcond_with	gtk3

Summary:	Web browser based on GTK+ WebCore
Name:		midori
Version:	0.5.7
Release:	1
License:	GPL v2+
Group:		X11/Applications/Networking
Source0:	http://www.midori-browser.org/downloads/%{name}_%{version}_all_.tar.bz2
# Source0-md5:	93ceaa9b3b4a65f2a2738293440a8bf5
Patch0:		%{name}-link.patch
Patch1:		%{name}-certs.patch
URL:		http://www.midori-browser.org/
%if %{with gtk3}
BuildRequires:	gtk+3-devel
BuildRequires:	gtk+3-webkit-devel
BuildRequires:	libunique3-devel
%else
BuildRequires:	gtk+-devel
BuildRequires:	gtk+-webkit-devel
BuildRequires:	libunique-devel
%endif
BuildRequires:	libsoup-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkg-config
BuildRequires:	rsvg-convert
BuildRequires:	sqlite3-devel
BuildRequires:	xorg-libXScrnSaver-devel
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	ldconfig
Requires:	glib-networking
# HTML5 h264 playback
Suggests:	gstreamer-ffmpeg
Suggests:	gstreamer-plugins-bad
Suggests:	gstreamer-plugins-good
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Midori is a lightweight GTK+ web browser based on GTK+ WebCore. It
features tabs, windows and session management, bookmarks stored with
XBEL, searchbox based on OpenSearch, and user scripts support.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake ..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/no

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/ldconfig
%update_icon_cache hicolor

%postun
/usr/sbin/ldconfig
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README

%dir %{_libdir}/%{name}
%dir %{_sysconfdir}/xdg/midori
%dir %{_sysconfdir}/xdg/midori/extensions
%dir %{_sysconfdir}/xdg/midori/extensions/adblock

%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %ghost %{_libdir}/libmidori-core.so.1
%attr(755,root,root) %{_libdir}/libmidori-core.so.*.*.*
%attr(755,root,root) %{_libdir}/%{name}/*.so

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/midori/search
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/midori/extensions/adblock/config
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg


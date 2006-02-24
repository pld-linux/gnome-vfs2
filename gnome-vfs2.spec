#
# Conditional build
%bcond_without	gnome_mount	# enable gnome-mount support
#
Summary:	GNOME - virtual file system
Summary(pl):	GNOME - wirtualny system plików
Name:		gnome-vfs2
Version:	2.13.91
Release:	5.1
License:	LGPL v2+
Group:		Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-vfs/2.13/gnome-vfs-%{version}.tar.bz2
# Source0-md5:	a4e5e5acc6d5ce030c22106b4e5be8ea
Source1:	%{name}-defaults.list
Patch0:		%{name}-no_g_mime.patch
Patch1:		%{name}-fstab_edit_crash.patch
Patch2:		%{name}-disable_cdda.patch
Patch3:		%{name}-default_cdda_handler.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.12.0
BuildRequires:	ORBit2-devel >= 1:2.12.3
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	avahi-glib-devel >= 0.6
BuildRequires:	bzip2-devel
BuildRequires:	dbus-glib-devel >= 0.34
BuildRequires:	docbook-dtd412-xml >= 1.0-10
BuildRequires:	fam-devel
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.9.3
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gnome-doc-tools
%{?with_gnome_mount:BuildRequires:	gnome-mount-devel}
BuildRequires:	gtk+2-devel >= 2:2.6.3
BuildRequires:	gtk-doc >= 1.4
BuildRequires:	hal-devel >= 0.5.6
BuildRequires:	heimdal-devel >= 0.7
BuildRequires:	intltool >= 0.34.2
BuildRequires:	libbonobo-devel >= 2.10.1
BuildRequires:	libsmbclient-devel >= 3.0
BuildRequires:	libtool >= 2:1.5.14
BuildRequires:	libxml2-devel >= 2.6.21
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	zlib-devel
Requires(post,preun):	GConf2
Requires:	shared-mime-info >= 0.15
Obsoletes:	gnome-vfs-extras
Obsoletes:	gnome-vfs2-vfolder-menu
Conflicts:	gnome-vfs2-module-menu <= 0.8-1
Conflicts:	libgnome < 2.5.1
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME Virtual File System.

%description -l pl
Wirtualny Systemu Plików GNOME.

%package libs
Summary:	gnome-vfs library
Summary(pl):	Biblioteka gnome-vfs
Group:		Development/Libraries
Requires:	hal-libs >= 0.5.6
Requires:	libbonobo >= 2.10.1

%description libs
This package contains gnome-vfs libraries.

%description libs -l pl
Pakiet zawiera biblioteki gnome-vfs.

%package devel
Summary:	gnome-vfs - header files
Summary(pl):	gnome-vfs - pliki nag³ówkowe
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	GConf2-devel >= 2.12.0
Requires:	avahi-devel >= 0.6
Requires:	gtk-doc-common
Requires:	libbonobo-devel >= 2.10.1
Requires:	openssl-devel >= 0.9.7d

%description devel
This package contains header files for gnome-vfs library.

%description devel -l pl
Pakiet ten zawiera pliki nag³ówkowe biblioteki gnome-vfs.

%package static
Summary:	gnome-vfs - static libraries
Summary(pl):	gnome-vfs - biblioteki statyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static gnome-vfs libraries.

%description static -l pl
Pakiet ten zawiera biblioteki statyczne gnome-vfs.

%package apidocs
Summary:	gnome-vfs API documetation
Summary(pl):	Dokumentacja API gnome-vfs
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
gnome-vfs API documetation.

%description apidocs -l pl
Dokumentacja API gnome-vfs.

%prep
%setup -q -n gnome-vfs-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
# force rebuild
touch libgnomevfs/GNOME_VFS_Daemon.idl
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-howl \
	--disable-schemas-install \
	--%{?with_gnome_mount:en}%{!?with_gnome_mount:dis}able-gnome-mount \
	--enable-gtk-doc \
	--enable-ipv6 \
	--with-html-dir=%{_gtkdocdir}
	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4dir=%{_aclocaldir} \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

# no static modules
rm -f $RPM_BUILD_ROOT%{_libdir}/{gnome-vfs-2.0/modules,bonobo/monikers}/*.{la,a}
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/filesystems/*.{la,a}

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/defaults.list

%find_lang gnome-vfs-2.0

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install desktop_default_applications.schemas
%gconf_schema_install desktop_gnome_url_handlers.schemas
%gconf_schema_install system_dns_sd.schemas
%gconf_schema_install system_http_proxy.schemas
%gconf_schema_install system_smb.schemas
%gconf_schema_install system_storage.schemas

%preun
%gconf_schema_uninstall desktop_default_applications.schemas
%gconf_schema_uninstall desktop_gnome_url_handlers.schemas
%gconf_schema_uninstall system_dns_sd.schemas
%gconf_schema_uninstall system_http_proxy.schemas
%gconf_schema_uninstall system_smb.schemas
%gconf_schema_uninstall system_storage.schemas

%post	libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f gnome-vfs-2.0.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%{_sysconfdir}/gnome-vfs-2.0
%{_sysconfdir}/gconf/schemas/desktop_default_applications.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_url_handlers.schemas
%{_sysconfdir}/gconf/schemas/system_dns_sd.schemas
%{_sysconfdir}/gconf/schemas/system_http_proxy.schemas
%{_sysconfdir}/gconf/schemas/system_smb.schemas
%{_sysconfdir}/gconf/schemas/system_storage.schemas
%attr(755,root,root) %{_bindir}/gnomevfs-*
%attr(755,root,root) %{_libdir}/gnome-vfs-daemon
%dir %{_libdir}/gnome-vfs-2.0
%dir %{_libdir}/gnome-vfs-2.0/modules
%attr(755,root,root) %{_libdir}/gnome-vfs-2.0/modules/*.so
%{_libdir}/bonobo/servers/*
%attr(755,root,root) %{_libdir}/bonobo/monikers/*.so
%{_desktopdir}/*.list

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/gnome-vfs-2.0
%{_includedir}/gnome-vfs-module-2.0
%{_libdir}/gnome-vfs-2.0/include
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gnome-vfs-2.0

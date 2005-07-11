Summary:	GNOME2 - virtual file system
Summary(pl):	GNOME2 - wirtualny system plików
Name:		gnome-vfs2
Version:	2.11.4
Release:	1
License:	LGPL v2+
Group:		Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-vfs/2.11/gnome-vfs-%{version}.tar.bz2
# Source0-md5:	8aad72f70a3aa2257b9d4afd5e53da65
Source1:	%{name}-defaults.list
Patch0:		%{name}-defaults-path.patch
Patch1:		%{name}-no_g_mime.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.10.0
BuildRequires:	ORBit2-devel >= 1:2.12.1
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	cdparanoia-III-devel
BuildRequires:	dbus-glib-devel >= 0.34
BuildRequires:	docbook-dtd412-xml >= 1.0-10
BuildRequires:	fam-devel
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.6.2
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gnome-doc-tools
BuildRequires:	gtk+2-devel >= 2:2.6.2
BuildRequires:	gtk-doc >= 1.1
BuildRequires:	hal-devel >= 0.5.2
BuildRequires:	heimdal-devel
BuildRequires:	howl-devel >= 0.9.10
BuildRequires:	intltool >= 0.30
BuildRequires:	libbonobo-devel >= 2.8.1
BuildRequires:	libsmbclient-devel >= 3.0
BuildRequires:	libtool >= 2:1.5.14
BuildRequires:	libxml2-devel >= 2.6.0
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	zlib-devel
Requires(post):	/sbin/ldconfig
Requires(post,preun):	GConf2
Requires:	hal-libs >= 0.5.2
Requires:	howl-libs >= 0.9.10
Requires:	libbonobo >= 2.8.1
Requires:	shared-mime-info >= 0.15
Obsoletes:	gnome-vfs-extras
Obsoletes:	gnome-vfs2-vfolder-menu
Conflicts:	gnome-vfs2-module-menu <= 0.8-1
Conflicts:	libgnome < 2.5.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME2 Virtual File System library.

%description -l pl
Biblioteka Wirtualnego Systemu Plików GNOME2.

%package devel
Summary:	gnome-vfs2 - header files
Summary(pl):	gnome-vfs2 - pliki nag³ówkowe
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	GConf2-devel >= 2.10.0
Requires:	gtk-doc-common
Requires:	howl-devel >= 0.9.10
Requires:	libbonobo-devel >= 2.8.1
Requires:	openssl-devel >= 0.9.7d

%description devel
This package contains header files for gnome-vfs2 library.

%description devel -l pl
Pakiet ten zawiera pliki nag³ówkowe biblioteki gnome-vfs2.

%package static
Summary:	gnome-vfs2 - static libraries
Summary(pl):	gnome-vfs2 - biblioteki statyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static gnome-vfs2 libraries.

%description static -l pl
Pakiet ten zawiera biblioteki statyczne gnome-vfs2.

%prep
%setup -q -n gnome-vfs-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--disable-schemas-install \
	--enable-ipv6 \

# check -DMOUNT_ARGUMENT=\\\"-s\\\"" before 2.12
%{__make} CFLAGS="%{rpmcflags} -DMOUNT_ARGUMENT=\\\"-s\\\""

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
/sbin/ldconfig
%gconf_schema_install desktop_default_applications.schemas
%gconf_schema_install desktop_gnome_url_handlers.schemas
%gconf_schema_install system_dns_sd.schemas
%gconf_schema_install system_http_proxy.schemas
%gconf_schema_install system_smb.schemas

%preun
%gconf_schema_uninstall desktop_default_applications.schemas
%gconf_schema_uninstall desktop_gnome_url_handlers.schemas
%gconf_schema_uninstall system_dns_sd.schemas
%gconf_schema_uninstall system_http_proxy.schemas
%gconf_schema_uninstall system_smb.schemas

%postun -p /sbin/ldconfig

%files -f gnome-vfs-2.0.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%{_sysconfdir}/gnome-vfs-2.0
%{_sysconfdir}/gconf/schemas/*
%attr(755,root,root) %{_bindir}/gnomevfs-*
%attr(755,root,root) %{_libdir}/gnome-vfs-daemon
%attr(755,root,root) %{_libdir}/*.so.*.*
%dir %{_libdir}/gnome-vfs-2.0
%dir %{_libdir}/gnome-vfs-2.0/modules
%attr(755,root,root) %{_libdir}/gnome-vfs-2.0/modules/*.so
%{_libdir}/bonobo/servers/*
%attr(755,root,root) %{_libdir}/bonobo/monikers/*.so
%{_desktopdir}/*.list

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/gnome-vfs-2.0
%{_includedir}/gnome-vfs-module-2.0
%{_libdir}/gnome-vfs-2.0/include
%{_pkgconfigdir}/*.pc
%{_gtkdocdir}/gnome-vfs-2.0

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

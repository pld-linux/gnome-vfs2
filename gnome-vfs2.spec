#
# Conditional build:
%bcond_without	hal	# don't use hal
#
Summary:	GNOME2 - virtual file system
Summary(pl):	GNOME2 - wirtualny system plików
Name:		gnome-vfs2
Version:	2.10.0
Release:	1
License:	LGPL
Group:		Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-vfs/2.10/gnome-vfs-%{version}.tar.bz2
# Source0-md5:	bb9df65d6a77414bbde9f1bc429c9d97
Source1:	%{name}-defaults.list
Patch0:		%{name}-defaults-path.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.10.0
BuildRequires:	ORBit2-devel >= 1:2.12.1
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	cdparanoia-III-devel
%{?with_hal:BuildRequires:	dbus-glib-devel >= 0.23}
BuildRequires:	docbook-dtd412-xml >= 1.0-10
BuildRequires:	fam-devel
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.6.2
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gnome-doc-tools
BuildRequires:	gnome-mime-data-devel >= 2.4.1
BuildRequires:	gtk+2-devel >= 2:2.6.2
BuildRequires:	gtk-doc >= 1.1
%{?with_hal:BuildRequires:	hal-devel >= 0.4.7}
BuildRequires:	heimdal-devel
BuildRequires:	howl-devel >= 0.9.6-2
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
BuildRequires:	zlib-devel
Requires:	desktop-file-utils >= 0.9
%{?with_hal:Requires:	hal-libs >= 0.4.7}
Requires:	howl-libs >= 0.9.6-2
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
Requires:	howl-devel >= 0.9.6-2
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
%if %{with hal}
	--enable-hal
%else
	--disable-hal
%endif
%{__make} CFLAGS="%{rpmcflags} -DMOUNT_ARGUMENT=\\\"-s\\\""

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4dir=%{_aclocaldir} \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

# no static modules
rm -f $RPM_BUILD_ROOT%{_libdir}/{gnome-vfs-2.0/modules,bonobo/monikers}/*.{la,a}
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/filesystems/*.{la,a}

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

install -d $RPM_BUILD_ROOT%{_datadir}/gnome/applications
install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/gnome/applications/defaults.list

%find_lang gnome-vfs-2.0

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%gconf_schema_install

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
%dir %{_datadir}/gnome/applications
%{_datadir}/gnome/applications/defaults.list

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

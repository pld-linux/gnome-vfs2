Summary:	GNOME2 - virtual file system
Summary(pl):	GNOME2 - wirtualny system plików
Name:		gnome-vfs2
Version:	2.0.1
Release:	2
License:	GPL
Group:		X11/Applications
Source0:	ftp://ftp.gnome.org/pub/GNOME/pre-gnome2/sources/gnome-vfs/gnome-vfs-%{version}.tar.bz2
Patch0:		%{name}-am15.patch
Patch1:		%{name}-rm_GNOME_COMMON_INIT_and_GNOME_PLATFORM_GNOME_2.patch
Patch2:		%{name}-applnk.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 1.2.0
BuildRequires:	ORBit2-devel >= 2.4.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bonobo-activation-devel >= 1.0.0
BuildRequires:	bzip2-devel
BuildRequires:	fam-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 2.0.3
BuildRequires:	gnome-mime-data-devel >= 2.0.0
BuildRequires:	libbonobo-devel >= 2.0.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.4.22
BuildRequires:	openssl-devel >= 0.9.6d
BuildRequires:	zlib-devel
BuildRequires:	gnome-common
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_sysconfdir	/etc/X11/GNOME2
%define		_gtkdocdir	/usr/share/doc/gtk-doc/html

%description
GNOME2 Virtual File System library.

%description -l pl
Biblioteka Wirtualnego Systemu Plików GNOME2.

%package devel
Summary:	gnome-vfs2 - header files
Summary(pl):	gnome-vfs2 - pliki nag³ówkowe
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}

%description devel
This package contains header files for gnome-vfs2 library.

%description devel -l pl
Pakiet ten zawiera pliki nag³ówkowe biblioteki gnome-vfs2.

%package static
Summary:	gnome-vfs2 - static libraries
Summary(pl):	gnome-vfs2 - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
This package contains static gnome-vfs2 libraries.

%description static -l pl
Pakiet ten zawiera biblioteki statyczne gnome-vfs2.

%prep
%setup -q -n gnome-vfs-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
rm -f missing
%{__libtoolize}
aclocal -I %{_aclocaldir}/gnome2-macros
%{__autoconf}
%{__automake}
%configure \
	--disable-gtk-doc
%{__make}

gzip -9nf AUTHORS ChangeLog NEWS README

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

%find_lang gnome-vfs-2.0

%clean
rm -rf $RPM_BUILD_ROOT

%post   
/sbin/ldconfig
GCONF_CONFIG_SOURCE="" /usr/X11R6/bin/gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/*.schemas > /dev/null

%postun -p /sbin/ldconfig

%files -f gnome-vfs-2.0.lang
%defattr(644,root,root,755)
%doc *.gz
%{_sysconfdir}/gnome-vfs-2.0
%{_sysconfdir}/gconf/schemas/*
%attr(755,root,root) %{_libdir}/*.so.*.*
%dir %{_libdir}/gnome-vfs-2.0
%dir %{_libdir}/gnome-vfs-2.0/modules
%attr(755,root,root) %{_libdir}/gnome-vfs-2.0/modules/*.??
%attr(755,root,root) %{_libdir}/vfs
%{_libdir}/bonobo/servers/*
%{_libdir}/bonobo/monikers/*.??

%files devel
%defattr(644,root,root,755)
%doc %{_gtkdocdir}/gnome-vfs-2.0
%attr(755,root,root) %{_libdir}/*.so
%attr(755,root,root) %{_libdir}/*.la
%{_includedir}/gnome-vfs-2.0
%{_includedir}/gnome-vfs-module-2.0
%{_libdir}/gnome-vfs-2.0/include
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_libdir}/gnome-vfs-2.0/modules/*.a

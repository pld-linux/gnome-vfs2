Summary:	GNOME2 - virtual file system
Summary(pl):	GNOME2 - wirtualny system plików
Name:		gnome-vfs2
Version:	1.9.15
Release:	0.1
License:	GPL
Group:		X11/Applications
Source0:	ftp://ftp.gnome.org:/pub/GNOME/pre-gnome2/sources/gnome-vfs/gnome-vfs-%{version}.tar.bz2
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 1.1.10
BuildRequires:	ORBit2-devel >= 2.3.108
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bonobo-activation-devel >= 0.9.8
BuildRequires:	bzip2-devel
BuildRequires:	fam-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 2.0.2
BuildRequires:	gnome-mime-data-devel >= 1.0.8
BuildRequires:	libbonobo-devel >= 0.116.0
BuildRequires:	libtool >= 1.4.2-10
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_sysconfdir	/etc/X11/GNOME2

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

%build
#rm -f missing acinclude.m4
libtoolize --copy --force
#aclocal
autoconf
#automake -a -c -f
%configure \
	--disable-gtk-doc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

gzip -9nf AUTHORS ChangeLog NEWS README

%find_lang gnome-vfs-2.0

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f gnome-vfs-2.0.lang
%defattr(644,root,root,755)
%doc *.gz
#%{_datadir}/gtk-doc/html/gnome-vfs-2.0
%{_sysconfdir}/gnome-vfs-2.0
%attr(755,root,root) %{_libdir}/*.so.*.*
%dir %{_libdir}/gnome-vfs-2.0
%dir %{_libdir}/gnome-vfs-2.0/modules
%attr(755,root,root) %{_libdir}/gnome-vfs-2.0/modules/*.??
%attr(755,root,root) %{_libdir}/vfs
%{_libdir}/bonobo/servers/*
%{_libdir}/bonobo/monikers/*.??

%files devel
%defattr(644,root,root,755)
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

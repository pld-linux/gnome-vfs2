Summary:	GNOME2 - virtual file system
Summary(pl):	GNOME2 - wirtualny system plików
Name:		gnome-vfs2
Version:	2.0.4.1
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-vfs/2.0/gnome-vfs-%{version}.tar.bz2
Patch0:		%{name}-am15.patch
Patch1:		%{name}-rm_GNOME_COMMON_INIT_and_GNOME_PLATFORM_GNOME_2.patch
Patch2:		%{name}-applnk.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 1.2.1
BuildRequires:	ORBit2-devel >= 2.4.3
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bonobo-activation-devel >= 1.0.0
BuildRequires:	bzip2-devel
BuildRequires:  docbook-dtd412-xml >= 1.0-10 
# install stage fails with docbook-dtd412-xml-1.0-8
BuildRequires:	fam-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 2.0.6
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-tools
BuildRequires:	gnome-mime-data-devel >= 2.0.1
BuildRequires:	gtk-doc >= 0.9-6
BuildRequires:	libbonobo-devel >= 2.0.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.4.24
BuildRequires:	openssl-devel >= 0.9.6d
BuildRequires:	zlib-devel
BuildConflicts:	bonobo-activation-devel >= 2.1.0
Requires:	bonobo-activation >= 1.0.0
Conflicts:	bonobo-activation >= 2.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/X11/GNOME2
%define		_gtkdocdir	%{_defaultdocdir}/gtk-doc/html

%description
GNOME2 Virtual File System library.

%description -l pl
Biblioteka Wirtualnego Systemu Plików GNOME2.

%package devel
Summary:	gnome-vfs2 - header files
Summary(pl):	gnome-vfs2 - pliki nag³ówkowe
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}
Requires:	gnome-mime-data-devel
Requires:	gtk-doc-common
Requires:	libbonobo-devel
Requires:	libxml2-devel
Requires:	openssl-devel

%description devel
This package contains header files for gnome-vfs2 library.

%description devel -l pl
Pakiet ten zawiera pliki nag³ówkowe biblioteki gnome-vfs2.

%package static
Summary:	gnome-vfs2 - static libraries
Summary(pl):	gnome-vfs2 - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}
Requires:	libbonobo-static
Requires:	libxml2-static

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
%{__aclocal} -I %{_aclocaldir}/gnome2-macros
%{__autoconf}
%{__automake}
%configure \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}
%{__make}

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
GCONF_CONFIG_SOURCE="`/usr/X11R6/bin/gconftool-2 --get-default-source`" /usr/X11R6/bin/gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/*.schemas > /dev/null

%postun -p /sbin/ldconfig

%files -f gnome-vfs-2.0.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
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
%{_libdir}/*.la
%{_includedir}/gnome-vfs-2.0
%{_includedir}/gnome-vfs-module-2.0
%{_libdir}/gnome-vfs-2.0/include
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_libdir}/gnome-vfs-2.0/modules/*.a
%{_libdir}/bonobo/monikers/*.a

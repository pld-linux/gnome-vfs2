Summary:	GNOME2 - virtual file system
Summary(pl):	GNOME2 - wirtualny system plików
Name:		gnome-vfs2
Version:	2.3.3
Release:	1
License:	GPL
Group:		Applications
# Source0-md5:	e589b2a23f961f1596a3b294a6437f98
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-vfs/2.3/gnome-vfs-%{version}.tar.bz2
Patch0:		%{name}-applnk.patch
#Patch1:		%{name}-locale-sr.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.2.0
BuildRequires:	ORBit2-devel >= 2.7.1
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:  docbook-dtd412-xml >= 1.0-10 
BuildRequires:	fam-devel
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 2.2.0
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-tools
BuildRequires:	gnome-mime-data-devel >= 2.0.1-3
BuildRequires:	gtk-doc >= 0.9-6
BuildRequires:	libbonobo-devel >= 2.3.1-4
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.5.1
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	zlib-devel
Requires:	libbonobo >= 2.3.1-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME2 Virtual File System library.

%description -l pl
Biblioteka Wirtualnego Systemu Plików GNOME2.

%package devel
Summary:	gnome-vfs2 - header files
Summary(pl):	gnome-vfs2 - pliki nag³ówkowe
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	GConf2-devel
Requires:	gtk-doc-common
Requires:	openssl-devel >= 0.9.7

%description devel
This package contains header files for gnome-vfs2 library.

%description devel -l pl
Pakiet ten zawiera pliki nag³ówkowe biblioteki gnome-vfs2.

%package static
Summary:	gnome-vfs2 - static libraries
Summary(pl):	gnome-vfs2 - biblioteki statyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
This package contains static gnome-vfs2 libraries.

%description static -l pl
Pakiet ten zawiera biblioteki statyczne gnome-vfs2.

%prep
%setup -q -n gnome-vfs-%{version}
%patch0 -p1
#%patch1 -p1

# sr_YU is latin2, sr_YU@cyrillic is cyrillic in glibc
#mv -f po/{sr.po,sr@cyrillic.po}
#mv -f po/{sr@Latn.po,sr.po}

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
	m4dir=%{_aclocaldir}

# no static modules
rm -f $RPM_BUILD_ROOT%{_libdir}/{gnome-vfs-2.0/modules,bonobo/monikers}/*.a

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
%attr(755,root,root) %{_libdir}/*.so.*.*
%dir %{_libdir}/gnome-vfs-2.0
%dir %{_libdir}/gnome-vfs-2.0/modules
%attr(755,root,root) %{_libdir}/gnome-vfs-2.0/modules/*.so
%{_libdir}/gnome-vfs-2.0/modules/*.la
%attr(755,root,root) %{_libdir}/vfs
%{_libdir}/bonobo/servers/*
%attr(755,root,root) %{_libdir}/bonobo/monikers/*.so
%{_libdir}/bonobo/monikers/*.la

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

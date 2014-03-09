Summary:	musl libc - new standard library to power a new generation of Linux-based devices
Summary(pl.UTF-8):	musl libc - nowa biblioteka standardowa dla urządzeń linuksowych nowej generacji
Name:		musl
Version:	0.9.15
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://www.musl-libc.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	06f590a38c85722ee9343db2416425f4
URL:		http://www.musl-libc.org/
BuildRequires:	gcc >= 5:3.2
BuildRequires:	zlib-devel
Requires:	uname(release) >= 2.6.0
ExclusiveArch:	%{ix86} %{x8664} arm mips microblaze ppc
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_prefix}/%{_lib}/musl
%define		_includedir	%{_prefix}/include/musl
%define		_fortify_cflags	%{nil}
%define		_ssp_cflags	%{nil}

# i386, x86_64, arm, mips, microblaze, ppc
%define		musl_arch	%{_target_base_arch}

%description
musl libc is a new standard library to power a new generation of
Linux-based devices. It is lightweight, fast, simple, free, and
strives to be correct in the sense of standards-conformance and
safety.

musl is an alternative to glibc, uClibc, dietlibc, and klibc.

%description -l pl.UTF-8
musl libc to nowa biblioteka standardowa, przeznaczona do zasilania
urządzeń linuksowych nowej generacji. Jest lekka, szybka, prosta,
wolnodostępna i stara się być poprawna w sensie zgodności ze
standardami i bezpieczeństwa.

musl jest alternatywą dla bibliotek glibc, uClibc, dietlibc i klibc.

%package devel
Summary:	Development files for musl libc
Summary(pl.UTF-8):	Pliki programistyczne biblioteki musl libc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for musl libc.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki musl libc.

%prep
%setup -q

%build
%configure \
	--syslibdir=/%{_lib}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}
echo '%{_libdir}' > $RPM_BUILD_ROOT%{_sysconfdir}/ld-musl-%{musl_arch}.path

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT INSTALL README WHATSNEW
%attr(755,root,root) /%{_lib}/ld-musl-%{musl_arch}.so.1
%dir %{_libdir}
%attr(755,root,root) %{_libdir}/libc.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ld-musl-%{musl_arch}.path

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/musl-gcc
%{_libdir}/libc.a
# empty stubs
%{_libdir}/libcrypt.a
%{_libdir}/libdl.a
%{_libdir}/libm.a
%{_libdir}/libpthread.a
%{_libdir}/libresolv.a
%{_libdir}/librt.a
%{_libdir}/libutil.a
%{_libdir}/libxnet.a
# crts
%{_libdir}/Scrt1.o
%{_libdir}/crt*.o
%{_libdir}/musl-gcc.specs
%{_includedir}

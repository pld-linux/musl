Summary:	musl libc - new standard library to power a new generation of Linux-based devices
Summary(pl.UTF-8):	musl libc - nowa biblioteka standardowa dla urządzeń linuksowych nowej generacji
Name:		musl
Version:	1.2.5
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://musl.libc.org/releases.html
Source0:	https://musl-libc.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	ac5cfde7718d0547e224247ccfe59f18
Patch0:		%{name}-gcc.patch
URL:		http://www.musl-libc.org/
BuildRequires:	gcc >= 5:3.2
BuildRequires:	rpmbuild(macros) >= 2.007
BuildRequires:	zlib-devel
Requires:	uname(release) >= 2.6.0
ExclusiveArch:	%{ix86} %{x8664} x32 %{arm} aarch64 loongarch64 mips microblaze ppc riscv32
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_prefix}/%{_lib}/musl
%define		_includedir	%{_prefix}/include/musl
%define		_fortify_cflags	%{nil}
%define		_ssp_cflags	%{nil}

%ifarch x32
%define		musl_arch	x32
%endif
%ifarch %{arm32_with_hf}
%define		musl_arch	armhf
%endif
%ifnarch x32 %{arm32_with_hf}
%define		musl_arch	%{_target_base_arch}
%endif

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
%patch0 -p1

%build
%configure \
	--syslibdir=/%{_lib}

# WRAPCC_GCC that will be used as $REALGCC fallback in musl-gcc script
# regardless what is value when this package is built (ccache, etc)
%{__make} \
	WRAPCC_GCC="%{_target_platform}-gcc"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# move actual library to /lib to handle /usr mounts
mv $RPM_BUILD_ROOT{%{_libdir}/libc.so,/%{_lib}/ld-musl-%{musl_arch}.so.1}
ln -s /%{_lib}/ld-musl-%{musl_arch}.so.1 $RPM_BUILD_ROOT%{_libdir}/libc.so

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
%{_libdir}/rcrt1.o
%{_libdir}/musl-gcc.specs
%{_includedir}

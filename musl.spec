Summary:	Development files for musl libc
Name:		musl
Version:	0.8.9
Release:	0.1
Source0:	http://www.etalabs.net/musl/releases/%{name}-%{version}.tar.gz
# Source0-md5:	1dfb3ba92ec08073bb982efc60b058cb
License:	LGPL v2+
Group:		Development/Libraries
URL:		http://www.etalabs.net/musl/
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
musl is a new standard library to power Linux-based devices. It is
lightweight, fast, simple, free, and strives to be correct in the
sense of standards-conformance and safety.

%package devel
Summary:	Development files for %{name}
License:	LGPL v2+
Group:		Development/Libraries

%description devel
Development files and headers for %{name}.

%prep
%setup -q

%build
sed -i -e 's!/usr/local!/usr/lib!' config.mak
# set arch:
%ifnarch %{ix86}
sed -i -e "s/i386/%{_arch}/" config.mak
%endif
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_prefix}/lib/bin $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc INSTALL README WHATSNEW
%{_prefix}/lib/musl
%attr(755,root,root) %{_bindir}/*

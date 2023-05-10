Name:           libsmi
Version:        0.4.8
Release:        26
Summary:        A library to access SMI MIB information
License:        GPLv2+ and BSD
URL:            http://www.ibr.cs.tu-bs.de/projects/libsmi/index.html
Source0:        https://www.ibr.cs.tu-bs.de/projects/libsmi/download/%{name}-%{version}.tar.gz
Source1:        smi.conf
Source2:	    IETF-MIB-LICENSE.txt
Patch0:		    libsmi-0.4.8-wget111.patch
Patch1:		    libsmi-0.4.8-CVE-2010-2891.patch
Patch2:		    libsmi-0.4.8-symbols-clash.patch
Patch3:		    libsmi-0.4.8-format-security-fix.patch

BuildRequires:  libtool flex bison
Requires:       gawk wget

%description
The core of the libsmi distribution is a library that allows management
applications to access SMI MIB module definitions. On top of this library,
there are tools to check, analyze dump, convert, and compare MIB
definitions. Finally, the distribution contains a steadily maintained and
revised archive of all IETF and IANA maintained standard MIB and PIB modules.


%package        devel
Summary:        Development environment for libsmi library
Requires:       %name = %version-%release
Requires:       pkgconfig

%description    devel
This package contains development files needed to develop
libsmi-based applications.

%package_help


%prep
%autosetup -p1
cp %{SOURCE2} .

%build
CFLAGS="$CFLAGS -Wno-int-conversion"; export CFLAGS
%configure --enable-smi --enable-sming --enable-shared --disable-static
%make_build LIBTOOL=/usr/bin/libtool

iconv -f latin1 -t utf-8 <COPYING >COPYING.utf8
mv COPYING.utf8 COPYING

%install
%make_install

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/smi.conf

%delete_la_and_a

%check
make check ||:
%ldconfig_scriptlets


%files
%license COPYING IETF-MIB-LICENSE.txt
%config(noreplace) %{_sysconfdir}/smi.conf
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/mibs/
%{_datadir}/pibs/

%files devel
%{_datadir}/aclocal/libsmi.m4
%{_libdir}/pkgconfig/libsmi.pc
%{_libdir}/*.so
%{_includedir}/*

%files help
%doc ANNOUNCE ChangeLog README THANKS TODO
%doc doc/draft-irtf-nmrg-sming-02.txt smi.conf-example
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Wed May 10 2023 Xiaoya Huang <huangxiaoya@iscas.ac.cn> - 0.4.8-26
- Fix clang building errors

* Tue Sep 15 2020 Ge Wang <wangge20@huawei.com> - 0.4.8-25
- Modify Source0 Url

* Tue Nov 19 2019 mengxian <mengxian@huawei.com> - 0.4.8-24
- Package init

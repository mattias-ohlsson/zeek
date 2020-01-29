#
# spec file for package Zeek
#
# Copyright (c) 1995-2014 The Regents of the University of California
# through the Lawrence Berkeley National Laboratory and the
# International Computer Science Institute. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# (1) Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
# (2) Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
# (3) Neither the name of the University of California, Lawrence Berkeley
#     National Laboratory, U.S. Dept. of Energy, International Computer
#     Science Institute, nor the names of contributors may be used to endorse
#     or promote products derived from this software without specific prior
#     written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Note that some files in the distribution may carry their own copyright
# notices.
Name:           zeek
Version:        3.0.1
Release:        1.1
Summary:        Zeek is a powerful framework for network analysis and security monitoring
Group:          Productivity/Networking/Diagnostic

License:        BSD-3-Clause
URL:            http://zeek.org
Source0:        https://www.zeek.org/downloads/%{name}-%{version}.tar.gz
Patch0:         install-symlink-old-cmake.patch
Patch1:         libdir.patch
%if 0%{?centos_version} == 600 || 0%{?scientificlinux_version} == 600 || 0%{?rhel_version} == 505
Patch2:         cmake-2.6.patch
%endif
%if 0%{?fedora_version} == 30
Patch2:         python3-patch.patch
%endif
Requires:       zeek-core = %{version}
Requires:       zeekctl = %{version}
Requires(pre):  /usr/sbin/groupadd, /usr/bin/getent

%if %{defined rhel_version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif

%define _prefix /opt/zeek
%define _sysconfdir %{_prefix}/etc
%define _libdir %{_prefix}/lib
%define _mandir %{_prefix}/share/man

%if 0%{?suse_version}
%define __cmake /usr/bin/cmake
%endif

%description
Zeek is a powerful network analysis framework that is much different from the
typical IDS you may know.  While focusing on network security monitoring, Zeek
provides a comprehensive platform for more general network traffic analysis as
well. Well grounded in more than 15 years of research, Zeek has successfully
bridged the traditional gap between academia and operations since its
inception. Today, it is relied upon operationally in particular by many
scientific environments for securing their cyberinfrastructure. Zeek's user
community includes major universities, research labs, supercomputing centers,
and open-science communities.

%package -n zeek-core
Summary:        The core zeek installation without zeekctl
Group:          Productivity/Networking/Diagnostic
BuildRequires: flex bison cmake openssl-devel zlib-devel python-devel swig gcc-c++
BuildRequires: libpcap-devel
%if 0%{?sle_version} >= 150000 || 0%{?suse_version} >= 1550
BuildRequires: python3
%endif

%description -n zeek-core
Zeek is a powerful network analysis framework that is much different from the
typical IDS you may know.  While focusing on network security monitoring, Zeek
provides a comprehensive platform for more general network traffic analysis as
well. Well grounded in more than 15 years of research, Zeek has successfully
bridged the traditional gap between academia and operations since its
inception. Today, it is relied upon operationally in particular by many
scientific environments for securing their cyberinfrastructure. Zeek's user
community includes major universities, research labs, supercomputing centers,
and open-science communities.

%package -n zeek-devel
Summary:        Development files for Zeek
Group:          Productivity/Networking/Diagnostic
Requires:       zeek-libcaf-devel = %{version}
Requires:       libbroker-devel = %{version}

%description -n zeek-devel
Development files for Zeek; these files are needed when building binary packages
for Zeek.

%package -n zeek-libcaf-devel
Summary:        C++ actor framework development files
Group:          System/Libraries

%description -n zeek-libcaf-devel
CAF is an open source C++11 actor model implementation featuring lightweight &
fast actor implementations, pattern matching for messages, network transparent
messaging, and more.
This package bundles the library files and headers that were used during the Zeek
build process; they may be needed when building packages for Zeek.

%package -n libbroker-devel
Summary:        Development files for Zeek's Messaging Library
Group:          System/Libraries

%description -n libbroker-devel
The Broker library implements Zeek's high-level communication patterns.
This package bundles the library files and headers that were used during the Zeek
build process; they may be needed when building packages for Zeek.

%package -n zeekctl
Summary:        Zeek Control
Group:          Productivity/Networking/Diagnostic
%if 0%{?sle_version} == 150000
Requires: python3
%else
Requires:       python
%endif
Requires:       zeek-core = %{version}
%if 0%{?suse_version}
Requires:       python-curses
%endif

%description -n zeekctl
ZeekControl is Zeek's interactive shell for operating Zeek installations.

%pre
/usr/bin/getent group zeek >/dev/null || /usr/sbin/groupadd -r zeek

%pre -n zeek-core
/usr/bin/getent group zeek >/dev/null || /usr/sbin/groupadd -r zeek

%pre -n zeek-devel
/usr/bin/getent group zeek >/dev/null || /usr/sbin/groupadd -r zeek

%pre -n zeekctl
/usr/bin/getent group zeek >/dev/null || /usr/sbin/groupadd -r zeek

%pre -n zeek-libcaf-devel
/usr/bin/getent group zeek >/dev/null || /usr/sbin/groupadd -r zeek

%pre -n libbroker-devel
/usr/bin/getent group zeek >/dev/null || /usr/sbin/groupadd -r zeek

%prep
%setup -n zeek-3.0.1 -q
# some platforms do in-source builds when using cmake. I don't really care, so just patch the error out.
find ./ -name "ProhibitInSourceBuild.cmake" | xargs -I file sh -c 'cat /dev/null > "file"'
%patch0 -p0
%patch1 -p1
%if 0%{?centos_version} == 600 || 0%{?scientificlinux_version} == 600 || 0%{?rhel_version} == 505
%patch2 -p0
%endif
%if 0%{?fedora_version} == 30
%patch2 -p1
%endif

%build
./configure --prefix=%{_prefix} --libdir=%{_libdir} --binary-package --enable-static-broker --enable-static-binpac
# make %{?_smp_mflags}
make

%install
rm -rf $RPM_BUILD_ROOT
%if %{defined rhel_version}
make install DESTDIR=$RPM_BUILD_ROOT
%else
%make_install
%endif
mkdir -p %{?buildroot}/opt/zeek/spool/tmp
mkdir -p %{?buildroot}/opt/zeek/logs
touch %{?buildroot}/opt/zeek/spool/zeekctl-config.sh

%files

%files -n zeek-core
%defattr(-,root,zeek,0755)
%dir %{_prefix}
%dir %{_bindir}
%dir %{_datadir}
%dir %{_datadir}/zeek
%dir %{_mandir}
%dir %{_mandir}/man1
%dir %{_mandir}/man8
%dir %{_libdir}
%dir %{_libdir}/zeek
%dir %{_libdir}/zeek/plugins
%{_bindir}/zeek
%{_bindir}/zeek-wrapper
%{_bindir}/bro
%{_bindir}/zeek-cut
%{_bindir}/bro-cut
%{_bindir}/zeek-config
%{_bindir}/bro-config
%{_bindir}/adtrace
%{_bindir}/rst
%{_bindir}/paraglob-test
%{_datadir}/zeek/base
%{_datadir}/zeek/policy
%{_datadir}/zeek/zeekygen
%{_mandir}/man1/zeek-cut.1
%{_mandir}/man8/zeek.8
%defattr(0664,root,zeek,2775)
%dir %{_datadir}/zeek/site
%config %{_datadir}/zeek/site/local.zeek

%files -n zeekctl
%defattr(-,root,zeek,0755)
%dir %{_prefix}
%dir %{_bindir}
%dir %{_datadir}
%dir %{_datadir}/zeek
%dir %{_libdir}
%dir %{_libdir}/zeekctl
%dir %{_mandir}
%dir %{_mandir}/man1
%dir %{_mandir}/man8
%{_bindir}/zeekctl
%{_bindir}/broctl
%{_bindir}/capstats
%{_bindir}/trace-summary
%{_datadir}/zeekctl
%{_datadir}/zeek/zeekctl
%{_libdir}/broctl
%{_libdir}/zeekctl/*.so
%{_libdir}/zeekctl/*.p*
%{_libdir}/zeekctl/plugins
%{_libdir}/zeekctl/broker
%{_libdir}/zeekctl/ZeekControl
%{_libdir}/zeekctl/BroControl
%{_mandir}/man8/zeekctl.8
%{_mandir}/man1/trace-summary.1
%defattr(0664,root,zeek,2775)
%dir %{_sysconfdir}
%config %{_sysconfdir}/zeekctl.cfg
%config %{_sysconfdir}/networks.cfg
%config %{_sysconfdir}/node.cfg
%defattr(0664,root,zeek,2770)
%{_prefix}/spool
%{_prefix}/logs

%files -n zeek-devel
%defattr(-,root,zeek,0755)
%dir %{_prefix}
%dir %{_bindir}
%dir %{_includedir}
%dir %{_libdir}
%dir %{_datadir}
%dir %{_datadir}/zeek
%{_bindir}/bifcl
%{_bindir}/binpac
%{_includedir}/binpac
%{_includedir}/zeek
%{_includedir}/paraglob
%{_libdir}/libbinpac.a
%{_libdir}/libparaglob.a
%{_datadir}/zeek/cmake

%files -n libbroker-devel
%defattr(-,root,zeek,0755)
%dir %{_prefix}
%dir %{_includedir}
%dir %{_libdir}
%{_includedir}/broker
%{_libdir}/libbroker.a

%files -n zeek-libcaf-devel
%defattr(-,root,zeek,0755)
%dir %{_prefix}
%dir %{_includedir}
%dir %{_libdir}
%{_includedir}/caf
%{_libdir}/libcaf_*.a

%doc CHANGES COPYING NEWS README VERSION

%changelog
* Mon Feb 09 2015 Johanna Amann <build@xxon.net> 3.0.1-0
Nightly build version specification
* Wed Jan 28 2015 Johanna Amann <build@xxon.net> 2.3.2
Update to Zeek 2.3.2
* Wed Oct 29 2014 Johanna Amann <build@xxon.net> 2.3.1
Initial version
-

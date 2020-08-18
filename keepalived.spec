Name:		keepalived
Version:	2.1.5        
Release:        1%{?dist}
Summary:        HA monitor built upon LVS, VRRP and services poller

License:	GPL 
URL:            http://www.keepalived.org/
Source0:        https://keepalived.org/software/keepalived-2.1.5.tar.gz
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  openssl-devel
BuildRequires:	kernel-headers
BuildRequires:	autoconf automake pkgconfig
BuildRequires:	systemd-units

%description
The main goal of the keepalived project is to add a strong & robust keepalive
facility to the Linux Virtual Server project. This project is written in C with
multilayer TCP/IP stack checks. Keepalived implements a framework based on
three family checks : Layer3, Layer4 & Layer5/7. This framework gives the
daemon the ability to check the state of an LVS server pool. When one of the
servers of the LVS server pool is down, keepalived informs the linux kernel via
a setsockopt call to remove this server entry from the LVS topology. In
addition keepalived implements an independent VRRPv2 stack to handle director
failover. So in short keepalived is a userspace daemon for LVS cluster nodes
healthchecks and LVS directors failover.


%prep
%setup -q


%build
CONFIG_OPTS="--with-init=systemd"
autoreconf -f -i
%configure $CONFIG_OPTS
make %{?_smp_mflags} STRIP=/bin/true


%install
rm -rf %{buildroot}
%make_install DESTDIR=%{buildroot}
# Remove "samples", as we include them in %%doc
rm -rf %{buildroot}%{_sysconfdir}/keepalived/samples/
# Likewise remove README
rm -f %{buildroot}%{_docdir}/%{name}/README

%check
# A build could silently have LVS support disabled if the kernel includes can't
# be properly found, we need to avoid that.
if ! grep -q "#define _WITH_LVS_ *1" lib/config.h; then
    %{__echo} "ERROR: We do not want keepalived lacking LVS support."
    exit 1
fi

%clean
%{__rm} -rf %{buildroot}

%post
if [ $1 -eq 1 ]; then
        # Enable (but don't start) the units by default
	/sbin/chkconfig --add keepalived
	/bin/systemctl enable keepalived.service >/dev/null 2>&1 || :
:
fi

%preun
if [ $1 -eq 0 ]; then
        # Disable and stop the units
	/bin/systemctl disable keepalived.service >/dev/null 2>&1 || :
	/bin/systemctl stop keepalived.service >/dev/null 2>&1 || :
:
fi

%postun
if [ $1 -ge 1 ]; then
	# On upgrade, reload init system configuration if we changed unit files
	# and restart the daemon
	/bin/systemctl daemon-reload >/dev/null 2>&1 || :
	/bin/systemctl try-restart keepalived.service >/dev/null 2>&1 || :
:
fi

%files
%defattr(-, root, root, -)
%doc AUTHOR ChangeLog CONTRIBUTORS COPYING README TODO
%doc doc/keepalived.conf.SYNOPSIS doc/samples/
%dir %{_sysconfdir}/keepalived/
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/keepalived/keepalived.conf
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/keepalived
%{_unitdir}/keepalived.service
%{_bindir}/genhash
%attr(0755,root,root) %{_sbindir}/keepalived
%{_mandir}/man1/genhash.1*
%{_mandir}/man5/keepalived.conf.5*
%{_mandir}/man8/keepalived.8*


%changelog
* Wed Nov  1 2017 Quentin Armitage <quentin@armitage.org.uk> 1.3.9-1
- Fix installation of keepalived.service

* Tue Oct 17 2017 Quentin Armitage <quentin@armitage.org.uk> 1.3.8-1
- Handle Fedora and CentOS differences for %{_docdir_fmt}

* Fri Sep 16 2016 Quentin Armitage <quentin@armitage.org.uk> 1.2.24-2
- Fixes to allow building on a systemd based system

* Wed Sep 14 2016 Quentin Armitage <quentin@armitage.org.uk> 1.2.24-1
- Add more BuildRequires

* Tue Sep 13 2016 Quentin Armitage <quentin@armitage.org.uk> 1.2.24
- Update for changed format due of config.log due to using automake
- Add support for systemd and upstart based systems

* Thu Sep 13 2007 Alexandre Cassen <acassen@linux-vs.org> 1.1.14
- Merge work done by freshrpms.net... Thanks guys !!! ;)

* Wed Feb 14 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-5
- Add missing scriplet requirements.

* Tue Feb 13 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-4
- Add missing \n to the kernel define, for when multiple kernels are installed.
- Pass STRIP=/bin/true to "make" in order to get a useful debuginfo package.

* Tue Feb 13 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-3
- Add %%check section to make sure any build without LVS support will fail.

* Mon Feb  5 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-2
- Use our own init script, include a sysconfig entry used by it for options.

* Thu Jan 25 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-1
- Update to 1.1.13.
- Change mode of configuration file to 0600.
- Don't include all of "doc" since it meant re-including all man pages.
- Don't include samples in the main configuration path, they're in %%doc.
- Include patch to add an optional label to interfaces.

* Sat Apr 08 2006 Dries Verachtert <dries@ulyssis.org> - 1.1.12-1.2
- Rebuild for Fedora Core 5.

* Sun Mar 12 2006 Dag Wieers <dag@wieers.com> - 1.1.12-1
- Updated to release 1.1.12.

* Fri Mar 04 2005 Dag Wieers <dag@wieers.com> - 1.1.11-1
- Updated to release 1.1.11.

* Wed Feb 23 2005 Dag Wieers <dag@wieers.com> - 1.1.10-2
- Fixed IPVS/LVS support. (Joe Sauer)

* Tue Feb 15 2005 Dag Wieers <dag@wieers.com> - 1.1.10-1
- Updated to release 1.1.10.

* Mon Feb 07 2005 Dag Wieers <dag@wieers.com> - 1.1.9-1
- Updated to release 1.1.9.

* Sun Oct 17 2004 Dag Wieers <dag@wieers.com> - 1.1.7-2
- Fixes to build with kernel IPVS support. (Tim Verhoeven)

* Fri Sep 24 2004 Dag Wieers <dag@wieers.com> - 1.1.7-1
- Updated to release 1.1.7. (Mathieu Lubrano)

* Mon Feb 23 2004 Dag Wieers <dag@wieers.com> - 1.1.6-0
- Updated to release 1.1.6.

* Mon Jan 26 2004 Dag Wieers <dag@wieers.com> - 1.1.5-0
- Updated to release 1.1.5.

* Mon Dec 29 2003 Dag Wieers <dag@wieers.com> - 1.1.4-0
- Updated to release 1.1.4.

* Fri Jun 06 2003 Dag Wieers <dag@wieers.com> - 1.0.3-0
- Initial package. (using DAR)
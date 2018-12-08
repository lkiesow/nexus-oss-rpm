%define srcname    nexus

Name:      %{srcname}-oss
Summary:   Maven software artifact manager
Version:   2.14.11
Release:   1%{?dist}
License:   EPL
URL:       https://nexus.sonatype.org/
Source0:   https://sonatype-download.global.ssl.fastly.net/%{srcname}/oss/%{srcname}-%{version}-01-bundle.tar.gz
Source1:   https://raw.githubusercontent.com/lkiesow/nexus-oss-rpm/master/%{name}.service
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

# We only care for 64bit Linux
ExclusiveArch: x86_64

Requires: java-headless >= 1:1.7.0
%{?systemd_requires}
BuildRequires: systemd

%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%define __requires_exclude_from ^.*\\.jar$
%define __provides_exclude_from ^%{_datadir}/.*\\..*$

%description
Nexus manages software "artifacts" required for development, deployment, and
provisioning.  If you develop software, Nexus can help you share those
artifacts with other developers and end-users.

%prep
%setup -q -n %{srcname}-%{version}-01


%build
# Nothing to do


%install
rm -rf $RPM_BUILD_ROOT

# Create directories
mkdir -p %{buildroot}%{_datadir}/%{name}/bin/jsw/lib/
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
mkdir -p %{buildroot}/run/%{name}

mv lib       %{buildroot}%{_datadir}/%{name}
mv nexus     %{buildroot}%{_datadir}/%{name}
mv conf      %{buildroot}%{_sysconfdir}/%{name}

install -p -m 0644 \
  bin/jsw/lib/libwrapper-linux-x86-64.so \
  bin/jsw/lib/wrapper-*.jar \
  %{buildroot}%{_datadir}/%{name}/bin/jsw/lib/
install -p -D -m 0755 \
  bin/jsw/linux-x86-64/wrapper \
  %{buildroot}%{_datadir}/%{name}/bin/jsw/linux-x86-64/wrapper
install -p -D -m 0644 \
  bin/jsw/conf/wrapper.conf \
  %{buildroot}%{_sysconfdir}/%{name}/wrapper/wrapper.conf

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

ln -sf %{_sysconfdir}/%{name}         %{buildroot}%{_datadir}/%{name}/conf
ln -sf %{_sysconfdir}/%{name}/wrapper %{buildroot}%{_datadir}/%{name}/bin/jsw/conf
ln -sf %{_localstatedir}/log/%{name}  %{buildroot}%{_datadir}/%{name}/logs
ln -sf /tmp                           %{buildroot}%{_datadir}/%{name}/tmp

# patch work dir
sed -i -e "s#nexus-work=.*#nexus-work=%{_sharedstatedir}/%{name}/#g" \
  %{buildroot}%{_sysconfdir}/%{name}/nexus.properties

# patch logfile
sed -i -e  "s#wrapper.logfile=.*#wrapper.logfile=%{_localstatedir}/log/%{name}/nexus.log#" \
  %{buildroot}%{_sysconfdir}/%{name}/wrapper/wrapper.conf


%pre
# Add nexus user and group
getent group %{srcname} > /dev/null || groupadd -r %{srcname} || :
getent passwd %{srcname} > /dev/null || \
  useradd -g %{srcname} -s /bin/bash -r \
  -d %{_sharedstatedir}/%{name} %{srcname} &> /dev/null || :

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc NOTICE.txt LICENSE.txt bin/jsw/license/LICENSE.txt
%{_unitdir}/%{name}.service
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}
%attr(755,nexus,nexus) %dir %{_sharedstatedir}/%{name}
%attr(755,nexus,nexus) %dir %{_localstatedir}/log/%{name}

%changelog
* Sat Dec 08 2018 Lars Kiesow <lkiesow@uos.de> - 2.14.11-1
- Update to 2.14.11

* Sat Sep 22 2018 Lars Kiesow <lkiesow@uos.de> - 2.14.10-1
- Update to 2.14.10

* Thu Sep 06 2018 Lars Kiesow <lkiesow@uos.de> - 2.14.9-2
- Fixed packaging mistake

* Thu Sep 06 2018 Lars Kiesow <lkiesow@uos.de> - 2.14.9-1
- Update to 2.14.9

* Fri May 25 2018 Lars Kiesow <lkiesow@uos.de> 2.14.8-1
- Update to 2.14.8

* Wed Feb 21 2018 Lars Kiesow <lkiesow@uos.de> 2.14.7-1
- Update to 2.14.7

* Wed Feb 07 2018 Lars Kiesow <lkiesow@uos.de> 2.14.6-1
- Update to 2.14.6

* Mon Aug 21 2017 Lars Kiesow <lkiesow@uos.de> 2.14.2-1
- Update to 2.14.5

* Thu Jan 26 2017 Lars Kiesow <lkiesow@uos.de> 2.14.2-1
- Update to 2.14.2

* Mon Nov 07 2016 Lars Kiesow <lkiesow@uos.de> - 2.14.1-1
- Update to 2.14.1

* Tue May 10 2016 Lars Kiesow <lkiesow@uos.de> - 2.13.0-1
- Update to 2.13.0

* Thu Apr 07 2016 Lars Kiesow <lkiesow@uos.de> - 2.12.1.01-2
- Fixed update problem

* Thu Apr 07 2016 Lars Kiesow <lkiesow@uos.de> - 2.12.1.01-1
- Update to 2.12.1-01

* Tue Feb  2 2016 Lars Kiesow <lkiesow@uos.de> - 2.12.0.01-3
- Fixed restart

* Mon Feb  1 2016 Lars Kiesow <lkiesow@uos.de> - 2.12.0.01-2
- Require only java-headless

* Mon Feb  1 2016 Lars Kiesow <lkiesow@uos.de> - 2.12.0.01-1
- Update to 2.12.0-01

* Mon Sep 14 2015 Lars Kiesow <lkiesow@uos.de> - 2.11.4.01-3
- Added missing systemd requirement

* Fri Sep  4 2015 Lars Kiesow <lkiesow@uos.de> - 2.11.4.01-2
- Remove problematic bin script (systemd start only)

* Fri Aug 28 2015 Lars Kiesow <lkiesow@uos.de> - 2.11.4.01-1
- Update to 2.11.4-01
- Use port 8081
- Create nexus user
- Move configuration to /etc/nexus-oss

* Thu Dec 22 2011 Jens Braeuer <braeuer.jens@googlemail.com> - 1.9.2.3-1
- Initial packaging.
- For now nexus will run as root and listen to port 80


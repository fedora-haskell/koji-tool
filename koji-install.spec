# generated by cabal-rpm-2.0.10
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Haskell/

%global debug_package %{nil}

%bcond_with tests

Name:           koji-install
Version:        0.5
Release:        1%{?dist}
Summary:        CLI tool for installing rpms directly from Fedora Koji

License:        BSD
Url:            https://hackage.haskell.org/package/%{name}
# Begin cabal-rpm sources:
Source0:        https://hackage.haskell.org/package/%{name}-%{version}/%{name}-%{version}.tar.gz
# End cabal-rpm sources

# Begin cabal-rpm deps:
BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
%if 0%{?fedora}
BuildRequires:  ghc-Glob-static
%endif
BuildRequires:  ghc-base-devel
BuildRequires:  ghc-directory-devel
%if 0%{?fedora}
BuildRequires:  ghc-extra-static
%endif
BuildRequires:  ghc-filepath-devel
%if 0%{?fedora}
BuildRequires:  ghc-http-directory-static
BuildRequires:  ghc-koji-static
BuildRequires:  ghc-rpm-nvr-static
BuildRequires:  ghc-simple-cmd-static
BuildRequires:  ghc-simple-cmd-args-static
BuildRequires:  ghc-xdg-userdirs-static
%endif
BuildRequires:  cabal-install > 1.18
%if %{defined rhel}
BuildRequires:  ghc-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
%endif
# End cabal-rpm deps

%description
Koji-install can install a koji build/task of a package locally.
Koji is the RPM-based buildsystem of Fedora Linux and CentOS.


%prep
# Begin cabal-rpm setup:
%setup -q
# End cabal-rpm setup


%build
# Begin cabal-rpm build:
cabal update
%if %{defined fedora}
# need http-directory-0.1.9
#%%ghc_bin_build
cabal build
%else
%if 0%{?rhel} && 0%{?rhel} < 9
cabal sandbox init
cabal install
%endif
%endif
# End cabal-rpm build


%install
# Begin cabal-rpm install
mkdir -p %{buildroot}%{_bindir}
%if %{defined fedora}
#%%ghc_bin_install
strip -s -o %{buildroot}%{_bindir}/%{name} dist-newstyle/build/*/ghc-*/%{name}-%{version}/x/%{name}/build/%{name}/%{name}
%else
%if 0%{?fedora} >= 33 || 0%{?rhel} > 8
cabal install --install-method=copy --installdir=%{buildroot}%{_bindir}
%else
for i in .cabal-sandbox/bin/*; do
strip -s -o %{buildroot}%{_bindir}/$(basename $i) $i
done
%endif
%endif
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions/
%{buildroot}%{_bindir}/%{name} --bash-completion-script %{name} | sed s/filenames/default/ > %{buildroot}%{_datadir}/bash-completion/completions/%{name}
# End cabal-rpm install


%check
%if %{with tests}
%cabal_test
%endif


%files
# Begin cabal-rpm files:
%license LICENSE
%doc ChangeLog.md README.md
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}
# End cabal-rpm files


%changelog
* Tue Dec 28 2021 Jens Petersen <petersen@redhat.com> - 0.5-1
- '--package' and '--exclude' filters can now be combined
- '--package' and '--exclude' now also check subpackage names without
  the base prefix

* Tue Dec 21 2021 Jens Petersen <petersen@redhat.com> - 0.4-1
- support installing/listing by koji taskid
- select subpackages with --package and --exclude, by name or globbing
- check remote files date/size with http-directory
- listing a task either lists the task's children or rpms
- use dnf reinstall for installed packages and otherwise localinstall
- more detailed debug output
- system arch no longer hardcoded to x86_64

* Fri Dec  3 2021 Jens Petersen <petersen@redhat.com> - 0.3-0.1
- add `--list` command to list recent builds
- fix bug in generating kojifiles url from short name
- workarounds for rpmfusion's older koji not supporting patterns
- check if %dist is defined

* Fri Dec  3 2021 Jens Petersen <petersen@redhat.com> - 0.2.0-0.1
- 0.2.0

* Thu Aug 12 2021 Jens Petersen <petersen@redhat.com> - 0.1.0-1
- spec file generated by cabal-rpm-2.0.10

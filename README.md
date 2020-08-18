# Keepalived RPM generator

This repository guides you on how to build an RPM package from the keepalived source code.

**Note**: These instructions are tested under CentOS 7 to build `x86_64` package with `systemd` support. PRs are welcome :) 

## Prerequisite

Install the necessary packages:

```bash
yum install openssl-devel
yum install kernel-headers
yum install gcc rpm-build rpm-devel rpmlint make coreutils diffutils patch rpmdevtools
yum install autoconf automake pkgconfig
yum install systemd-units
```
Create RPM build directories:

```bash
rpmdev-setuptree
```
This command will create a `rpmbuild` directory in your home directory.

## Download keepalived source code

```bash
wget https://keepalived.org/software/keepalived-2.1.5.tar.gz -O ~/rpmbuild/SOURCES/keepalived-2.1.5.tar.gz
```
Change `2.1.5` to your prefered version

## Download keepalived.spec file

```bash
wget https://raw.github.com/yasharne/keepalived_rpm/master/keepalived.spec -O ~/rpmbuild/SPECS/keepalived.spec
```
edit `keepalived.spec` file and change the `Version` parameter to the keepalived version you want to package:
```
Version:        2.1.5 
```

## Build the package

```bash
rpmbuild -bb ~/rpmbuild/SPECS/keepalived.spec
```

The built RPM package is under `~/rpmbuild/RPMS/x86_64/` directory.

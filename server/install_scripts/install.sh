#!/bin/bash

# Install java

yum install java-1.8.0-openjdk-devel
java -version
update-alternatives --config java

# install postgresql
dnf install https://download.postgresql.org/pub/repos/yum/reporpms/F-30-x86x_64/pgdg-fedora-repo-latest.noarch.rpm
dnf install postgresql12
dnf install postgresql12-server
/usr/pgsql-12/bin/postgresql-12-setup initdb
systemctl enable postgresql-12
systemctl start postgresql-12

# Installing postgreSQL 

Short guide for installing a postgreSQL database on a Fedora system 

## Constraints 
* Root privleges 
* A machine running Fedora 

## Install

Install the package  
```
$ dnf install postgresql postgresql-contrib
```

postgresql requires a new linux user to interact with the database. When you install the `postgresql` package a new user with the name `postgres` will be added. 

You can switch to this user with the following command 

```
$ sudo -i -u postgres 
```

## Running postgres 
You can run the postgres database by doing the following 

```
$ psql 
```

# hfpython-flask
Flask app of Head first Python Second Edition.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development.

### Prerequisites

```
$ python --version
Python 3.6.3
$ /usr/local/mariadb/server/bin/mariadb --version
/usr/local/mariadb/server/bin/mariadb  Ver 15.1 Distrib 10.2.12-MariaDB, for osx10.13 (x86_64) using  EditLine wrapper
```

Below steps are needed to create DB table we use.
```
sudo /usr/local/mariadb/server/bin/mariadb
MariaDB [(none)]> create database vsearchlogDB; 
MariaDB [(none)]> grant all on vsearchlogDB.* to 'vsearch' identified by 'vsearchpasswd';
MariaDB [(none)]>　quit
$ sudo /usr/local/mariadb/server/bin/mariadb -u vsearch -p vsearchlogDB
MariaDB [vsearchlogDB]> create table log (
    -> id int auto_increment primary key,
    -> ts timestamp default current_timestamp,
    -> phrase varchar(128) not null,
    -> letters varchar(32) not null,
    -> ip varchar(16) not null,
    -> browser_string varchar(256) not null,
    -> results varchar(64) not null);
MariaDB [vsearchlogDB]> describe log;
+----------------+--------------+------+-----+---------------------+----------------+
| Field          | Type         | Null | Key | Default             | Extra          |
+----------------+--------------+------+-----+---------------------+----------------+
| id             | int(11)      | NO   | PRI | NULL                | auto_increment |
| ts             | timestamp    | NO   |     | current_timestamp() |                |
| phrase         | varchar(128) | NO   |     | NULL                |                |
| letters        | varchar(32)  | NO   |     | NULL                |                |
| ip             | varchar(16)  | NO   |     | NULL                |                |
| browser_string | varchar(256) | NO   |     | NULL                |                |
| results        | varchar(64)  | NO   |     | NULL                |                |
+----------------+--------------+------+-----+---------------------+----------------+

```

### Installing
Install Database driver.

[MySQL / Download Connector/Python](https://dev.mysql.com/downloads/connector/python/)


Install original package.

```
$ pip install ./vsearch-1.0.tar.gz 
```

And install other required packages from PyPI.

```
$ pip install -r requirements.txt 
```

Run.

```
$ python3 webapp/vsearch4web.py 
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

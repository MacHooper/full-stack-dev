# Relational Databases

## Database Charecteristics

- Store many types of data
- Multiple users at once = concurrency control
- Can access data later = persistence
- All users can access the same database = shared source of truth
- Data is stored in tables
- Columns have datatypes
- Provides constraints and triggers to enforce data integrity.

## Keys

There are three types of keys:

- Primary Keys = a uniquie identifier, something like user_id.
- Composite Keys = primary key consisting of columnS i.e user_id and reg_no.
- Foreign Keys = Create a relationship between two tables.

SQLFiddle is down so I can't play with the drivers and vehichles database.

## DBMS Database Management Systems

Different DBMS systems have their own DIALECTS of SQL. The DBMS that we will be using for this course is PostgresSQL

## Execution Plan

A DBMS takes the SQL query and generates an execution plan.

EXAMPLE

```
SELECT * from vehicles WHERE driver_id = 3

Builds an execution plan:

Go through every row in the vehicles table

Whenever driver_id = 3, copy the row

Plan is then read, processed and executed by the DBMS.
```

> Inner Joins return rows shared between two tables excluding rows that only exist in one of the two.

In SQLFiddle if you run a query you can see the execution plan.Each row of the execution plan has a cost.
The Execution Plan looks as follows.

```
SELECT make, model from vehicles
JOIN drivers on vehicles.driver_id = drivers.id;

// Hash Join: This joins two record sets, the hash join creates a hash in-memory that hashes based the driver_id column.

// Seq Scan: Sequential scan is done across the entire vehicles table. This makes sense since we are looking to fetch all 'make' and 'model' across 'all records' in the vehicles table.

// Hash with Seq Scan on drivers: as the seq scan continues, the join key is checked in the Hash returned from Step 1, where if it does not exists, given that this is an Inner join, we ignore that row, and if it does exist then we fetch the row from the has to generate the outputted, joined row.
```

> We can always gain visibility over how performant a given SQL query is by looking at its execution plan.

Always try to improve the performance of SQL Queries by using critical indexes to speed up lookups, utilities like SQL views for splitting queries into subroutines.
[Use the Index, Luke](https://use-the-index-luke.com/) is a good guide for database performance.
This is important because it could be the difference between a 4 second load time and a half a second load time.

## Client-Server Model

Clients and Servers interact as follows

![Client-Server Model](https://video.udacity-data.com/topher/2019/October/5db32370_client-server-model/client-server-model.png)

a **server** is a program that communicates over a network to serve _clients_

a **client** is a program that can request data from a _server_

### Adding database to the model

**Servers, Clients, Hosts**

- A **server** serves many **clients**
- Servers and clients are programs that run on _hosts_
- **Hosts** Are computers connected over a network (the internet)

**Requests & Responses**

> Restaraunt: a client sends a request to the server and the _waiters_ collect the data from the kitchen. The server returns with a **response** to the client. The client and server use a common language (**communication protocol**)

![C3PO](https://cdn0.iconfinder.com/data/icons/famous-character-vol-1-colored/48/JD-34-512.png)

**Relational Database Clients**

- A databse client is any program that sends requests to a database.
- In some cases, the database client is a web server! When your browser makes a request the server acts as a server(_fulfilling the request_) but when the server requests data from the database, it is acting as a client to that database.
- To a **database server** a **webserver** is a **client**
- to a web client a web server is a server

> Simple **clients** make requests **servers** fulfill requests

## Example: Janes Store

Online Clothing Store.
When a user clicks on a product it serves more info on a product detail page, with an add to cart button.

What happens when a user clicks on a product

```
* User clicks on item.
* Web Client registers a click event that occured in the users browser.
* an event handler (click event) sees what was clicked and passes a function
* Request is asking for info (data req.) and to render a diff. page (view req.)
* Server process listens to the request sent, fetches data and renders new page.

    Data Fetch
    * server receives request, and uses input data to shape query.
    * database processes request, sends response to web server
    * server receives DB response abd determines view + powers view template with fetched data sends to client.
    * client is responsible for rendering something to the user, that represents the data and presentation.
```

> The \***\*web server\*\*** receives a request from the **client** and sends a request to the **database**, which sends back a response to the **web server**, **which then sends back a response** to the **client**.

## TCP/IP

In this section we will look at communication protocols, commonly referred to as **TCP/IP** or **Transmission Control Protocol** and **Internet Protocol**

**TCP/IP uses:**

- **IP addresses:** An IP address identifies the location of a computer on a network.
- **Ports**: A port is a location on the recipient computer, where data is received.

An IP tells you where to find a computer it doesn't tell you specifically where on that computer a connection should be made — that's what **port numbers** are for

### Port numbers you should know:

- **Port 80:** Most commonly used for HTTPS requests. e.g. port 80 is usually used when a client makes a request to a web server.
- ** Port 5432:** The port number used by most database systems; default port for Postgres.

> Ports allow multiple types of traffic being received at the same time on a given device, to be tracked and routed to where they need to go.
> An IP has many ports

## Connections and Sessions in TCP/IP

- TCP/IP is **connection-based**, meaning all communications between parties are arranged over a connection. A connection is established before any data transmission begins.
- Over TCP/IP we always need to establish a connection between clients and servers to enable communications.
  - Deliveries over a connection are **error-checked:** if packets arrive damage or lost they are resent(known as _retransmission_)
- Connection starts a **session.** Ending the connection ends the **session**.
- In a DB session, many **transactions** can occur during a session. Each transaction does work to commit changes to the database.

### Aside: The UDP Protocol

The internet offers the UDP protocol, simpler than TCP: hosts on the network send data (in _datagrams_) without connections needed.

** TCP vs UDP **
TCP is like building highways, UDP is like sending a pigeon. UDP is simpler to manage but doesn't scale as well, used when speed is preferred over reliability i.e when an application needs to stream very small amounts of data quickly, UDP is preferred. TCP's continuous connection is more reliable, but has more latency.

## Transactions

All Changes to data are made through transactions. These include **UPDATES**, **INSERTS** and **DELETES**

- Databases are interacted with using client-server interactions over a network.
- Postgres uses TCP/IP to be interacted with, which is connection-based.
- We interact with databases like Postgres during sessions.
- Sessions have transsactions that commit work to the database.

**Transactions capture logical bundles of work.**
Work is bundled into transactions so that in case of system failures, data in your database is still kept in a valid state (by rolling back the entire transaction if any part of it fails). To ensure a database is consistent before and after work is done to it, they use atomic transactions and actions like commits and rollbacks to handle failures appropriately. Transactions are ACID

> Transactions are: atomic units of work for the database to perform as a whole.
> a transaction captures one or more changes to a database, executed in order.
> UPDATE, INSERT & DELETE can be added to Transactions.
> You can send off the set of changes to the database by _committing_ the transaction.
> A transaction can be cleared of commands using a _rollback_

## Postgres

### Install

Before we can use Postgres we will need to install it. It comes preinstalled on MacOS.

on Linux run

```
sudo apt-get update
sudo apt-get install postgresql-10.4
```

The set the password and createa testdb

```
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
sudo -u postgres psql -c "CREATE DATABASE example;"
```

Start postgres server

```
sudo service postgresql start
```

Stop postgres server

```
sudo service postgresql stop
```

### Initial installation settings

The initial install will

- create a database named `postgres`
- create a user named `postgres`. Your `postgres` user will have no password by default.
- create initial databases called `template1` and `template0`. Any other database created after `template1` is a clone of `template1`, including its tables and rows. If you add rows (objects) to `template1`, they will be copied into future created databases. `template0` should stay pure and never changed.
- The default host machine that runs your postgres server, on your machine is `localhost` (aka, `127.0.0.1`)
- The default port traditionally used to host your server is `5432` there are very few reasons to use a different port.

Default connection settings are:

```
Field 	Default Value
Host 	localhost
Port 	5432
Username 	postgres
Password 	(left blank)
```

### Deepdive into what Postgres is

- Postgres is an open source, general purpos and **object-relational database management system**. It's a relational database system with object-oriented features, that work across operating systems.
  - Object-relational support includes support for arrays and inheritance.
- Built in 1977, it is **Highly Stable** requires minimal maintenance.
- **Widely used**: App, Cisco, Etsy, Micrsoft, Reddit, Instagram and many others.
- Comprehensive support for the **SQL** standard.
- **Transaction-based**: operations on the database are done through atomic transactions.
- has **multi-version concurrency control** avoiding unnecessary locking when multiple writes are happening at once.
  - Postgres lets you have several databases availivle for reading from and writing to.
- Offers **great performance** and many **indexing** capabilities for optimizing query performance.
- PostgreSQL is often called Postgres.

## Postgres Command Line Applications

To start a postgres server

`sudo service postgresql start`

to stop

`sudo service postgresql stop`

Log in as a user _default user is_ `postgres`

`sudo -u <username> -i`

Create new database

`createdb <database-name>`

Destroy a database

`dropdb <database-name>`

Reset a database

`dropdb <database-name> && createdb <database-name>`

## Intro to psql

### Takeaways

- \*\*psql is an interavtive terminal application for connecting and interacting with your local postgres server.
- connect using `psql <dbname>`
- psql lets you
  - Directly input SQL commands.
  - Inspect and preview your database tables using psql meta-commands

### Base psql commands

`create table <tablename>( id INTEGER PRIMARY KEY, description VARCHAR NOT NULL` - Creates a table, you can then add column names with constraints within parentheses, followed by a semicolon. In this example it creates a primary key with uniqueness and integer constraints and a description with VARCHAR and NOT NULL constraints.

### Useful psql commands

`psql <dbname> [<username>]` - starts psql connection to dbname. Optionally use another user other than the current user.

in psql:
`# \l` - Lists all database on the server, their owners and User Access levels.

`# \c <dbname>` - Connect to the named database.

`# \dt` - Show database tables

`# \d <tablename>` - Describe the table schema

`# \q` Quit psql and return to terminal.

`# \?` Display availible commands.

## Using psql - SQL Commands
[Screengrab of SQL Commands](https://i.imgur.com/8tmYR0z.png)

**example command**
insert a row in to table1 `INSERT INTO table1 (id, description) VALUES (1, 'this is a thing'); then SELECT to query the table`SELECT \* from table1;` and it will output all rows from table 1 in this case the values we just entered in row 1.

## Other Postgres clients

### CLI Tools

> psql, createdb, dropdb etc.

### Postgres GUIs

- **pgAdmin** - A popular gui Postgres client works on all OS'.
- **PopSQL** - Another gui, availible on Mac only.
  & **Tableplus** - A different multi operating system gui

### Postgres Adapters

> **Database Adapters:** psycopg2 (to make client python apps)

### Useful Information

```
**Connection Setting:**	*Default*
Host	                *localhost (aka, 127.0.0.1)*
Port	                *5432*
Username	            *postgres*
Password	            *(None)*
```

## DBAPIs and psycogp2

Sometimes we will want to interact with our DB in a programming language. E.g. to build web applications or data pipelines in a specific language (Ruby, Python, JS, Julia etc.) That's where DBAPIs come in.

- A DBAPI
  - provides a standard interface for one language (like Python) to talk to a relational DB server.
  - Is a low level library for writing SQL statements that connect to a database
  - is also known as a DB adapter.
- Different DBAPIs exist for every server framework or language + database system
- Database adapters define a standard for using a databes (with SQL) and using the results of DB queries as input data in the given language
  - Turn a selected `SELECT * from some_table;` list of rows into an array of objects in Javascript for say a NodeJS adapter; or a list of tuples in python for a Python adapter.

### Examples across languages and frameworks

- Ruby: pg
- NodeJS: node-postgres
- Python: psycogp2

### Install psycopg2

Make sure you have at least Python3.4
`python --version`
Install latest pip version
`pip3 install -U pip`
Set the path for postgres - You can find this by running `sudo find /usr -wholename '*/bin/postgres*` then `locate bin/postgregs`
`export PATH=/usr/lib/postgresql/10.2/bin/:$PATH`
Then run
`pip install psycopg2` - If you run into errors checkout [this](https://stackoverflow.com/questions/28253681/you-need-to-install-postgresql-server-dev-x-y-for-building-a-server-side-extensi/28938258#28938258)

## psycopg2: basic usage

### How to use psycogp2

1. Open Terminal, cd to location and mkdir to store demo scripts CD into that directory.
2. touch demo.py && open in IDE.
3. start the \*.py file with import psycogp2 then write your scripts.

### Table Script
The following script will connect to the 'example' database, create a table named todos with 3 columns (id, description and completed) which you are able to check whether you have completed the task or not.

> Note: Make sure to sign in as postgres in terminal before running the .py script

```
import psycopg2

connection = psycopg2.connect('dbname=example user=postgres password=postgres')

# Open a cursor to perfor DB operations
cursor = connection.cursor()

# create table
# triple quotes allow multiline text in python
cursor.execute('''
    CREATE TABLE todos (
        id INTEGER PRIMARY KEY,
        task VARCHAR NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT False
    );
''')

cursor.execute('INSERT INTO todos (id, completed) VALUES (1, true);')

# commit, so it does the executions on the db and persists in the db
connection.commit()

cursor.close()
connection.close()
```

> If you run into a `ROLE does not exits` error. Open psql and use the following

```
sudo -u postgres psql
postgres=# create database <db>;
postgres=# create user myuser with encrypted password 'mypass';
postgres=# grant all privileges on database <db> to myuser;
```

> The demo.py script in the work folder contains a script which does the following.
```
import psycopg2

connect to the database as user postgres

sets a table_name variable with the value todos

opens a cursor for the database

deletes any existing table with the name todos

create a table named todos with two columns (id=Pkey & completed=Boolean not null default False)

inserts 5 rows with data into the table

then fetches rhe rows and prints them to the terminal.

The script then commits the connection, closes the cursor and connection.
```
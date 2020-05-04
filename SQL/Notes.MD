# Relational Databases

## Database Charecteristics 
* Store many types of data
* Multiple users at once = concurrency control
* Can access data later = persistence 
* All users can access the same database = shared source of truth
* Data is stored in tables
* Columns have datatypes
* Provides constraints and triggers to enforce data integrity.

## Keys
There are three types of keys:
* Primary Keys   = a uniquie identifier, something like user_id.
* Composite Keys = primary key consisting of columnS i.e user_id and reg_no.
* Foreign Keys = Create a relationship between two tables.

SQLFiddle is down so I can't play with the drivers and vehichles database.

## DBMS Database Management Systems
Different DBMS systems have their own DIALECTS of SQL. The DBMS that we will be using for this course is PostgresSQL

## Execution Plan 
A DBMS takes the SQL query and generates an execution plan.

EXAMPLE

```
SELECT ** from vehicles WHERE driver_id = 3

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
* A **server** serves many **clients**
* Servers and clients are programs that run on _hosts_
* **Hosts** Are computers connected over a network (the internet)


**Requests & Responses**
> Restaraunt: a client sends a request to the server and the _waiters_ collect the data from the kitchen. The server returns with a **response** to the client. The client and server use a common language (**communication protocol**) 

![C3PO](https://cdn0.iconfinder.com/data/icons/famous-character-vol-1-colored/48/JD-34-512.png)

**Relational Database Clients** 
* A databse client is any program that sends requests to a database.
* In some cases, the database client is a web server! When your browser makes a request the server acts as a server(_fulfilling the request_) but when the server requests data from the database, it is acting as a client to that database.
* To a **database server** a **webserver** is a **client**
* to a  web client a web server is a server

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
> The ****web server**** receives a request from the **client** and sends a request to the **database**, which sends back a response to the **web server**, **which then sends back a response** to the **client**.

## TCP/IP
In this section we will look at communication protocols, commonly referred to as **TCP/IP** or **Transmission Control Protocol** and **Internet Protocol**

**TCP/IP uses:**
* **IP addresses:** An IP address identifies the location of a computer on a network.
* **Ports**: A port is a location on the recipient computer, where data is received.

An IP tells you where to find a computer it doesn't tell you specifically where on that computer a connection should be made — that's what **port numbers** are for

### Port numbers you should know:
* **Port 80:** Most commonly used for HTTPS requests. e.g. port 80 is usually used when a client makes a request to a web server.
* ** Port 5432:** The port number used by most database systems; default port for Postgres.

> Ports allow multiple types of traffic being received at the same time on a given device, to be tracked and routed to where they need to go. 
> An IP has many ports

## Connections and Sessions in TCP/IP
* TCP/IP is **connection-based**, meaning all communications between parties are arranged over a connection. A connection is established before any data transmission begins.
* Over TCP/IP we always need to establish a connection between clients and servers to enable communications.
    * Deliveries over a connection are **error-checked:** if packets arrive damage or lost they are resent(known as *retransmission*)
* Connection starts a **session.** Ending the connection ends the **session**.
* In a DB session, many **transactions** can occur during a session. Each transaction does work to commit changes to the database.

### Aside: The UDP Protocol
The internet offers the UDP protocol, simpler than TCP: hosts on the network send data (in *datagrams*) without connections needed.

** TCP vs UDP ** 
TCP is like building highways, UDP is like sending a pigeon. UDP is simpler to manage but doesn't scale as well, used when speed is preferred over reliability i.e when an application needs to stream very small amounts of data quickly, UDP is preferred. TCP's continuous connection is more reliable, but has more latency.

## Transactions 
All Changes to data are made through transactions. These include **UPDATES**, **INSERTS** and **DELETES**
* Databases are interacted with using client-server interactions over a network.
* Postgres uses TCP/IP to be interacted with, which is connection-based.
* We interact with databases like Postgres during sessions.
* Sessions have transsactions that commit work to the database.

**Transactions capture logical bundles of work.**
Work is bundled into transactions so that in case of system failures, data in your database is still kept in a valid state (by rolling back the entire transaction if any part of it fails). To ensure a database is consistent before and after work is done to it, they use atomic transactions and actions like commits and rollbacks to handle failures appropriately. Transactions are ACID 
> Transactions are: atomic units of work for the database to perform as a whole.
> a transaction captures one or more changes to a database, executed in order. 
> UPDATE, INSERT & DELETE can be added to Transactions.
> You can send off the set of changes to the database by *committing* the transaction.
> A transaction can be cleared of commands using a *rollback*

## Postgres 

### Install 

Before we can use Postgres we will need to install it. It comes preinstalled on MacOS.

on Linux run
```
sudo apt install postgressql
```
Test the install by running which postgres, it will output a path such as below.
```
$ which postgres
/usr/local/bin/postgres
```
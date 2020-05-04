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

a *server* is a program that communicates over a network to serve _clients_

a *client* is a program that can request data from a _server_


### Adding database to the model

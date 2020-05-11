# SQLAlchemy

## 1. Introduction

- **SQLAlchemy ** is a popular open source library for working with relational databases from Python.
- It is one type of **ORM** library, AKA an **Object-Relational Mapping** library. It provides an interface for using Object Oriented Programming to interact with a database.
- An ORM maps tables and columns to class objects and attributes.
- You still need to take into consideration the dialect of SQL you will be using.

### Pros of using SQLAlchemy

- Write less bug-prone code
- Work entirely in Python
- Be able to switch database systems easily without rewriting code.

> Other ORM libraries include: Javascript: Sequelize & Bookshelf.js Ruby on Rails: ActiveRecord PHP: CakePHP

## 2. Layers of Abstraction

Without SQLAlchemy we'd only use a DBAPI to establish connections and execute SQL statements, simple but not scalable.
SQLAlchemy offers several layers of abstraction and convenient tools for interacting with a database.

SQLAlchemy is broken down into various layers of abstraction. As follows.

![SQLAlchemy Abstractions](https://video.udacity-data.com/topher/2019/August/5d5a1ede_sqla/sqla.png)

### SQLAlchemy and psycopg2 diff.

- SQLAlchemy **generates** SQL statements
- psycopg2 directly **sends** SQL statements to the database.
- SQLAlchemy depends on psycopg2 or other database drivers to communicate with the database under the hood.

### SQLALchemy allows you to move through all 3 layers of abstraction to interact with your database.

- Can stay on the ORM level
- Can dive into database operations to run customized SQL code specific to the database, on the Expressions level.
- Can write raw SQL to execute, when needed, on the engine level.
  - Can more simply use psycopg2 in this case

### Design Practice (example)

- Keep code Pythonic. Work in classes and objects as much as possible.
  - Make switching to a diff. Backend is easy in the future.
- Avoid writing raw SQL until absolutely necessary.

# Layers of SQLAlchemy

- DBAPI
- The Dialect
- The Connection Pool
- The Engine
- SQL Expressions
- SQLAlchemy ORM (optional)

## 3. The Dialect

Why use SQLAlchemy

- No need to write RAW SQL
- Avoid errors in SQL syntax
- quicker
- Can forget about **dbms**, meaning we can switch the database management system

## 4. The Connection Pool

No need to connect to databases, the opening and closing of connections is abstracted away.

- Connection pools are easy to reuse
- handle dropped connections
- Avoid doing many small calls to the db (slow)

## 5. The Engine

- 1 of 3 main layers for how you may choose to interact with the DB
- is the lowest level layer for interacting, much like using a DBAPI. Similar to psycopg2, managing a connection directly.
- The engine in Alchemy refers to both itself, the Dialect and the connection Pool which all work together to interface with our database.
- A connection pool gets automatically created when we create a SQLAlchemy engine.

# 6. SQL Expressions

- Instead of sending raw SQL we can compose python objects to compose SQL expressions instead.
- SQL Expressions still involve using and knowing SQL to interact with the database.
- We can avoid doing SQL query string composition.

# 7. SQLAlchemy ORM

- Lets you compose SQL expressions by mapping classes of objects to tables in a database.
- Is the highest layer of abstraction in SQLAlchemy.
- Wraps the SQL Expressions and Engine to work together to interact with the database.
- Will be used in this course so we can know how to use ORM libraries in general.

SQLAlchemy is split into two libraries:

- **SQLAlchemy Core**
- **SQLAlchemy ORM**

ORM is offered as an optional library so you don't have to use the ORM in order to use the rest of Alchemy.
_ The ORM uses the core library inside
_ The ORM lets you **map** from the database schema to the applications Python object \* The ORM persists objects into corresponding database tables.

![layers of abstraction detailed](https://video.udacity-data.com/topher/2019/August/5d4de779_sqlalchemy-layers-of-abstraction/sqlalchemy-layers-of-abstraction.png)

- The Engine layer is the lowest level of abstraction a lot like interacting directly with a DB-API.
- The Dialect layer makes it possible to interact with any database management system.
- The Connection Pool layer avoids opening and closing connections for all data changes.
- The SQL Expressions layer lets you compose SQL statements by building Python objects.
- The ORM Layer Highest level of abstraction, maps classes to tables.

# 8. Mapping Between Tables and Classes

Example class = Human

```
class Human:
    def __init__(self, first_name, last_name, age):
    self.first_name = first_name
    self.last_name  = last_name
    self.age        = age
```

Is equivalent to the following

```
CREATE TABLE humans (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    age INTEGER
);
```

**TABLES** map to **CLASSES**
**TABLE RECORDS** map to **OBJECTS**
**TABLE COLUMNS** map to **ATTRIBUTES**

## 9. Hello App with Flask-SQLAlchemy

Flask is a Python web framework.
Start by installing flask with pip3 => to use in a python script use
`pip3 install flask` `from flask import flask`
Then install Flask-SQLAlchemy with pip3 => to use in a python script use
`pip3 install flask-sqlalchemy` `from flask_sqlalchemy import SQLAlchemy`

> See the folder named SQLAlchemy for the python scripts detailed below.

We will be creating a Hello, {name} Application where {name} is read from a database

You can run a flask app with the following in your terminal, the =... should point to the .py file.
`FLASK_APP=flask-hello-app.py flask run` - This will be running on localhost:\$PORT
`if __name__ == '__main__':` - You can run the app using `python3 app.py` if you include this at the bottom of your .py script

`export FLASK_ENV=development` - If you run this first you will enable debugger mode which will allow live reloading.

### Exercise 1

- [x]Write a Flask App that outputs 'Hello World!'
- [x]Run the Application in debug mode.
- [x]Use the method outline above to run the application using `python3 app.py` instead, using the `if **name** == '**main**':

```
# import flask
from flask import Flask

# initialize the app
app = Flask(__name__)

#route handler
@app.route('/')
def index():
    return 'Hello World!'

# this runs the app meaning you can call `python3 app.py` instead of using the full FLASK_APP=app.py ...
if __name__ == '__main__':
  app.run()
```

## 10. Connecting to the Database - Hello App

1. Start by importing the Flask-SQLAlchemy library
2. Set the database using `db = SQLAlchemy(app)` - This will link an instance of the database
3. Connect to the DB with a configuration variable. Set on `app.config['SQLALCHEMY_DATABASE_URI'] = '' URI is set with all caps and \_ in between
4.
5.

Database URI

![Database URI](https://video.udacity-data.com/topher/2019/August/5d4df44e_database-connection-uri-parts/database-connection-uri-parts.png)

## 11. db.model and Defining Models

- db is an interface for interacting with our database
- `db.Model` lets us create and manipulate **data models**
- `db.session` lets us create and manipulate **database transactions**

### Creating a `person` class with `db.model`

**Declaring Classes**

- Declare classes with `class MyModel(db.Model) will inherit from`db.Model`
- By inheriting from db.Model, we map our classes to tables via SQLAlchemy ORM

**Defining Columns**

- Within our class, we declare attributes equal to `db.Column(...)`
- `db.Column` takes `<datatype>, <primary_key?> <constraint?>, <default?>`

**Table naming**

- By default, SQLAlchemy will pick the name of the table for you, setting it equal to the lower case version of your class's name. Otherwise , we set the name of the table using.

`__tablename__ = 'custom_table_name'`

## 12. Syncing Models, db.create_all()

We need to create the tables in our database using `db.create_all()` which creates tables if they do not exist.

## 13. Inserting Records

We'll finish off creating a Hello App that says hello to our name by inserting a record into the persons table in our database, and showing the person's name on the index route.

INSERT the record using PSQL, then query the database using the following snippet.

```
person = Person.query.first()
```

FULL APP CODE

```
flask-hello-app.py

# import flask
from flask            import Flask
from flask_sqlalchemy import SQLAlchemy

# initialize the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/example'
db = SQLAlchemy(app)

# tells postgres to create a table called persons with an id and name column
class Person(db.Model):
  __tablename__ = 'persons'
  id   = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)

# creates all tables as long as they do not exist
db.create_all()

#route handler
@app.route('/')
def index():
  person = Person.query.first()
  return 'Hello ' + person.name

# this runs the app
if __name__ == '__main__':
  app.run()
```

## 14. Interactive Mode

We can experiment with our app using the interactive mode of the Python interpreter.

1. Activate the interactive mode by typing `python3`
2. Make sure you rename the app from `flask-hello-app.py` to `flask_hello_app.py` so we can import it with Python
3. import the app by running `import flask_hello_app`
4. If you get the depreciation warning, modify the app to set `app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False`

Run the following

```
from flask_hello_app import Person, db
Person.query.all()
Person.query.first()
query = Person.query.filter(Person.name == 'Mac')
query.first()
query.all()
```

You can also add the following code to the .py file which allows us to print results as a string, which is useful for debugging.

```
def **repr**(self):
return f'<Person ID: {self.id}, name: {self.name}>'
```

Then when you print a query containing a Person it will print `<Person ID: 1, name: Mac>`

You can also add things to the string `Hello + <Person ID: 1, name: Mac>`

### Inserting records from Python Interactive Mode

you can call `db.session` from SQLAlchemy to create records in Python interactive mode

Create an instance of a Person, setting attributes and setting it to the variable person
Next call db.session.add() to add this object to the session
This will queue up a statement in a transaction that is managed by db.session.
And that person's record will now exist in our `persons` table within our database. We can check this by running

```
cd PROJECT_DIRECTORY
python3
from flask_hello_app import db, Person
person = Person(name='Name')
db.session.add(person)
db.session.commit()
psql
SELECT \* from persons;
```

## 15. SQLAlchemy Data Types

![data types](https://video.udacity-data.com/topher/2019/August/5d5a43a0_screen-shot-2019-08-18-at-11.36.57-pm/screen-shot-2019-08-18-at-11.36.57-pm.png)

## 16. SQLAlchemy Constraints

Constraint ensures data integrity across a database.
e.g.
Python SQL
`nullable = False` is = to `NOT NULL`
`unique=True` is = to `UNIQUE`

## 17. Recap

SQLAlchemy Core vs SQLAlchemy ORM

![SQLAlchemy Core vs SQLAlchemy ORM](https://video.udacity-data.com/topher/2019/August/5d5a4854_sqlalchemy-layers/sqlalchemy-layers.png)

# Lesson 4: SQAlchemy ORM In Depth

## 1. Introduction

Open up Python3 in the SQLALchemy directory and import the database Person from flask_app

`from flask_hello_app import db, Person`

Then run `Person.query.all` to see all entries into the table. Looks as follows\*

`[<Person ID: 1, name: Mac>, <Person ID: 2, name: Name>, <Person ID: 3, name: Him>, <Person ID: 4, name: Her>]`

`Person.query.filter_by(name='Mac')` returns the following
`<flask_sqlalchemy.BaseQuery object at 0x7f1f67a38af0>`

and just `Person.query` returns the first entry in the same format.
`<flask_sqlalchemy.BaseQuery object at 0x7f1f67a38af0>`

With the latter two you won't see the results until you add `.all`
`<flask_sqlalchemy.BaseQuery object at 0x7f1f67a38af0>` - filter_by
`[<Person ID: 1, name: Mac>, <Person ID: 2, name: Name>, <Person ID: 3, name: Him>, <Person ID: 4, name: Her>]` - Person.query

> \*at time of writing

## Adding multiple objects

```
person1 = Person(name='Boy')
person2 = Person(name='Girl')
db.session.add_all(person1, person2)
db.session.commit()
Person.query.all()

RETURNS
[<Person ID: 1, name: Mac>, <Person ID: 2, name: Name>, <Person ID: 3, name: Him>, <Person ID: 4, name: Her>, <Person ID: 5, name: Boy>, <Person ID: 6, name: Girl>]
```

You can also exit Python3 and see the records in psql.

## 2. Model.query

Model.query

- Source of all SELECT statements generated by the ORM
- Person.query.filter_by(name='Mac') - Filters results by the constraints within the parentheses.
- Person.query.all() - like SELECT \*, shows All entries
- Person.query.count() - Like a GROUP BY COUNT in SQL
- Person.query.filter(Person.name == 'Mac') - A flexible way of filtering results
- Person.query.filter(Person.name == 'Mac', Team.name == 'Dev/Des.co) You can filter by comma separated models.
- Person.query.get(1) - Gets an object by Primary Key

- Product.query.filter_by(category='Misc').delete() - Will filter by the category misc. and then delete all records the db finds.

**Method Chaining**
You can do the following and see the same results Queries are infinitely nestable until you need to fetch a result.

```
Person.query
  .filter(Person.name == 'Mac')
  .filter(Team.name == 'Dev/Design.co)
  .first()
```

Example

> There are two tables Driver and Vehicles, we can join the two, filter by driver_id=3, then return all results from both tables.

```
Driver.query
  .join('vehicles')
  .filter_by(driver_id=3)
  .all()
```

You can access query objects in two ways.
`Person.query` which is the same as `db.session.query(Person)`
This is useful for if you want to do a joint query
`session.query(Person).join(Team)

## 3. SQAlchemy Object Lifecycle - Part 1

- Within a session, we create **transactions** every time we want to commit work to the database.
- Proposed changes are not immediately committed to the database and instead go through stages to allow for undos.
- The ability to undo is allowed via `db.session.rollback()`

It is when we run `db.session.commit` that all changes are committed.

A Flush takes pending changes and translates them into SQL commands, ready to be committed to the database.
On INSERTS a flush allows future primary key values to exist.
NOT the same as a commit - Nothing is persisted to the database yet when a flush happens.

### Stages:

1. **Transient:** an object exists, it was defined.
   `user1=User(name='Mac')
2. **Pending:** an object was attached to a session. "Undo becomes available via `db.session.rollback(). Waits for a flush to happen
3. **Flushed:** about ready to be committed to the database, translating actions into SQL command statements for the engine.
4. **Committed:** manually called for a change to persist to the database; session's transaction is cleared for a new set of changes.

## 4. SQAlchemy Object Lifecycle - Part 2

- A **flush** takes pending changes, and translates them into commands ready to be committed. It occurs:
  - when you call `Query`. Or
  - on `db.session.commit()

A commit creates persistent changes on the database AND lets the db.session start with a new transaction.

When a statement has been flushed already, SQLAlchemy knows not to do the work of translating actions to SQL statements.

> Flush occurs whenever a `query` or `commit()` is called.

# Building a CRUD App with SQLAlchemy

## 1. Introduction

**Create** INSERT
**Read** SELECT
**Update** UPDATE
**Delete** DELETE

### Building out a CRUD application.

So far I have covered the conceptual foundation needed to understand how to do real-world b development across the stack. In the next lessons I will be building a fully function application.

#### Creating a CRUD To-Do App

**Create** INSERT - When a user creates something, it updates to the database.
**Read** SELECT - A user can read things already stored on the database.
**Update** UPDATE - A user can update the items within a databse.
**Delete** DELETE - A user can delete things from the databse.
will be using ORM which means whenever a user wants to create something it is added to the Python3 session which will create the SQL Expressions for me.

ORM Commands
**Create/INSERT** `db.session.add(user1)`
**Read/SELECT** `User.query.all()`
**Update/UPDATE** `user1.foo = 'new value`
**Delete/DELETE** `db.session.delete(user1)`

### The App

The user will be able to create and delete lists that contains a list of todo items, each to-do item is something the user wants to complete, the user should be able to create new to-do's, update them, check them off and delete them.

#### Using

- Model View Controller - MVC Pattern - One of the most common patterns for architecting a full stack application
- Migrations - Are necessary for changing our data schema in the future when there may already be data in the database
- Modelling Relationships - Modelling relationships in ORM in a way that reflects the real relationships in our app
- Implementing Search

## 2. Create a Dummy ToDo App

Flask allows you to use data from HTML templates. Flask uses a templating engine called Jinja, which allows you to put non-HTML within an HTML file it processes the file and replaces **template strings** with **strings** and renders the file to the user.

Add comments to this code later to show what each step does.
app.py

```
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index() -
    return render_template('index.html', data=[{
        'description' - 'Todo 1'
    },{
        'description' - 'Todo 2'
    },{
        'description' - 'Todo 3'
    },])
```

index.html

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo App</title>
</head>
<body>
    <ul>
        {% for d in data %}
        <li>{{ d.description }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```

## 3. Reading ToDo Items - The "R" In CRUD

In this section read operations are used, querying the database t oreturn backed views, replacing our dummy data with "real" data coming from a database.

> SQLAlchemy is not able to create your database for you, so it has to be created manually using `createdb`

```
app.py
from flask            import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres -//postgres -postgres@localhost -5432/todoapp'
db = SQLAlchemy(app)

class Todo(db.Model) -
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self) -
        return f'<Todo {self.id} {self.description}>'

db.create_all()

@app.route('/')
def index() -
    return render_template('index.html', data=Todo.query.all())
```

## 4. Model View Controller (MVC)

- **MVC** stands for Model-View-Controller, a common pattern for architecting b applications
- Describes the 3 layers of the application are developing.

### Layers

    * **Models -** manage *data* and *business logic*. What happens inside models and database, capturing logical relationships and properties across the b app objects
    * **Views -** handles *display and representation logic*. What the user sees (HGTML, CSS, JS from the users' perespective)
    * **Controllers -** routes commands to the models and views, containing *control logic* Control how commands are sent to models and views, and how models and views wound up interacting with each other.

![Model-View Controller Diagram](https -//video.udacity-data.com/topher/2019/August/5d5dc48f_screen-shot-2019-08-21-at-3.23.56-pm/screen-shot-2019-08-21-at-3.23.56-pm.png)

## 5. Handling User Input

Creating, updating and deleting information from a database requires handling user input on what is being created/updated/deleted.

#### MVC Development - How to add Create To-Do item functionality

    * On the view -       implement an HTML form
    * On the controller - retrieve the user's input and manipulate models
    * On the models -     create a record in our database, and return the newly created to-do item to the controller
    * On the controller - take the newly created to-do item and decide how to update the view with it.

#### Learn

1. **How accep and get user data** in the context of a Flask app
2. **Send data in controllers** using database sessions in a controller
3. **Manipulating models** adding records in SQLAlchemy Models
4. **Direct how the view should update** within the controller and views

## 6. Getting User Data In Flask - Part 1

There are three methods for getting user data in flask
_ URL query paramaters
_ Forms \* JSON

#### URL query parameters

- Listed as key-value pairs at the end of a URL, preceding a '?' e.g. `www.example.com/hello?my_key=my_value`.

#### Form Data

- `reuqest.for.get('<name>')` reads the value from a form input (text, number, password, etc.) by the name attrivute on the input HTML element.

  > Defaults
  >
  > - `request.args.get`, `request.form.get` both accept an optional second parameter, e.g. `request.args.get('foo', 'my default')`, set to a default value in case the result is empty.

#### JSON - the more modern way.

- `reques.data` retrieves JSON _as a string_. Then I can use that string by turning it into python constructs, calling `json.loads` on the `request.data` string to turn it into lists and dictionaries in Python.

* Forms take an `action` (name of the route) and `method`(route method) to submit data to our server.
* the `name` attribute on a form control element is the key used to retrieve data from `request.get(<key>).
* All forms either define a submit button, or allow the user to hit ENTER on an input to submit the form.

> for the todo app the form method will be used.

Example form
![Submit Data with HTML Forms](https -//i.imgur.com/A0ShmaM.png)

### Form methods `POST` vs `GET`

- The way form data traverses from thje client to server differes based on whether are using a GET or a POST method.

**The Post Submission**

- On submit, send off an hTTP POST request to the route `/create` with a **request body**
- The requesy body stringifies the key-value pairs of fields from the form ( as part of the `name` attribute) along with their values.

**The GET Submission**

- Sends off a GET request with **URL Query Paramaters** that appends the form data to the URL.
- Ideal for smaller form submissions.

> POSTs are best for longer form submissions, since URL query parameters can only be so long compared to request bodies (max 2048 chars.) forms can only send POST and GET requests, nothing else.

## 7. Getting User Data In Flask - Part 2

Begin implementing the Create To-Do Item functionality in the To-Do app.

```
app.py

from flask import Flask, render_template, request, redirect, url_for # added request, url_for and redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres -//postgres -postgres@localhost -5432/todoapp'
db = SQLAlchemy(app)

class Todo(db.Model) -
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)

  def __repr__(self) -
    return f'<Todo {self.id} {self.description}>'

db.create_all()

# altered this code
@app.route('/todos/create', methods=['POST'])
def create_todo() -
    description = request.form.get('description', '')
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/')
def index() -
  return render_template('index.html', data=Todo.query.all())
```

```
index.html

<html>
  <head>
    <title>Todo App</title>
  </head>
  <body>
  <!-- added form -->
    <form method="post" action="/todos/create">
      <input type="text" name="description" />
      <input type="submit" value="Create" />
    </form>
    <ul>
      {% for d in data %}
      <li>{{ d.description }}</li>
      {% endfor %}
    </ul>
  </body>
</html>

```

This app has the following. 1. View - HTML Form 2. Controller - Receives the form submission 3. Model interactions - within the controller

## 8. Using AJAX to send data to flask

Data requests are either synchronous or async(asynchronous)
Async data request are requests that get sent to the server and back to the client without a page refresh.
Async request(AJAX Requests) use one of two methods -
_ XMLHtppRequest
_ Fetch(Modern Way)

> Axios or Jquery are libraries used for sending AJAX requests.

#### Using XMLHttpRequest

```
var xhttp = new XMLHttpRequest();

description = document.getElementById("description").value;

xhttp.open("GET", "/todos/create?description=" + description);

xhttp.send();
```

```
ONSUCCESS
xhttp.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
      // on successful response
      console.log(xhttp.responseText);
    }
};
```

#### Using FETCH

```
fetch('/my/request', {
  method - 'POST',
  body - JSON.stringify({
    'description' - 'some description here'
  }),
  headers - {
    'Content-Type' - 'application/json'
  }
});
```

```
app.py

```

```
index.html

<html>
  <head>
    <title>Todo App</title>
    <!--Added Style -->
    <style>
      .hidden{display - none;}
    </style>
  </head>
  <body>
    <form id="form">
      <input type="text" name="description" />
      <input type="submit" value="Create" />
    </form>
    <div id="error" class="hidden">Something nt wrong</div>
    <ul>
      {% for d in data %}
      <li>{{ d.description }}</li>
      {% endfor %}
    </ul>
  </body>
  <!-- added script-->
  <script>
    document.getElementById('form').onsubmit = function(e) {
      e.preventDefault();
      fetch('/todos/create', {
        method - 'POST',
        body - JSON.stringify({
          'description' - document.getElementById('description').value
        }),
        headers - {
          'Content-Type' - 'application/json'
        }
      })
      .then(function(response) {
        return response.json();
      })
      .then(function(jsonResponse) {
        console.log(jsonResponse);
        const liItem = document.createElement('LI');
        liItem.innerHTML = jsonResponse['description'];
        document.getElementById('todos').appendChild(liItem)
        document.getElementById('error').className = 'hidden';
      })
      .catch(function() {
        document.getElementById('error').className = '';
      })
    }
  </script>
</html>
```

## 9. Using sessions in controllers

Commits can succeed or fail. On fail, want to rollback the session to avoid potential implicit commits done by the database.
Good practice is to close connections at the end of every session

#### Pattern (try-except-finally)

```
 import sys

 try -
   todo = Todo(description=description)
   db.session.add(todo)
   db.session.commit()
 except -
   db.session.rollback()
   error=True
   print(sys.exc_info())
 finally -
   db.session.close()
```

```
app.py

from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres -//postgres -postgres@localhost -5432/todoapp'
db = SQLAlchemy(app)

class Todo(db.Model) -
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)

  def __repr__(self) -
    return f'<Todo {self.id} {self.description}>'

# edits here
@app.route('/todos/create', methods=['POST'])
def create_todo() -
  error = False
  body = {}
  try -
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
  except -
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally -
    db.session.close()
  if error -
    abort (400)
  else -
    return jsonify(body)

@app.route('/')
def index() -
  return render_template('index.html', data=Todo.query.all())
```

> expire_on_commit - defaults to TRue. When True, all instances will be fully expired after each commit()
> to avoid this add `db= SQLAlchemy(app, session_options={"expire_on_commit" - False})

## 10. Recap

Next adding how to change data models over time.

# Building a CRUD App with SQLAlchemy - Part 2

## 1. Introduction

- Implementing update functionality: update a todo item's completed state
- Implementing delete functionality: remove a todo item
- Model relationships beten objects in SQL and SQLAlchemy
  - Setting up Foreign Key constraints
  - Building CRUD on Lists of To-Do items
- Handling the special case of modeling many-to-many relationships

## 2. Updating a Todo Item Part 1

UPDATE
In SQL```
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;

````
In SQLAlchemy ORM```
    user = User.query.get(some_id)
    user.name = 'Some new name'
    db.session.commit()
````

Updating a ToDo Item using if statements in Jinja

1. Add check boxes to `index.html` `<li><input type="checkbox" {% if d.completed %} checked {% endif %}>{{ d.description }}</li>`
2. Add an event listener and function that runs an update when the boxes are checked. This will cause an console log when checkbox state changes.
   ```
   const checkboxes = document.querySelectorAll('.check-completed');
   for (let i = 0; i < checkboxes.length; i++) {
     const checkbox = checkboxes[i];
     checkbox.onchange = function(e){
       console.log('event', e);
     }
   }
   ```

## 3. Updating a Todo Item Part 2

Next define a handler for the checkbox ticks in app.py
Also adding the todo id to the url in both the front end and the backend so that will be

```
   <li>
      <input class="check-completed" data-id="{{ todo.id }}" type="checkbox" {% if todo.completed %} checked {% endif %} />
      {{ todo.description }}
    </li>
```

```
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
try:
  completed = request.get_json()['completed']
  print('completed', completed)
  todo = Todo.query.get(todo_id)
  todo.completed = completed
  db.session.commit()
except:
  db.session.rollback()
finally:
  db.session.close()
return redirect(url_for('index'))
```

Make sure to add this to the index route so that the todo items are always in order of last created.

```
  return render_template('index.html', todos=Todo.query.order_by('id').all())
```

## 4. DELETE A Todo Items

Add a button next to the li that contains an X that users can delete the to do item with
The following expressions are used

```
SQL

DELETE FROM table_name
WHERE condition;

ORM

todo = Todo.query.get(todo_id)
db.session.delete(todo) # or...
Todo.query.filter_by(id=todo_id).delete()
db.session.commit()
```

## 5. Intro - Modeling Relationships

> The relationships beten these models can determine if certain actions on one model should happen on other models, so that when something happens to one model, related model objects should also be affected (by being created, read, updated, or deleted).

## 6. Review - Relationships & Joins

> An INNER join selects all rows from both tables that have a match beten the columns, specifying JOIN with no prefixes defaults to an INNER join

## 7. db.relationship

- SQLAlchemy configures the settings beten model relationships once, and generates JOIN statements for us whenever need them.
- db.relationship is an interface offered in SQLAlchemy to provide and configure a mapped relationship beten two models.
- db.relationship is defined on the parent model, and it sets:
  - the name of its children (e.g. children), for example parent1.children
  - the name of a parent on a child using the backref, for example child1.my_amazing_parent

![Parent class 'SomeParent' and Child class 'SomeChild'](https://video.udacity-data.com/topher/2019/August/5d5f5ed0_screen-shot-2019-08-22-at-8.34.29-pm/screen-shot-2019-08-22-at-8.34.29-pm.png)

## 9. Configuring Relationships

> When calling child1.some_parent, SQLAlchemy determines when load the parent from the database.

Why is it important to care about when load parents?

- Joins are expensive.
- avoid having the user idling. Delays more than 150ms are noticeable, so milliseconds of performance matter!
- make sure the joins happen during a time and place in the UX that doesn't negatively impact the experience too much.

## 10. Foreign Key Constraint Setup

`db.relationship` does not set up foreign key constraints for you. add a column, `some_parent_id`, on the **child** model, set the foreign key constraint on the **child** model

Whereas set `db.relationship` on the **parent** model, set the foreign key constraint on the **child** model.

A foreign key constraint prefers **referential integrity** from one table to another, by ensuring that the foreign key column always maps a
primary key in the foreign table.

`db.ForeignKey`

- Option in db.column to specify a foreign key constraint, referring to the primary key of the other table / model
- Gets defined on the Child model

## 11. One-to-Many Relationship Setup

1. Modified the todo model to allow null values in list_id:
   `list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=True)`
2. Ran the migration, allowing `list_id` to be null

`see update file here SQL/todo/migrations/versions/916708d2db29_.py`

Then in psql

1. populated database with a default list("uncategorized)
2. Associated existing to-do items with the "Uncategorized" list with ID 1, setting todo.list_id = 1. We could have also done this in a migration rather than using psql; either works.
3. Set nullable=False on the list_id column
4. Ran flask db migrate to generate a migration file for updating the nullability constraint
5. Ran flask db upgrade to apply the migration

# All is done except list_id doesn't show and

## 12. CRUD on a List of To-Do

### Challenge yourself

    * Create a list: Implement a create list form, similar to the To-Do Item.
    * Update a list (and all children of the list.)
    * Delete a list: make the lists deletable, similar to the remove a todo.

## 13. Many-To-Many Relationships - Part 1

In one-to-many relationships, the foreign key is established on the child model.

In many-to-many a special association table exists to join the two tables together, storing two foreign keys that link to the two foreign tables that have relationships with each other.

## 14. Many-To-Many Relationships - Part 2

To setup many-to-many in SQLAlchemy

1. Define an association table using `Table` from SQLAlchemy
2. Set the multiple foreign keys in the association table
3. Map the association table to a parent model using the option `secondary` in `db.relationship`

### Example with Order, Product and Order Item

```
order_items = db.table('order_items',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer,db.ForeignKey('product.id'), primary_key=True)
)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(), nullable=False)
    products = db.relationship('Product', secondary=order_items,
        backref=db.backref('order', lazy=True))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
```

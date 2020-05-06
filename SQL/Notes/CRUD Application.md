# Building a CRUD App with SQLAlchemy

## 1. Introduction

**Create** INSERT
**Read** SELECT
**Update** UPDATE
**Delete** DELETE

### Building out a CRUD application.

So far I have covered the conceptual foundation needed to understand how to do real-world web development across the stack. In the next lessons I will be building a fully function application.

#### Creating a CRUD To-Do App

**Create** INSERT - When a user creates something, it updates to the database.
**Read** SELECT - A user can read things already stored on the database.
**Update** UPDATE - A user can update the items within a databse.
**Delete** DELETE - A user can delete things from the databse.
We will be using ORM which means whenever a user wants to create something it is added to the Python3 session which will create the SQL Expressions for me.

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
def index():
    return render_template('index.html', data=[{
        'description': 'Todo 1'
    },{
        'description': 'Todo 2'
    },{
        'description': 'Todo 3'
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

## 3. Reading ToDo Items: The "R" In CRUD

In this section read operations are used, querying the database t oreturn backed views, replacing our dummy data with "real" data coming from a database.

> SQLAlchemy is not able to create your database for you, so it has to be created manually using `createdb`

```
app.py
from flask            import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres@localhost:5432/todoapp'
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

db.create_all()

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())
```

## 4. Model View Controller (MVC)

- **MVC** stands for Model-View-Controller, a common pattern for architecting web applications
- Describes the 3 layers of the application we are developing.

### Layers

    * **Models:** manage *data* and *business logic*. What happens inside models and database, capturing logical relationships and properties across the web app objects
    * **Views:** handles *display and representation logic*. What the user sees (HGTML, CSS, JS from the users' perespective)
    * **Controllers:** routes commands to the models and views, containing *control logic* Control how commands are sent to models and views, and how models and views wound up interacting with each other.

![Model-View Controller Diagram](https://video.udacity-data.com/topher/2019/August/5d5dc48f_screen-shot-2019-08-21-at-3.23.56-pm/screen-shot-2019-08-21-at-3.23.56-pm.png)

## 5. Handling User Input

Creating, updating and deleting information from a database requires handling user input on what is being created/updated/deleted.

#### MVC Development: How to add Create To-Do item functionality

    * On the view:       implement an HTML form
    * On the controller: retrieve the user's input and manipulate models
    * On the models:     create a record in our database, and return the newly created to-do item to the controller
    * On the controller: take the newly created to-do item and decide how to update the view with it.

#### Learn

1. **How we accep and get user data** in the context of a Flask app
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
![Submit Data with HTML Forms](https://i.imgur.com/A0ShmaM.png)

### Form methods `POST` vs `GET`

- The way form data traverses from thje client to server differes based on whether we are using a GET or a POST method.

**The Post Submission**

- On submit, we send off an hTTP POST request to the route `/create` with a **request body**
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres@localhost:5432/todoapp'
db = SQLAlchemy(app)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)

  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

db.create_all()

# altered this code
@app.route('/todos/create', methods=['POST'])
def create_todo():
    description = request.form.get('description', '')
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/')
def index():
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

This app has the following. 1. View: HTML Form 2. Controller: Receives the form submission 3. Model interactions: within the controller

## 8. Using AJAX to send data to flask

Data requests are either synchronous or async(asynchronous)
Async data request are requests that get sent to the server and back to the client without a page refresh.
Async request(AJAX Requests) use one of two methods:
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
  method: 'POST',
  body: JSON.stringify({
    'description': 'some description here'
  }),
  headers: {
    'Content-Type': 'application/json'
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
      .hidden{display: none;}
    </style>
  </head>
  <body>
    <form id="form">
      <input type="text" name="description" />
      <input type="submit" value="Create" />
    </form>
    <div id="error" class="hidden">Something went wrong</div>
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
        method: 'POST',
        body: JSON.stringify({
          'description': document.getElementById('description').value
        }),
        headers: {
          'Content-Type': 'application/json'
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

Commits can succeed or fail. On fail, we want to rollback the session to avoid potential implicit commits done by the database.
Good practice is to close connections at the end of every session

#### Pattern (try-except-finally)

```
 import sys

 try:
   todo = Todo(description=description)
   db.session.add(todo)
   db.session.commit()
 except:
   db.session.rollback()
   error=True
   print(sys.exc_info())
 finally:
   db.session.close()
```

```
app.py

from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres@localhost:5432/todoapp'
db = SQLAlchemy(app)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)

  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

# edits here
@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)

@app.route('/')
def index():
  return render_template('index.html', data=Todo.query.all())
```

> expire_on_commit - defaults to TRue. When True, all instances will be fully expired after each commit()
> to avoid this add `db= SQLAlchemy(app, session_options={"expire_on_commit": False})

## 10. Recap

Next adding how to change data models over time.

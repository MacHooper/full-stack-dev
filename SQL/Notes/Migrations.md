# Migrations

## 1. Introduction

**Migrations or Schema Migrations**

- Migrations deal with how we manage modifications to our data schema, over time.
- Mistakes to our database schema are very expensive to make. The entire app can go down, so we want to
  - quickly roll back changes, and
  - test changes before we make them
- A migration is a file that keep track of changes to our database schema (structure of our database).
  - Offers version control on our schema.

Upgrades and rollbacks

- Migrations stack together in order to form the latest version of our database schema
- We can upgrade our database schema by applying migrations
- We can roll back our database schema to a former version by reverting migrations that we applied

> doing a `git commit` is similar to applying a migration (a schema upgrade)

## 2. Migrations - Part 2

**Migrations**

- encapsulate a set of changes to our database schema, made over time.
- are uniquely named
- are usually stored as local files in our project repo, e.g. a migrations/ folder
- There should be a 1-1 mapping between the changes made to our database, and the migration files that exist in our migrations/ folder.
- Our migrations files set up the tables for our database.
- All changes made to our db should exist physically as part of migration files in our repository.

### These are 3 scripts usually needed for `migrations`

- migrate: creating a migration script template to fill out; generating a migration file based on changes to be made
- upgrade: applying migrations that hadn't been applied yet ("upgrading" our database)
- downgrade: rolling back applied migrations that were problematic ("downgrading" our database)

### Migration Library for Flask + SQLAlchemy

- Flask-Migrate is a library for migrating changes using SQLAlchemy. It uses Alembic underneath the hood.

### Flask-Migrate & Flask-Script

- Flask-Migrate (flask_migrate) is our migration manager for migrating SQLALchemy-based database changes
- Flask-Script (flask_script) lets us run migration scripts we defined, from the terminal

### Steps to get migrations going

1. Initialize the migration repository structure for storing migrations
2. Create a migration script (using Flask-Migrate)
3. (Manually) Run the migration script (using Flask-Script)

### Why Use Migrations?

Without migrations:

-We do heavy-handed work, creating and recreating the same tables in our database even for minor changes
-We can lose existing data in older tables we dropped

With migrations:

- Auto-detects changes from the old version & new version of the SQLAlchemy models
- Creates a migration script that resolves differences between the old & new versions
- Gives fine-grain control to change existing tables

This is helpful, because

- We can keep existing schema structures, only modifying what needs to be modified
- We can keep existing data
- We isolate units of change in migration scripts that we can roll back to a “safe” db state

> Migrations still need to be run manually
> Migrations are physical files stored in our local repo, that captures sets of changes to the database schema.
> FLask-Migrate manages migrations. Flask-Script is how they are run. Flask-Script is needed to apply migrations.

## 3. Flask-Migrate - Part 1

See the Flask-Migrate and Alembic docs [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) [Alembic](https://alembic.sqlalchemy.org/en/latest/)

### Installing Flask-Migrate

`pip3 install Flask-Migrate`

### Import with

`from flask_migrate import Migrate`

## 4. Flask-Migrate - Part 2

### Creating the migrations directory structure using `flask db init`

Run the initial command

`flask db init`

This will create a `migrations` folder in our project directory. This folder contains everything needed to get started with migrations

### Syncind models using `flask db migrate`

Delete the current database and recreate the databse so it's blank. Then run the command

`flask db migrate`

> This script will replace db.createall() so remove that from the py script

## 3. Flask-Migrate - Part 3

`flask db upgrade` and `flask db downgrade`

Self explanatory, these apply the updates to the database or if we are unhappy with the changes allows us to roll them back.

After running this with `\dt` in todoapp you can see `alembic_version` this table stores the current version of our database, best not to touch this table.

Now add a completed column to the Todo Model and run an upgrade to see the changes. It will autodetect the added column `todos.completed` it then interpreted the changes and stored it instide a migration file, that's named after the hash.

Then run `flask db upgrade` and the table will now contain the extra column

## 4. Flask-Migrate - Part 4

## Working with existing data

Start by Rolling back the upgrade and then inserting some data so that before the upgrade the databse isn't empty.

Then exit psql and run the upgrade again.

Terminal will return an error because the completed column is required to be `NOT NULL` but the initial entries we added didn't have anything in the completed column.

To fix this, if wew open the migration script and modify the upgrade to make the completed column 

`nullable=True` and also add the following

`op.execute('UPDATE todos SET completed = False WHERE completed IS NULL;')`

`op.alter_column('todos', 'completed', nullable=False)`

This will allow the script to run as the completed column no longer has a requirement of `NOT NULL`

- Bootstrap database migrate commands: link to the Flask app models and database, link to command line scripts for running migrations, set up folders to store migrations (as versions of the database)
- Run initial migration to create tables for SQLAlchemy models, recording the initial schema: ala git init && first git commit. Replaces use of db.create_all()

- Migrate on changes to our data models
  - Make changes to the SQLAlchemy models
  - Allow Flask-Migrate to auto-generate a migration script based on the changes
  - Fine-tune the migration scripts
  - Run the migration, aka “upgrade” the database schema by a “version”

## 5. Recap

### It's a good idea to setup migrations at the begining of an application so that changes to the schema are trackable.

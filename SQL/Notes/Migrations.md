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

## 3. Flask-Migrate - Part 1

## 4. Flask-Migrate - Part 2

## 3. Flask-Migrate - Part 3

## 4. Flask-Migrate - Part 4

## 5. Recap

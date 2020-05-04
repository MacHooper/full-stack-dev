import psycopg2

connection = psycopg2.connect('dbname=example1 user=postgres password=postgres')

# Open a cursor to perfor DB operations
cursor = connection.cursor()

# create table
# triple quotes allow multiline text in python
cursor.execute('''
    CREATE TABLE table2 (
        id INTEGER PRIMARY KEY,
        completed BOOLEAN NOT NULL DEFAULT False
    );
''')

cursor.execute('INSERT INTO table2 (id, completed) VALUES (1, true);')

# commit, so it does the executions on the db and persists in the db
connection.commit()

cursor.close()
connection.close()
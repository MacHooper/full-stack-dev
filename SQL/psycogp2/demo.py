import psycopg2

connection = psycopg2.connect('dbname=example user=postgres password=postgres')

table_name = 'todos'

# Open a cursor to perform DB operations
cursor = connection.cursor()

# drop any existing db's of the same name
cursor.execute("DROP TABLE IF EXISTS todos;")

# create table
# triple quotes allow multiline text in python
cursor.execute('''
    CREATE TABLE todos ( 
        id INTEGER PRIMARY KEY,
        completed BOOLEAN NOT NULL DEFAULT False
    );
''')

cursor.execute("insert into %s values (%%s, %%s)" % table_name, [1, True])
cursor.execute("insert into %s values (%%s, %%s)" % table_name, [2, False])
cursor.execute("insert into %s values (%%s, %%s)" % table_name, [3, True])
cursor.execute("insert into %s values (%%s, %%s)" % table_name, [4, True])
cursor.execute('insert into todos (id, completed)' + 'VALUES (%(id)s, %(completed)s);', {
    'id' : 5,
    'completed' : False
})

# fetching rows and printing to terminal
rows = 'SELECT * from todos where id < 10'
numberOfRows = cursor.execute(rows)

while True:
    row = cursor.fetchone()
    if row == None:
        break
    print(row)

# commit, so it does the executions on the db and persists in the db
connection.commit()

cursor.close()
connection.close()
# import flask
from flask            import Flask
from flask_sqlalchemy import SQLAlchemy

# initialize the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# tells postgres to create a table called persons with an id and name column
class Person(db.Model):
  __tablename__ = 'persons'
  id   = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)

# allows us to customize a printable string (useful for debugging)
  def __repr__(self):
    return f'<Person ID: {self.id}, name: {self.name}>'

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

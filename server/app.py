# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here

@app.route ('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)

    if earthquake:
        return make_response(jsonify(earthquake.to_dict()), 200)
    else:
        return make_response(
            jsonify({"message":f"Earthquake {id} not found."}),
            404
        )
    
@app.route('/earthquakes/magnitude/<float:magnitude>')

def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    quakes = [eq.to_dict() for eq in earthquakes]
    response = {
        "count":len(quakes),
        "quakes":quakes
    }

    return make_response(jsonify(response), 200)
if __name__ == '__main__':
    app.run(port=5555, debug=True)

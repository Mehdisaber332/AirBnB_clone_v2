#!/usr/bin/python3
"""script starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review


app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    """Method to remove current SQLAlchemy Session"""
    storage.close()


@app.route("/hbnb", strict_slashes=False)
def hbnb_filters():
    """Displays the main HBnB filters HTML page."""
    states = storage.all(State)
    amenities = storage.all(Amenity)
    places = storage.all(Place)
    reviews = storage.all(Review)
    return render_template("100-hbnb.html",
                           states=states, amenities=amenities, places=places,
                           reviews=reviews)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
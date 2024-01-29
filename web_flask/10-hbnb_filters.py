#!/usr/bin/python3
"""script starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    """
    display “Hello HBNB!”
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    display "HBNB"
    """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    """
    display “C ” followed by the value of the text variable
    (replace underscore _ symbols with a space )
    """
    return f"C {text.replace('_', ' ')}"


@app.route('/python', strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_text(text="is cool"):
    """
    display “Python ”, followed by the value of the text variable
    (replace underscore _ symbols with a space )
    """
    return f"Python {text.replace('_', ' ')}"


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """
    display “n is a number” only if n is an integer
    """
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """
    display a HTML page only if n is an integer
    """
    return render_template('5-number.html', n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    """
    display a HTML page only if n is an integer
    """
    num_type = "odd"
    if n % 2 == 0:
        num_type = "even"
    return render_template('6-number_odd_or_even.html', n=n, num_type=num_type)


@app.teardown_appcontext
def teardown(self):
    """Method to remove current SQLAlchemy Session"""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def get_states():
    """
    List states
    """
    states = storage.all()
    return render_template('7-states_list.html', states=states)


@app.route('/cities_by_states', strict_slashes=False)
def states_and_cities():
    """List states and cities"""
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.route('/states', strict_slashes=False)
def all_states():
    """
    display a HTML page
    """
    states = storage.all(State)
    return render_template('9-states.html', states=states, mode="all_states")


@app.route('/states/<id>', strict_slashes=False)
def state_by_id(id):
    """
    Displays a html page with citys of that state
    """
    for state in storage.all(State).values():
        if state.id == id:
            return render_template(
                '9-states.html', states=state, mode="state_by_id")
    return render_template('9-states.html', states=state, mode='None')


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """
    Display a HTML page like 6-index.html, which was done during the project
    0x01. AirBnB clone - Web static
    """
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template("10-hbnb_filters.html",
                           states=states, amenities=amenities)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)

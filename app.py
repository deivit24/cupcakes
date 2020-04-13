"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, redirect, flash, session, jsonify
# import requests

from models import db, connect_db, Cupcake
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'isaacneterothe12thchairman'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)
 
connect_db(app)

# Home Route

@app.route("/")
def root():
    """Render homepage."""

    return render_template("index.html")

# API GET Route
@app.route("/api/cupcakes")
def list_cupcakes():
    """ All cupcakes"""

    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

# API POST Route
@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Adds cupcake, and returns data about new cupcake."""

    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()

    res_json = jsonify(cupcake=cupcake.to_dict())

    return (res_json, 201)

# API GET Specific Cupcake Route

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Return data on specific cupcake."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    res_json = jsonify(cupcake=cupcake.to_dict())
    return res_json

# API PATCH update a cupcake

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update cupcake from data in request. Return updated data."""

    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    res_json = jsonify(cupcake=cupcake.to_dict())
    return res_json

# API DELETE Cupcake
@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Delete cupcake and return confirmation message. """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")
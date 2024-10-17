from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    region_type_id = db.Column(db.Integer, db.ForeignKey('region_type.id'), nullable=False)
    region_type = db.relationship('RegionType', backref=db.backref('regions', lazy=True))

class RegionType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), nullable=False)

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    weather_condition = db.Column(db.String(50), nullable=False)
    precipitation_amount = db.Column(db.Float, nullable=False)
    measurement_date_time = db.Column(db.DateTime, nullable=False)
    region = db.relationship('Region', backref=db.backref('weathers', lazy=True))

@app.route('/registration', methods=['POST'])
def register():
    data = request.json
    if not data or not data.get('email') or not data.get('password'):
        abort(400, description="Missing data")
    if Account.query.filter_by(email=data['email']).first():
        abort(409, description="Email already exists")
    new_account = Account(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password_hash=data['password']
    )
    db.session.add(new_account)
    db.session.commit()
    return jsonify({
        'id': new_account.id,
        'firstName': new_account.first_name,
        'lastName': new_account.last_name,
        'email': new_account.email
    }), 201

@app.route('/region', methods=['POST'])
def add_region():
    data = request.json
    if not data:
        abort(400, description="Missing data")
    new_region = Region(
        name=data['name'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        region_type_id=data['region_type']
    )
    db.session.add(new_region)
    db.session.commit()
    return jsonify({
        'id': new_region.id,
        'name': new_region.name,
        'latitude': new_region.latitude,
        'longitude': new_region.longitude,
        'region_type': new_region.region_type_id
    }), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, host='0.0.0.0', port=5000)

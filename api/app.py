from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime
from main import sendMenuSender
import json
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'people.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app,db)

class Recipient(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(200), nullable=False)
  name = db.Column(db.String(200), nullable=True)
  referral = db.Column(db.String(200), nullable=True)
  archived = db.Column(db.Boolean, nullable=True, default=False)
  unsubscribed = db.Column(db.Boolean, nullable=True, default=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)
  date_updated = db.Column(db.DateTime, default=datetime.utcnow)

class RecipientSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Recipient

@app.route("/renew/password", methods=["GET"])
def renewPassword():
  print("WHO")

@app.route("/send", methods=["POST"])
def sendMenu():
  data = request.get_data()
  data = json.loads(data)
  message = data["message"]
  password = data["password"]

  with open('password.txt') as f:
    password_check = f.readline()

  if password != password_check:
    return jsonify({"title": "Naughty Naughty!", "description": "Please get out of the admin area smh.", "status": "error"}), 403

  all_recipients = Recipient.query.filter(Recipient.unsubscribed != True).all()
  recipient_schema = RecipientSchema(many=True)
  recipients = recipient_schema.dump(all_recipients)

  if (message != ""):
    sendMenuSender(recipients, message)
    return jsonify({"title": "Menu Sender Send!", "description": "With your special message too!", "status": "success"}), 200
  
  sendMenuSender(recipients)
  return jsonify({"title": "Menu Sender Send!", "description": None, "status": "success"}), 200

@app.route("/recipient/subscribe", methods=["POST"])
def addRecipient():
  data = request.get_data()
  data = json.loads(data)
  email = data['email']
  name = data['name']
  referral = data['referral']

  try:
    possible_subscriber = Recipient.query.filter_by(email=email).first()
    if possible_subscriber is not None:
      if possible_subscriber.unsubscribed == True:
        possible_subscriber.unsubscribed = False
        db.session.commit()
        return jsonify({"title": "That was a success " + name.split(" ")[0], "description": "You'll start recieving emails tomorrow.", "status": "success"}), 200
      return jsonify({"title": "Oops " + name.split(" ")[0], "description": "Looks like you are already on the list!", "status": "warning"}), 200

  except Exception:
    return jsonify({"title": "Something has gone wrong", "description": "The error means that you have not been signed up.", "status": "error"}), 500

  new_recipient = Recipient(name=name, email=email, referral=referral, archived=False, unsubscribed=False)

  try:
    db.session.add(new_recipient)
    db.session.commit()
    return jsonify({"title": "That was a success " + name, "description": "You'll start recieving emails tomorrow.", "status": "success"}), 200
  except Exception:
    return jsonify({"title": "Something has gone wrong", "description": "The error means that you have not been signed up.", "status": "error"}), 500

@app.route("/recipient/unsubscribe", methods=["POST"])
def removeRecipient():
  data = request.get_data()
  data = json.loads(data)
  email = data["email"]

  unsubscriber = Recipient.query.filter_by(email=email).first()

  if unsubscriber.unsubscribed == True:
    return jsonify({"title": "Oops!", "description": "It looks like you aren't on the list!.", "status": "warning"}), 200

  unsubscriber.unsubscribed = True
  db.session.commit()

  return jsonify({"title": "I'm sad to see you go!", "description": "You won't receive any emails from now on.", "status": "success"}), 200

if __name__ == "__main__":
  app.run(debug=True)
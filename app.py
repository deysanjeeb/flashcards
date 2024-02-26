import os
from dataclasses import dataclass
from flask import Flask,request
from flask_cors import CORS, cross_origin
from flask import jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api,reqparse

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import datetime
import time
import requests
import csv

deck_parser = reqparse.RequestParser()
deck_parser.add_argument('deckName')

deck_parser.add_argument('userId')
deck_parser.add_argument('deckId')

card_parser = reqparse.RequestParser()
card_parser.add_argument('cardId')
card_parser.add_argument('deck_Id')
card_parser.add_argument('cardFront')
card_parser.add_argument('cardBack')

app = Flask(__name__)
current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///"+os.path.join(current_dir,"database.sqlite3")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

# app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///"+os.path.join(current_dir,"database.sqlite3")
# #app.config['SQLALCHEMY DATABASE URI'] = 'sqlite:///database.sqlite3'
# db = SQLAlchemy()
# db.init_app(app)

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT =  1025
SENDER_ADDRESS = "noreply@flashcards.com"
SENDER_PASSWORD = ""


def email_alert(subj, body, to):
	msg= MIMEMultipart()
	msg['Subject'] = subj
	msg['To'] = to

	msg['From']=SENDER_ADDRESS
	msg.attach(MIMEText(body, "html"))
	server=smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
	server.login(SENDER_ADDRESS,SENDER_PASSWORD)
	server.send_message(msg)
	server.quit()
	return True

@dataclass
class Users(db.Model):
	__tablename__ = 'users'
	userid: int
	username: str
	pwd: str
	email: str
	userid = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
	username = db.Column(db.String, unique=True, nullable=False)
	pwd= db.Column(db.String, nullable=False)
	email = db.Column(db.String, unique=True, nullable=False)

@dataclass
class Decks(db.Model):
	__tablename__ = 'decks'
	deck_id: int
	creator_id: str
	deck_name: str
	deck_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	creator_id = db.Column(db.String, nullable=False)
	deck_name= db.Column(db.String, unique=True, nullable=False)

@dataclass
class Cards(db.Model):
	__tablename__ = 'cards'
	card_id: int
	deck_id: int
	front: str
	back: str
	card_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	deck_id = db.Column(db.Integer, nullable=False)
	front= db.Column(db.String, nullable=False)
	back = db.Column(db.String, nullable=False)

@dataclass
class Scores(db.Model):
	__tablename__ = 'scores'
	user_id: int
	deck_id: int
	user_score: int
	time: str
	user_id = db.Column(db.Integer,  primary_key=True)
	deck_id = db.Column(db.Integer, primary_key=True)
	user_score= db.Column(db.Integer, nullable=False)
	time = db.Column(db.String, nullable=False)

app.config["JWT_SECRET_KEY"] = "top-secret"  # Change this!
jwt = JWTManager(app)
app.app_context().push()


app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
def create_app():
    cors.init_app(app=app, supports_credentials=True)

@app.route("/signup", methods=["POST"])
@cross_origin()
def signup():
	
	emailId=request.json.get('email',None)
	username=request.json.get('user',None)
	pwd=request.json.get('pwd',None)
	usr = Users(email=emailId,username=username,pwd=pwd)
	db.session.add(usr)
	db.session.commit()
	global user
	user = Users.query.filter_by(username=username,pwd=pwd).first()
	access_token = create_access_token(identity=username)
	print(access_token)
	return jsonify({ "token": access_token,"user": user})


@app.route("/login", methods=["POST"])
def login():
	if not request.is_json:
		return jsonify({"msg": "Missing JSON in request"}), 400
	username = request.json.get("user", None)
	password = request.json.get("pwd", None)
	global user
	user = Users.query.filter_by(username=username,pwd=password).first()
	# 
	if user:
		response=[]
		decks = Decks.query.filter_by(creator_id=user.userid).all()
		scores= Scores.query.filter_by(user_id=user.userid).all()
		access_token = create_access_token(identity=username)
		print(access_token)
		return jsonify({ "token": access_token,"user": user})
	else:
		return jsonify({"msg": "Bad username or password"}), 401

@app.route("/dashboard", methods=["GET"])
@cross_origin()
def dashboard():
	decks = Decks.query.filter_by(creator_id=user.userid).all()
	scores= Scores.query.filter_by(user_id=user.userid).all()
	return jsonify({"decks":decks,"scores":scores})

@app.route("/getcards/<deckid>", methods=["GET"])
@cross_origin()
def getcards(deckid):
	cards = Cards.query.filter_by(deck_id=deckid).all()
	return jsonify({"cards":cards})

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
	current_user = get_jwt_identity()
	print(current_user)
	return jsonify({"logged_in_as":current_user}), 200

@app.route("/greeting")
def greeting():
	return {"greeting": "Hello from Flask!"}

@app.route("/", methods=["GET"])
def unprotected():
	return jsonify("unprotected page"), 200

rev_cards=[]
total=0
@app.route("/review", methods=["POST"])
@cross_origin()
def review():
	deckid=request.json.get('deck_id',None)
	print("deck:",deckid)
	deck = Decks.query.filter_by(deck_id=deckid).first()
	print(deck)
	if request.method=="POST":
		global rev_cards
		total=0
		cards = Cards.query.filter_by(deck_id=deckid).all()
		print(len(cards))
		card=cards[0]
		del cards[0]
		rev_cards=cards
		print(len(rev_cards))
	
		return jsonify({"deck":deck,"type":"review","card":card})
@app.route("/review/<deckid>", methods=["POST"])
@cross_origin()
def postreview(deckid):
	cardId= request.json.get('cardId',None)
	deck = Decks.query.filter_by(deck_id=deckid).first()
	if request.method=="POST":
		cardId=request.json.get('cardId',None)
		action=request.json.get('action',None)
		global total
		print(action)
		if action=="Next":
			rating=int(request.json.get('rating',None))
			total=rating+total

			print(len(rev_cards))
			
			if(len(rev_cards)==0):
				done=True
				time=datetime.datetime.now()
				print(time)
			
				score= Scores.query.filter_by(user_id=user.userid,deck_id=deckid).first()
				if score:
					score.user_score=total
					print(score.user_score)
					score.time=time
					db.session.commit()

				else:
					score=Scores(deck_id=int(deckid),user_id=int(user.userid),user_score=total,time=time)
					db.session.add(score)
					db.session.commit()

				db.session.commit()
				decks = Decks.query.filter_by(creator_id=user.userid).all()
				scores= Scores.query.filter_by(user_id=user.userid).all()
				return jsonify({"decks":decks,"user":user,"scores":scores,"done":done})
				
			else:
				card=rev_cards[0]
				del rev_cards[0]
				done=False
				return jsonify({"deck":deck,"user":user,"type":"review","card":card,"done":done,"back":False})
		if action=="Show":
			done=False
			cardback = Cards.query.filter_by(card_id=cardId).first()
			return jsonify({"deck":deck,"user":user,"type":"review","card":cardback,"back":True,"done":done})

@app.route("/deck/create", methods=["GET","POST"])
def createDeck():
	db.session.commit()
	
	if request.method=="POST":
		deckName=request.json.get('deckName',None)

		print(deckName,user)
		r = requests.post(url='http://127.0.0.1:5000/api/decks',data = {'deckName':deckName,'userId':user.userid})
		deckId=r.text
		deck = Decks.query.filter_by(deck_id=deckId).first()

		return jsonify({"type":"create","deckid":deckId})

@app.route("/edit/<deckid>", methods=["GET","POST"])
@cross_origin()
def editDeck(deckid):
	if request.method=="GET":
		deck = Decks.query.filter_by(deck_id=deckid).first()
		cards = Cards.query.filter_by(deck_id=deckid).all()
		db.session.commit()
		if cards:
			return jsonify({"type":"edit","cards":cards,"deck":deck})		
		else:
			return jsonify({"type":"add","deck":deck})
			
	elif request.method=="POST":
		deckId=deckid
		print(deckId)
		deckName=request.json.get('deckName',None)
		
		r = requests.put(url='http://127.0.0.1:5000/api/decks',data = {'deckId':deckId,'deckName':deckName,'userId':user.userid})
		decks = Decks.query.filter_by(creator_id=user.userid).all()
		
		return jsonify({"decks":decks})	

@app.route("/deck/remove/<deckid>", methods=["GET","POST"])
def removeDeck(deckid):
	
	if request.method=="GET":
		r = requests.delete(url='http://127.0.0.1:5000/api/decks',data = {'deckId':deckid,'userId':user.userid})
		cards = Cards.query.filter_by(deck_id=deckid).all()
		for card in cards:
			r = requests.delete(url='http://127.0.0.1:5000/api/cards',data = {'cardId':card.card_id,'userId':user.userid})
		
		decks = Decks.query.filter_by(creator_id=user.userid).all()
		scores= Scores.query.filter_by(user_id=user.userid).all()
		return jsonify({"decks":decks})

@app.route("/deck/export/<deckid>", methods=["GET","POST"])
def export(deckid):
	
	if request.method=="GET":
		deck = Decks.query.filter_by(deck_id=deckid).first()
		f = open(deck.deck_name+".csv",'w')

		writer= csv.writer(f)
		cards = Cards.query.filter_by(deck_id=deckid).all()
		# for card in cards:
		writer.writerow(cards)
		f.close()
		email_alert(deck.deck_name+" export complete","The requested export has been completed.",user.email)
		decks = Decks.query.filter_by(creator_id=user.userid).all()
		scores= Scores.query.filter_by(user_id=user.userid).all()
		return jsonify({"decks":decks})

@app.route("/card/create", methods=["GET","POST"])
@cross_origin()
def createCard():
	
	db.session.commit()
	if request.method=="GET":
		cards = Cards.query.filter_by(deck_id=deckid).all()
		db.session.commit()
		return render_template("card.html" ,user=user,type="create",cards=cards,deckid=deckid)
	elif request.method=="POST":
		front=request.json.get('front',None)
		back=request.json.get('back',None)
		deckid=request.json.get('deckid',None)
		print("deckid",deckid)
		r = requests.post(url='http://127.0.0.1:5000/api/cards',data = {'deck_Id':deckid,'cardFront':front,'cardBack': back })
		cards = Cards.query.filter_by(deck_id=deckid).all()

		return jsonify({"type":"all","cards":cards,"deckid":deckid})

@app.route("/card/edit/<deckid>", methods=["GET","POST"])
@cross_origin()
def editCard(deckid):
	db.session.commit()
	if request.method=="GET":
		cards = Cards.query.filter_by(deck_id=deckid).all()
		db.session.commit()

		if cards:
			return jsonify({"type":"edit","cards":cards,"deckid":deckid})
		else:
			return jsonify({"type":"add","cards":cards,"deckid":deckid})

	elif request.method=="POST":
		front=request.json.get('front',None)
		back=request.json.get('back',None)
		cardId=request.json.get('cardId',None)
		print(front,back)
		r = requests.put(url='http://127.0.0.1:5000/api/cards',data = {'cardId':cardId,'deck_Id':deckid,'cardFront':front,'cardBack':back})
		# elif action=="Remove":
		# 	print("delete")
		# 	r = requests.delete(url='http://127.0.0.1:5000/api/cards',data = {'cardId':cardId,'deck_Id':deckid,'cardFront':front,'cardBack':back})
		# elif action=="Add":
		# 	r = requests.post(url='http://127.0.0.1:5000/api/cards',data = {'cardId':cardId,'deck_Id':deckid,'cardFront':front,'cardBack':back})
		print(r.text)
		cards = Cards.query.filter_by(deck_id=deckid).all()
	
		return jsonify({"type":"all","cards":cards,"deckid":deckid})

@app.route("/card/remove", methods=["GET","POST"])
@cross_origin()
def removeCard():
	if request.method=="GET":
		decks = Decks.query.filter_by(creator_id=userid).all()
		db.session.commit()
		if decks:
			return render_template("deck.html",user=user,type="remove",decks=decks)
	
	elif request.method=="POST":
		cardId=request.json.get('cardId',None)
		deckid=request.json.get('deck_id',None)	
		r = requests.delete(url='http://127.0.0.1:5000/api/cards',data = {'cardId':cardId,'deck_Id':deckid})
		db.session.commit()
		cards = Cards.query.filter_by(deck_id=deckid).all()
		return jsonify({"type":"all","cards":cards,"deckid":deckid})
class cards(Resource):
	def get(self,card_id):
		
		print(card_id)
		card= Cards.query.filter_by(card_id=card_id).first()
		if card:
			return{"deck_id":card.deck_id, "card_id":card_id, "front":card.front,"back":card.back}
		else:
			raise BusinessValidationError(status_code=404,error_code='',error_message="Card not found")
	def put(self):
		args = card_parser.parse_args()
		cardId=args.get("cardId")
		front=args.get("cardFront")
		back=args.get("cardBack")
		print("api",front,back,cardId)
		card = Cards.query.filter_by(card_id=cardId).first()
		if card:
			card.front=front
			card.back=back
			db.session.commit()
			card = Cards.query.filter_by(card_id=cardId).first()
			print("placed")
			return{"deck_id":card.deck_id, "card_id":card.card_id, "front":card.front,"back":card.back}
		

	def delete(self):
		args = card_parser.parse_args()
		cardId=args.get("cardId")
		print(cardId)
		card = Cards.query.filter_by(card_id=cardId).first()
		if card:
			Cards.query.filter_by(card_id=cardId).delete()
			db.session.commit()
			return{"message":"Successfully Deleted"}
		
			

	def post(self):
		args = card_parser.parse_args()
		deckId=args.get("deck_Id")
		cardFront=args.get("cardFront")
		cardBack=args.get("cardBack")
		print(deckId,cardFront,cardBack)
		# if (not isinstance(roll_number,str)) or len(roll_number)==0:
		# 	raise BusinessValidationError(status_code=400,error_code='STUDENT001',error_message="Bad request")
		# if not(isinstance(first_name,str)) or len(first_name)==0:
		# 	raise BusinessValidationError(status_code=400,error_code='STUDENT002',error_message="Bad request")
		
		card= Cards(deck_id=deckId,front=cardFront,back=cardBack)
		db.session.add(card)
		db.session.commit()
		print(card.card_id)
		card= Cards.query.filter_by(card_id=card.card_id).first()
		if card:
			return{"deck_id":card.deck_id, "card_id":card.card_id, "front":card.front,"back":card.back}
		


class decks(Resource):
	def get(self,deck_id):
		print(deck_id)
		deck = Decks.query.filter_by(deck_id=deck_id).first()
		if deck:
			return{"deck_id":deck_id, "creator_id":deck.creator_id, "deck_name":deck.deck_name}
		else:
			raise BusinessValidationError(status_code=404,error_code='',error_message="Deck not found")
		
	def put(self):
		args = deck_parser.parse_args()
		userId=args.get("userId")
		deckName=args.get("deckName")
		deckId=args.get("deckId")
		print(userId,deckId,deckName)
		deck = Decks.query.filter_by(creator_id=userId,deck_id=deckId).first()
		if deck:
			deck.deck_name=deckName
			db.session.commit()
			deck= Decks.query.filter_by(deck_id=deckId).first()
			return{"deck_id":deckId, "creator_id":deck.creator_id, "deck_name":deck.deck_name}
			# return{"message":"Successfully Edited"}
		# if not deck:
		# 	raise BusinessValidationError(status_code=404,error_code='',error_message="Deck not found")
		# # if not(isinstance(student.roll_number,str)) or len(student.roll_number)==0:
		# 	raise BusinessValidationError(status_code=400,error_code='STUDENT001',error_message="Bad request")
		# if not(isinstance(student.first_name,str)) or len(student.first_name)==0:
		# 	raise BusinessValidationError(status_code=400,error_code='STUDENT002',error_message="Bad request")

		deck= Decks.query.filter_by(deck_id=deckId).first()
		

	def delete(self):
		
		args = deck_parser.parse_args()
		deckId=args.get("deckId")
		userId=args.get("userId")
		print(deckId)
		deck = Decks.query.filter_by(deck_id=deckId,creator_id=userId).first()
		if deck:
			Decks.query.filter_by(deck_id=deckId).delete()
			db.session.commit()
			return{"message":"Successfully Deleted"}
		else:
			raise BusinessValidationError(status_code=404,error_code='',error_message="Deck not found")
		

	def post(self):
		args = deck_parser.parse_args()
		userId=args.get("userId")
		deckName=args.get("deckName")
		print(userId,deckName)

		deck= Decks(creator_id=userId,deck_name=deckName)
		db.session.add(deck)
		db.session.commit()
		return(deck.deck_id)
		# return{"deck_id":deck.deck_id, "creator_id":deck.creator_id, "deck_name":deck.deck_name}

api = Api(app)
app.app_context().push()



api.add_resource(cards, "/api/cards","/api/cards/<card_id>")
api.add_resource(decks, "/api/decks","/api/decks/<deck_id>")

if __name__ == "__main__":
	app.run(debug=True)

	
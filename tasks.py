from celery import Celery,shared_task
import os
import time
from datetime import datetime
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass
from flask import Flask,request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery.schedules import crontab

current_dir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI= "sqlite:///"+os.path.join(current_dir,"database.sqlite3")
engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

Base = declarative_base()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = Session()
Base.metadata.create_all(bind=engine)

class Users(Base):
    __tablename__ = 'users'
    userid = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    pwd= Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

class Decks(Base):
    __tablename__ = 'decks'
    deck_id = Column(Integer, autoincrement=True, primary_key=True)
    creator_id = Column(String, nullable=False)
    deck_name= Column(String, unique=True, nullable=False)

class Cards(Base):
    __tablename__ = 'cards'
    card_id = Column(Integer, autoincrement=True, primary_key=True)
    deck_id = Column(Integer, nullable=False)
    front= Column(String, nullable=False)
    back = Column(String, nullable=False)

class Scores(Base):
    __tablename__ = 'scores'
    user_id = Column(Integer,  primary_key=True)
    deck_id = Column(Integer, primary_key=True)
    user_score= Column(Integer, nullable=False)
    time = Column(String, nullable=False)



cel = Celery('tasks',backend='redis://localhost', broker='redis://localhost//')
cel.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=True,
)

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

@cel.task
def daily_review():
    users = db.query(Users).all()
    for user in users:
        reviews= db.query(Scores).filter(Scores.user_id==user.userid)
        # print(reviews)
        for review in reviews:
            deck= db.query(Decks).filter(Decks.deck_id==review.deck_id).first()
            # print(datetime.strptime(review.time,"%Y-%m-%d %H:%M:%S.%f"))
            if ((datetime.now()-datetime.strptime(review.time,"%Y-%m-%d %H:%M:%S.%f")).days>1):
                # print(deck)
                email_alert("Daily","This is reminder to login and review your deck:"+deck.deck_name,user.email)
                print("sending")


    print("See you in ten seconds!")
    return True 
cel.conf.beat_schedule = {
    "evening-reminder-task": {
        "task": "tasks.daily_review",
        # "schedule": 60,
        "schedule": crontab(hour=18,minute=0 ),
    }
}
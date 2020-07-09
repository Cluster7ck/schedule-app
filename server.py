from flask import Flask
from flask import request
from pprint import pprint
from constraint import *
import json

app = Flask(__name__)

topics = []

'''
Key: user
Value:
    [{
        "topic": string
        "importance": [0-2] 
    },...]
'''
user_prefs = {}

@app.route('/topics')
def get_topics():
    return json.dumps(topics)

@app.route('/topics/<topic>')
def post_topics(topic):
    topics.append(topic)
    return ''

@app.route('/calc')
def calc():
    topic_to_user = {}
    for topic in topics:
        topic_to_user[topic] = []

    for user in user_prefs:
        for pref in user_prefs[user]:
            if pref["importance"] > 0:
                topic_to_user[pref["topic"]].append(user)
    problem = Problem()
    problem.addVariables(range(0,16),range(0,len(topic_to_user)))
'''
    for i in range(5):
        f = lambda x : constraint(topics.)
        problem.addConstraint()
''' 
    return json.dumps(topic_to_user)

def constraint(topics, topic_dict):
    users = topic_dict.items()
    sets = iter(map(set, users))
    result = sets.next()
    for s in sets:
        result = result.intersection(s) 
    return len(result) == 0
    
@app.route('/ser_prefs', methods = ['POST', 'GET'])
def post_user_pref():
    if request.method == 'POST':
        up=request.json
        user_prefs[up["user"]]=up["prefs"]
        return ''
    if request.method == 'GET':
        return json.dumps(user_prefs)

@app.route('/')
def hello_world():
    return 'Hello, World!'

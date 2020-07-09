from flask import Flask
from flask import request
from pprint import pprint
from constraint import *
import json

app = Flask(__name__)

topics = ["default"]

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
                if pref["topic"] in topics:
                    topic_to_user[pref["topic"]].append(user)
    pprint("topic to user")
    pprint(topic_to_user)
    problem = Problem()
    topic_idxs = range(0,len(topic_to_user))
    pprint("topic_idxs")
    pprint(topic_idxs)
    problem.addVariables(range(0,15),topic_idxs)

    problem.addConstraint(MaxSumConstraint(sum(topic_idxs)))
    problem.addConstraint(MinSumConstraint(sum(topic_idxs)))
    g = lambda *v: all_in_range_once(topic_idxs, v)
    problem.addConstraint(g)
    for row in range(5):
        idxs = [row * 3 + i for i in range(3)]
        f = lambda a, b, c: constraint(a, b, c, topic_to_user)
        problem.addConstraint(f, idxs)
    
    pprint(problem.getSolution())
    return json.dumps(problem.getSolution())

def constraint(a, b, c, topic_dict):
    if (a != 0 and b != 0) and a==b:
        return False
    if (b != 0 and c != 0) and b==c:
        return False
    if (a != 0 and c != 0) and a==c:
        return False
    aa = set(topic_dict[topics[a]])
    bb = set(topic_dict[topics[b]])
    cc = set(topic_dict[topics[c]])

    if len(aa.intersection(bb)) > 0:
        return False
    if len(aa.intersection(cc)) > 0:
        return False
    if len(cc.intersection(bb)) > 0:
        return False
    return True

def all_in_range_once(r, *values):
    seen = [False for i in r]
    seen[0] = True
    #pprint(values)
    for v in list(values[0]):
        if v == 0:
            continue
        if seen[v]:
            return False
        else:
            seen[v] = True
    return all(seen)


    
@app.route('/user_prefs', methods = ['POST', 'GET'])
def post_user_pref():
    if request.method == 'POST':
        up = request.json
        user = list(up.keys())[0]
        user_prefs[user]=up[user]
        return ''
    if request.method == 'GET':
        return json.dumps(user_prefs)

@app.route('/')
def hello_world():
    return 'Hello, World!'

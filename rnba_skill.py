from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/reddit_nba")

def get_headlines():
	user_pass_dict = {'user': 'USERNAME',	#insert username and password for reddit
	                  'password':'PASSWORD',
	                  'api_type':'json'}
	sess = requests.Session()
	sess.headers.update({'User-Agent': 'Alexa Skill'})
	sess.post('https://www.reddit.com/api/login', data=user_pass_dict)
	time.sleep(0.25)
	url = 'https://www.reddit.com/r/nba/.json?limit=10'
	html = sess.get(url)
	data = json.loads(html.content.decode('utf-8'))
	titles =  [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
	titles = '...'.join([i for i in titles]) 
	return titles


@app.route('/')

def homepage():
	return "Hi, how are you doing?"

@ask.launch
def start_skill():
	welcome_message = "Hello, would you like NBA news?"
	return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
	headlines = get_headlines()
	headline_msg = 'The current top posts on reddit NBA are {}'.format(headlines)
	return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
	bye_text = "Okay then, let me know if you would like NBA news later."
	return statement(bye_text)

if __name__ == '__main__':
	app.run(debug=True)

import praw
from random import shuffle, randint
from flask import *

app = Flask(__name__)

# Updates for article in question
is_true = True
s_link = ""

@app.route("/", methods=["GET", "POST"])
def index():
	return render_template("index.html", headline=generate_headline())

@app.route("/guess", methods=["GET", "POST"])
def guess():
	print("app.py: " + str(is_true))
	print("app.py: " + s_link)
	if is_true:
		return jsonify(is_true = True, link = s_link)
	else:
		return jsonify(is_true = False, link = s_link)

# Reddit instance
reddit = praw.Reddit(client_id     = 'M4K5s4jT-5OV1g',
					 client_secret = '9MfkJKY5Wt2VkrMBzdOkojEGNJ8',
					 user_agent    = 'Onion Peeler')

realNews = []
fakeNews = []

# Fetches 100 of the hottest r/notheonion and r/theonion posts
def update_news() :

	global realNews
	global fakeNews

	# Fetch real news from r/nottheonion
	realNews = list(reddit.subreddit('nottheonion').hot(limit = 100))
	# Fetch fake news from r/theonion
	fakeNews = list(reddit.subreddit('theonion').hot(limit = 100))

# Returns a headline and also if it's true or not
def generate_headline() :

	global is_true
	global s_link

	update_news()
	shuffle(realNews)
	shuffle(fakeNews)

	r = randint(1, 2)

	# Generate real news.
	if r == 1:
		is_true = True
		s_link = realNews[0].url
		return realNews[0].title.upper()

	# Generate fake news.
	else:
		is_true = False
		s_link = fakeNews[0].url
		return fakeNews[0].title.upper()

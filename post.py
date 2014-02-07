import twitter
import bitly_api
import urllib2
import re
import random
import uuid
from BeautifulSoup import BeautifulSoup

# Set the config values in post_config.py
from post_config import cnf

# Fire up Twitter connection
api = twitter.Api(	consumer_key = cnf['twitter']['consumer_key'],
					consumer_secret = cnf['twitter']['consumer_secret'],
					access_token_key = cnf['twitter']['access_token_key'],
					access_token_secret = cnf['twitter']['access_token_secret'])

# Fire up bitly connection if specified
if cnf['bitly']['active']:
	bitly  =  bitly_api.Connection(access_token=cnf['bitly']['access_token'])

# Parse the sitemap to get the entries to choose from; search both the blog and resources section
site = cnf['params']['site']
if site[-1] != "/":
	site += "/"
rss_url = site + cnf['params']['site_sitemap']
req = urllib2.Request(rss_url)
response = urllib2.urlopen(req)
html = response.read()
entries = []
for subdir in cnf['params']['site_subdirs_regex']:
	entries += re.findall(re.escape(site + subdir) + cnf['params']['site_subdirs_regex'][subdir],html)
nEntries = len(entries)

while True:

	# Select one of the entries at random, get its title, and redo this if it needs to be excluded
	url = entries[random.randint(0,nEntries - 1)]

	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	html = response.read()
	soup = BeautifulSoup(html)

	# Extract the title, compare it to the whitelist and blacklist, and use an alternative if specified
	title = re.split(cnf['params']['title_split_regex'],soup.find("title").string)[1]

	# Try again if the entry we grabbed was in the blacklist or not in the whitelist
	if ( title in cnf['params']['blacklist_titles'] ) or ( cnf['params']['whitelist_titles'] and title not in cnf['params']['whitelist_titles'] ):
		continue

	# If we want to alter the title for this tweet, check for a match
	if title in cnf['params']['changed_titles']:
		title = cnf['params']['changed_titles'][title]

	# Grab the bitly url if specified and initialize the tweet
	if cnf['bitly']['active']:
		url = bitly.shorten(url)['url']
	tweet = "{:s} {:s} |".format(title,url)

	# Go through the meta keywords list and assume they're in descending order of importance
	# If efficient_hashtags is set and the hashtag word is already in the tweet's body then prepend a #, otherwise append it to the end
	keywords = soup.find("meta",{"name":"keywords"})['content'].replace(" ","").split(",")

	j = 0
	while keywords and len(tweet)<=135 and j < len(keywords):
		if cnf['params']['efficient_hashtags'] and  " {:s} ".format(keywords[j].lower()) in " {:s}".format(tweet.lower()) and len(tweet)+1 <= 135:
			location = " {:s}".format(tweet.lower()).find(" {:s} ".format(keywords.pop(j).lower()))
			tweet = tweet[:location] + "#" + tweet[location:]
		elif len(tweet) + len(keywords[j]) + 2 <= 135:
			tweet += " #{:s}".format(keywords.pop(j))
		else:
			j += 1

	# Prevents duplicate status error
	append = " " + "".join(random.sample(uuid.uuid4().hex,min(8,138-len(tweet))))
	tweet += append

	status = api.PostUpdate(tweet)

	break

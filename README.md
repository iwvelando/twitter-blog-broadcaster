# twitter-blog-broadcaster

# Purpose

This Twitter bot's purpose is to periodically (and relatively frequently) tweet articles from your website or blog using relevant and meaningful hashtags so that anyone searching by hashtag might find your relevant article. As this tweeting is performed fairly frequently (I presently set it to tweet twice per hour) this is not a suitable bot to solicit followers for as it would be very spammy and redundant for a single site.

The mechanism this bot uses is to parse a sitemap and select a random article with which to form a tweet with the following format:

\[Page Title of Article\] \[URL\] | #metaKeyword1 #metaKeyword2 #metaKeyword3 [Random UUID-based string to prevent duplication]

Optionally, if set in the configuration file, if a metaKeyword is found in the title it will hashtag that word instead of appending it after the URL. While this is more space-efficient, depending on the title and keywords this may produce obnoxious tweets that look like hashtag spam and obfuscate the URL. This mode is to be used with care.

# Requirements

## Python Modules

The Python script has been tested in Python 2 and you can view all the explicit modules used in post.py, but the nonstandard ones are:

* [python-twitter](https://github.com/bear/python-twitter)
* [bitly\_api](https://github.com/bitly/bitly-api-python)

which may be installed with pip:

    sudo pip install bitly_api python-twitter

## Twitter API Credentials

You will need to create an application with **read and write** access at:

https://twitter.com/login?redirect_after_login=https%3A//apps.twitter.com/

and the four credentials will be supplied in the config file.

## (Optional) Bit.ly API Credential

To shorten the links you tweet via bit.ly (mainly so you can track clicks) you'll need a credential from:

https://bitly.com/a/oauth_apps

which will be supplied in the config file.

# Configuration

## post\_config.py

The *post\_config.py.example* file will need to be populated with certain information to suit your site.

* *twitter*: place the four API credentials here
* *bitly*: if active is set to True, supply the API credential
* *params*
 * *date\_show*: When set to True, the page is searched for a tag like &lt;time datetime="2014-02-11T19:58:00-06:00"&gt; and parses the date out of it to be placed after the URL in a particular format.
 * *date\_compact*: When set to True and *prepend\_date* is also True, the format will be (d)d/(m)m/yy, in other words leading zeros are removed.
 * *date\_format*: If *date\_compact* is False and *prepend\_date* is True, the [strftime-compatible format](http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior) specified here will be used for the date.
 * *efficient\_hashtags*: When set to True, if a keyword is found in the page title then it will be hashtagged (so it appears in the first part of the tweet before the URL rather than appended after). This makes room for more keyword hashtags after the URL but if the title is too populated with keywords the tweet may appear as obnoxious hashtag spam. Use with care.
 * *site*: the URL of the root level domain as it appears in the sitemap; if a trailing slash is omitted it will be added in the main script
 * *site\_sitemap*: specifies what to append to *site* to reach the sitemap to be parsed
 * *site\_subdirs\_regex*: Form a non-empty dictionary where the keys are subdirectories off the root URL to gather articles from and values are regular expressions to use to match the full URL of an individual article (only specify the portion of regex to match what comes after the subdirectory; the rest is formed in the script).
 * *title\_split\_regex*: specifies a regular expression to use to extract the desired piece of the title for the first section of the tweet; if you want to use the entire title use "(.\*)"
 * *whitelist\_titles*: Form a (possibly empty) list where each entry is a title (**after** it has been split as set in *title\_split\_regex*) to match against when selecting the article; only matching titles are accepted.
 * *blacklist\_titles*: same as *whitelist\_titles* but if not empty any matches are never accepted
 * *changed\_titles*: Form a (possibly empty) dictionary where keys are titles to match against and values are custom titles to replace them with; use this if you'd like to reword things more appropriately for Twitter usage.

Once the configuration is set, rename the file to *post\_config.py*.

## (Optional) post\_runner.sh

This bash script is used to run *post.py* at random times within certain intervals in conjunction with a cron job (see the Implementation section). I prefer using a shell script to set the wait time rather than setting a wait time within the Python script itself because that will consume substantially more memory until the timer ends and it tweets; if you're running this on a server you should be as efficient as possible.

The configurable here is to adjust $intervalSeconds to the length of the window where a tweet may occur in seconds minus one. So if I want the bot to tweet once every 30 minutes I'll set this to 1799 which is one second less than 30 minutes. Subtracting one prevents (an unlikely) overlap.

# Implementation

You have a few options as to how to use this:

* Run it manually

        python post.py

* Run it as a fixed-interval cron job (in this example every 30 minutes)

        crontab -e
        */30 * * * * /usr/bin/env python /path/to/post.py

* Run *post\_runner.sh* as a fixed-interval cron job in order to run *post.py* at random times within fixed intervals (in this example, use 30 minute intervals)

        crontab -e
        */30 * * * * /path/to/post_runner.sh

My preference is with the third option. If peoples' Twitter habits are fairly predictable then you'll limit your potential audience by tweeting at the same times each day. Selecting the third choice causes *post\_runner.sh* to wait a random time within the interval length before running the Python script. Over a long time your tweets will be scattered randomly over the course of the day and your potential audience grows in diversity.

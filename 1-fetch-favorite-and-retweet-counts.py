"""Given a json dump of tweets, fetch the favorite and retweet counts.

This is not available in the original json dump of tweets, which contains
the tweets as they are published in realtime, i.e. before anyone has had
a chance to favorite or retweet them.

This scripts requires a secrets.py in the same dir which contains
your Twitter API secrets (APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET).
"""
import json
import time
from twython import Twython
from secrets import *

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

tweetids = []
fp = open('data/pyastro16-tweets.json')
for line in fp.readlines():
    if line.startswith('{'):
        try:
            tweet = json.loads(line)
            if 'retweeted_status' not in tweet:
                tweetids.append(tweet['id'])
        except Exception:
            pass

chunksize = 99  # We're not allowed to grab everything at once

out = open('data/pyastro16-twitter-stats.csv', 'w')
out.write('id,favorite_count,retweet_count,created_at\n')
for idx_start in range(0, len(tweetids) + chunksize, chunksize):
    print('Querying {} tweets from tweet #{}'.format(chunksize, idx_start))
    ids = ','.join([str(tid) for tid in tweetids[idx_start:idx_start + chunksize]])
    time.sleep(1)
    tweets = twitter.lookup_status(id=ids)
    for tweet in tweets:
        out.write('{id},{favorite_count},{retweet_count},{created_at}\n'.format(**tweet))
out.close()


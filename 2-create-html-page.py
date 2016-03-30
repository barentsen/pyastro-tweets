"""Creates the `twitter-archive.html` page for the #pyastro meeting websites.
"""
from jinja2 import Template
import pandas as pd

tweets = pd.read_csv('data/pyastro16-twitter-stats.csv', index_col='created_at', parse_dates=True).sort_index()
tweets['label'] = 'tweets-after'
for idx, day in enumerate([21, 22, 23, 24, 25]):
    tweets.loc['2016-03-{} 10'.format(day):'2016-03-{} 10'.format(day+1), 'label'] = 'tweets-day-{}'.format(idx+1)

mask_popular = (tweets['label'].notnull() &
                (
                    (tweets['favorite_count'] > 4) |
                    (tweets['retweet_count'] > 4)
                )
                )

template = Template(open('templates/pyastro-tweets-template.html').read())
with open('output/pyastro16-tweets.html', 'w') as out:
    out.write(template.render(tweets=tweets[mask_popular]))


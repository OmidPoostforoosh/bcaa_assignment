import feedparser #This package is for working with xml file
from sqlalchemy import create_engine
import pandas as pd
from creds import credentials

# Providing connection string from creds.py
postgres_str = credentials()
# Create the connection itself
cnx = create_engine(postgres_str)
print('database connection established')

def feed_article(n):
    # Step1: Download and parsing the latest paper xml file from arxiv.org
    NewsFeed = feedparser.parse("http://export.arxiv.org/rss/cs")
    posts = []
    # Step2: Loading all entries from the parsed xml content
    feeds = NewsFeed.entries
    # Step3: Extracting interested fields from entries
    for feed in feeds:
        posts.append((feed.title, feed.link, feed.description))
    # Step4: Converting to a pandas data frame
    df = pd.DataFrame(posts, columns=['title', 'link', 'description'])
    # Step5: Adding a new column for saving the the time of loading and feeding data
    df['created_date'] = pd.to_datetime('now')
    # Step6: Only 'n' papers will be appended to the table
    df = df.head(n)
    # Step7 : Create arxiv table or append data if exists
    df.to_sql('arxiv', con=cnx, if_exists='append')

# how many pages will be loaded in database
n = 10
# recurring frequency
print("Data PIPELINE started")
if __name__ == '__main__':
    feed_article(n)
print("Data PIPELINE finished")

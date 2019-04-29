import feedparser
import threading
import time
from sqlalchemy import create_engine
import pandas as pd
from creds import credentials


# Providing connection string from creds.py
postgres_str = credentials()
# Create the connection itself
cnx = create_engine(postgres_str)
print('database connection established')

class Schedule(threading.Thread):
    def __init__(self, interval, func, *args, **kwargs):
        threading.Thread.__init__(self)
        self.interval = interval  # seconds between calls
        self.func = func          # function to call
        self.args = args          # optional positional argument(s) for call
        self.kwargs = kwargs      # optional keyword argument(s) for call
        self.runable = True
    def run(self):
        while self.runable:
            self.func(*self.args, **self.kwargs)
            time.sleep(self.interval)
    def stop(self):
        self.runable = False

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
# Set the following parameter to indicate schedule interval
schedule_interval = 86400  # 86,400 seconds equals to 24 hours

# This means thread starts and stay active. Every [schedule_interval] seconds the function feed_article
# will be loading new feeds into database
thread = Schedule(schedule_interval, feed_article, n)
print("starting")
thread.start()
# The following commands commented out as we expect to run this app for ever
# If we want to terminate the job after a period of the time, we need to change the seconds in thread.join(X)
# and uncomment the following commands
# thread.join(20)  # executing thread for X seconds
# thread.stop()
# Job stops if thread.stop() became active or user pressed the ctrl + c button
print("Press ctrl + c to quit ...")
# The purpose for this Python script is:
# demonstrating my knowledge in AWS and it's resources such as Amazon Redshift and Simple Storage Service (S3)
# To run this script you need to provide :
# 1- AWS Redshift credentials (host name, username, password, port number and database name)
# 2- S3 Bucket access key and secret key

import feedparser #This package is for working with xml file
import boto3
import psycopg2
import pandas as pd

# Providing connection to the Amazon Redshift
conn = psycopg2.connect(
        host='<host name>',
        user='<user name>',
        port=5439,
        password='<password>',
        dbname='<database name>')
cur = conn.cursor()

# Providing connection to the Amazon S3 buckets
s3 = boto3.client(
        's3',
        aws_access_key_id='<aws_access_key_id>',
        aws_secret_access_key='<aws_secret_access_key>',
    )
filename = 'feed.csv'
object_name = 'python/feed.csv'
bucket_name = 'bcaa_assignment'

print('Connections are established')

# Assuming there is an schema called engineering_sandbox, this script will create "arxive" table in it
create_table_statement = 'create table if not exists engineering_sandbox.arxiv(' \
            'index integer, ' \
            'title text, ' \
            'link text, ' \
            'description text, ' \
            'created_date datetime);'
# AWS command for loading data from a file in the S3 bucket
# This command is so fast and highly recommended
s3_bucket = """
     COPY engineering_sandbox.arxiv FROM 's3://bcaa_assignment/python/feed.csv'
         access_key_id '<aws_access_key_id>'
         secret_access_key '<aws_secret_access_key>'
         delimiter as ','
         ignoreheader 1;"""

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
    # Step 7: Creating a csv file from data frame
    df.to_csv('feed.csv')
    # Step 8: Upload the created csv file into S3 bucket
    s3.upload_file(filename, bucket_name, object_name)
    # Step9: Creating the table if it is not already existed
    print(create_table_statement)
    cur.execute(create_table_statement)
    conn.commit()
    # Step10 : Copy data from csv file located in S3 bucket to Redshift table
    cur.execute(s3_bucket)
    conn.commit()


# how many pages will be loaded in database
n = 10
# recurring frequency
print("Data PIPELINE started")
if __name__ == '__main__':
    feed_article(n)
print("Data PIPELINE finished")














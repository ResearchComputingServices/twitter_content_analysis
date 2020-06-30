#
# Usage:
#   python <input_file> <output_file> <from_date> <to_date>
# Note:
#   <from_date> and <to_date> are optionally, and their format is YYYY-MM-DD
#
# Example:
#   python tweet_hydration.py wexit_tweets.csv wexit_tweets_output2.txt 2019-10-01 2019-10-22
#

import time
import sys
import tweepy
import json
import os
from tqdm import tqdm
from dateutil.parser import parse
import pytz

utc=pytz.UTC

CONSUMER_TOKEN = ''
CONSUMER_SECRET = ''

CHUNK_SIZE = 100 # Max limit allowed by twitter API at a time


def chunks(l, n):
    n = max(1, n)
    return [l[i:i+n] for i in range(0, len(l), n)]


def get_api_object():
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    api = tweepy.API(auth,
            wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True,
            # Handle error 503 (twitter service unavailable)
            retry_count=10,
            retry_delay=5,
            retry_errors=[104, 503])

    return api

def date_first_less_than_second(first, second):
    first_date = first.replace(tzinfo=utc)
    second_date = second.replace(tzinfo=utc)
    return first_date < second_date

def main(command_line_arguments):
    file_name = command_line_arguments.get("file_name")
    output_file = command_line_arguments.get("output_file")
    from_date = command_line_arguments.get("from_date")
    to_date = command_line_arguments.get("to_date")
    with open(file_name, 'r', encoding="utf-8") as f:
        try:
            lines = [l.strip() for l in f.readlines()]
            tweet_chunks = chunks(lines, CHUNK_SIZE)
        except Exception as e:
            print('an exception occured:'.format(str(e)))

    api = get_api_object()

    with open(output_file, 'w', encoding="utf-8") as f:
        for chunk in tqdm(tweet_chunks):
            while True:
                try:
                    tweets = api.statuses_lookup(id_=chunk, tweet_mode='extended', include_entities=True, map_=True)
                    for tweet in [t._json for t in tweets]:
                        created_at = tweet.get('created_at')
                        if created_at == None:
                            continue
                        dt = parse(created_at)
                        if from_date != None:
                            from_date_dt = parse(from_date)
                            if date_first_less_than_second(dt, from_date_dt):
                                continue
                        if to_date != None:
                            to_date_dt = parse(to_date)
                            if date_first_less_than_second(to_date_dt, dt):
                                continue
                        print(dt.date())
                        print("created_at:" + created_at + "\n")
                        f.write(str(tweet) + '\n\n\n')
                    break
                except Exception as e:
                    print('an exception occured, retrying in 2s: {:s}'.format(str(e)))
                    time.sleep(2)

if __name__ == '__main__':
    print(sys.argv)
    argc = len(sys.argv)
    command_line_arguments = {
        "file_name": sys.argv[1],
        "output_file": sys.argv[2]
    }
    if argc >= 4:
        command_line_arguments["from_date"] = sys.argv[3]
    if argc >= 5:
        command_line_arguments["to_date"] = sys.argv[4]
    main(command_line_arguments)


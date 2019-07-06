import json
import tweepy
from os import path
from sys import exit

def get_ids(start=None):
    ids = [l.split(',')[0] for l in open('all_data_tweet_id.txt', 'r').readlines()[1:]]
    if start is not None:
        try:
            id_ix = ids.index(start)
            return ids[id_ix:]
        except Exception as e:
            print(f'Start id {id} not found.')
            exit(1)
    else:
        return ids


if __name__ == '__main__':
    keys = json.load(open('.keys', 'r'))
    consumer_token, consumer_secret = keys['API key'], keys['API secret key']
    auth = tweepy.AppAuthHandler(consumer_token, consumer_secret)
    api = tweepy.API(auth)

    try:
        with open('last_tweet.txt', 'r') as id_file:
            start = id_file.read()
    except Exception as e:
        start = None

    try:
        with open('tweets_id_text.json', 'r+') as infile:
            tweets = json.load(infile)
    except Exception as e:
        tweets = dict()

    ids = get_ids(start)
    for id in ids:
        try:
            tweet = api.get_status(id)
            print(tweet.text)
            tweets[id] = tweet.text
        except Exception as e:
            print(e.args[0][0]['message'])
            if e.args[0][0]['code'] == 88:
                print(f'Limit exceeded at id: {id}')
                with open('last_tweet.txt', 'w') as id_file:
                    id_file.write(id)
                break

    with open('tweets_id_text.json', 'w') as outfile:
        json.dump(tweets, outfile)

    if id == ids[-1]:
        exit(112)  # exit code 112 means that the dataset has been completely hydrated
    else:
        exit(111)  # exit code 111 means that the hydrator should run again to complete the hydration

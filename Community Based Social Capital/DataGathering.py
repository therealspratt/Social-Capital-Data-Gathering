from twython import Twython
from twython import TwythonError
import time
import TwitterDataModel

con_key = "mUv5JGLV75o5rEyCRFlNjb2sO"
acc_token = "AAAAAAAAAAAAAAAAAAAAAOCFgQAAAAAA0RESD1aJyAUWCGDmLn6lAhVeOlo%3DJMgMwVs74WNuoTdkC91Z2gIGyQPE9mmUR7fflrIamrmmXyA8As"

class TwitterCrawlerMention:

    users_expanded=[]

    def __init__(self, file_name):
        self.output_file=open(file_name, "w")
        self.twitter_connection=Twython(con_key, access_token=acc_token)

    def start_crawl(self, search_term, node_limit):
        data={}
        while True:
            try:
                data = self.twitter_connection.search(q=search_term, lang="en", result_type="recent", count=100)
                break
            except TwythonError as e:
                print e
                if str(429) in e.msg:
                    time.sleep(900)
                    self.twitter_connection = Twython(con_key, access_token=acc_token)
        for tweet in data:
            users_mentioned=tweet["entities"]["user_mentions"]
            for mentioned_user in users_mentioned:
                if mentioned_user not in self.users_expanded:
                    self.users_expanded.append(mentioned_user)
                while True:
                    try:
                        results = self.twitter_connection.get_user_timeline(screen_name=mentioned_user, count=100, include_rts=False)
                        break
                    except TwythonError as e:
                        print e
                        if str(429) in e.msg:
                            time.sleep(900)
                            self.twitter_connection = Twython(con_key, access_token=acc_token)
                        else:
                            return

class TwitterCrawlerFollow:

    users_expanded=[]

    def __init__(self, file_name):
        self.output_file=open(file_name, "w")
        self.twitter_connection=Twython(con_key, access_token=acc_token)

    def start_crawl(self, search_term, node_limit):
        data={}
        while True:
            try:
                data = self.twitter_connection.search(q=search_term, lang="en", result_type="recent", count=1)
                break
            except TwythonError as e:
                print e
                if str(429) in e.msg:
                    time.sleep(900)
                    self.twitter_connection = Twython(con_key, access_token=acc_token)

    def expand_user(self, user, depth, max_depth):
        friends=self.twitter_connection.get_friends_list(user_id=user, count=200)

        for friend in friends:
            if depth<max_depth:
                if user not in self.users_expanded:
                    self.users_expanded.append(friend)
                    self.expand_user(friend, depth+1, max_depth)
            else:
                return
from twython import Twython
from twython import TwythonStreamer
from TwitterDataModel import Node, Edge, Graph

class CollectorStream(TwythonStreamer):
    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret, limit, output):
        TwythonStreamer.__init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret)
        self.limit=limit

    def set_limit(self, num):
        self.limit=num

    def set_timeout(self, time):
        self.timeout=time

    def on_success(self, data):
        if "text" in data and data["text"][0:2] != "RT" and "retweeted_status" not in data and data["lang"] == "en":
            text = ((((data["text"].replace("\n"," ")).replace(","," ")).replace("\r"," ")).replace("\""," ")).lower()
            self.output_file.write(text.encode("utf-8")+",")
            self.output_file.write(data["user"]["screen_name"].encode("utf-8")+",")
            self.output_file.write(str(data["user"]["friends_count"])+",")
            self.output_file.write(str(data["user"]["followers_count"])+",")
            self.output_file.write(str(data["user"]["statuses_count"])+",")
            self.output_file.write(str(data["user"]["favourites_count"])+",")
            self.output_file.write(str(data["user"]["utc_offset"])+",")
            self.output_file.write(data["id_str"]+",")
            self.output_file.write(data["created_at"].encode("utf-8")+",")
            self.output_file.write(str(data["favorite_count"])+",")
            self.output_file.write(str(data["retweet_count"])+",")
            self.output_file.write(str(len(data["entities"]["hashtags"]))+",")
            self.output_file.write((str(len(data["entities"]["user_mentions"])))+",")
            self.output_file.write(str(1)+"\n")
            if(self.i==self.limit-1):
                exit()
            print self.i
            self.i+=1

class TwitterCrawlerFollow:

    def __init__(self):
        consumer_key = "mUv5JGLV75o5rEyCRFlNjb2sO"
        acc_token = "AAAAAAAAAAAAAAAAAAAAAOCFgQAAAAAA0RESD1aJyAUWCGDmLn6lAhVeOlo%3DJMgMwVs74WNuoTdkC91Z2gIGyQPE9mmUR7fflrIamrmmXyA8As"
        self.twit = Twython(consumer_key, access_token=acc_token)

    def start_crawl(self, starting_point):
        graph=Graph()
        starter_node=Node(starting_point)
        graph.add_node(starter_node)
        friend_ids=self.twit.get_friends_ids(screen_name=starting_point)["ids"]
        for friend in friend_ids:
            graph.add_edge(starter_node, Edge(Node(friend)))



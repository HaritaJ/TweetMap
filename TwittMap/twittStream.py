#Import the necessary methods from tweepy library
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from geopy.geocoders import Nominatim
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from textwrap import TextWrapper
import cgi
import sys



#Variables that contains the user credentials to access Twitter API
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""


#This is a basic listener that just prints received tweets to stdout.
class TListener(StreamListener):

    def on_data(self, data):
        try:
            status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')
            twitt_data = json.loads(data)
            print data
            if ('coordinates' in twitt_data.keys()):
                if (twitt_data['coordinates'] is not None):
                    es.create(index="twitter-py",
                        doc_type="twitter_twp",
                        body=twitt_data
                      )
        except Exception, e:
            pass



        return True

    def on_error(self, status):
        print status
        exit()


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    host = 'search-twittmap-hehinisyr7ifk7ql5jwlo5pwom.us-west-2.es.amazonaws.com'
    awsauth = AWS4Auth('', '', 'us-west-2', 'es')



    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )


    print(es.info())
    l = TListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    try:
        stream.filter(locations=[-180, -90, 180, 90],
                      track=['Trump', 'modi', 'holi', 'love', 'first', 'photo', 'lunch', 'today', 'sunday', 'trump',
                             'Donald'])
    except Exception, e:
        pass

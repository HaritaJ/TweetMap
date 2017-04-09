from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.http import *
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
access_token = "1194341250-VVXcuVmt0naHfNvCFL7kPYINHF0XbQuWebYm7qN"
access_token_secret = "pDDZDUFBYErje7RLnFYYuFfvdl9f5KwKHeHRK3BxngTwd"
consumer_key = "6R8WSg5LtlyIdlT08zdpjXU1S"
consumer_secret = "arA8mSAdUDs4XosjOjdC7YPI4VTpHx7aCFUFbcK2xH1ZML3nIo"

host = 'search-twittmap-hehinisyr7ifk7ql5jwlo5pwom.us-west-2.es.amazonaws.com'
awsauth = AWS4Auth('AKIAISXJPZTWFN6HKXSA', 'h6joFSTDwj7QTTSnLVgH3vyjJckqEpTiWuUdd9sb', 'us-west-2', 'es')

es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )



# Create your views here.
class IndexView(generic.ListView):
    """
    Creates the view for the index page of the question
    """
    template_name = 'TwittMap/index.html'

    def get_queryset(self):
        return True


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        searchStr=request.POST['searchString']
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        res = es.search(index="twitter-py", size = 10000, body={"query": {"match":{"text": "%"+searchStr+"%"}}},)
        coordinates = {}
        print("Got %d Hits:" % res['hits']['total'])
        print res.keys()
        for hit in res['hits']['hits']:
            print(hit["_source"].keys())
            if ('coordinates' in hit["_source"].keys()):
                if (hit["_source"]['coordinates'] is not None):
                    lat = hit["_source"]['coordinates']['coordinates'][0]
                    lon = hit["_source"]['coordinates']['coordinates'][1]
                    coordinates[lat] = lon

    return HttpResponse(json.dumps(coordinates))

def geo_user(request):
    if request.method == 'POST':
        searchStr=request.POST['searchString']
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        res = es.search(index="twitter-py", size = 10000, body={"query": {"match":{"text": "%"+searchStr+"%"}},"filter":{"geo_distance": {"100": str(distance) + "km","location": {"lat": lat,"lon": lng}}}})
        coordinates = {}
        print("Got %d Hits:" % res['hits']['total'])
        print res.keys()
        for hit in res['hits']['hits']:
            print(hit["_source"].keys())
            if ('coordinates' in hit["_source"].keys()):
                if (hit["_source"]['coordinates'] is not None):
                    lat = hit["_source"]['coordinates']['coordinates'][0]
                    lon = hit["_source"]['coordinates']['coordinates'][1]
                    coordinates[lat] = lon

    return HttpResponse(json.dumps(coordinates))


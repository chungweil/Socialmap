import urllib, oauth, hidden, json, time, os, pprint
from datetime import datetime



class TwitterSearch(object):

    def augment(self, url, parameters) :
        '''
        Combine the "oauth keys" and the "parameters"
        with the url of a twitter API
        '''

        # My twitter oauth keys are stored in the hidden.py file
        secrets = hidden.oauth()

        consumer = oauth.OAuthConsumer(secrets['consumer_key'], secrets['consumer_secret'])
        token = oauth.OAuthToken(secrets['token_key'],secrets['token_secret'])

        oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer,
                                                                   token=token,
                                                                   http_method='GET',
                                                                   http_url=url,
                                                                   parameters=parameters)

        oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), consumer, token)

        return oauth_request.to_url()

    def fetch_json(self, query, count=100) :

        base_url = 'https://api.twitter.com/1.1/search/tweets.json?'
        params = {'q'    : query,
                  'count': count}
                  # 'geocode': '40.7128 -74.0059 100mi'


        url = self.augment(base_url, params)
        print '* Calling '+ url + '\n'

        connection = urllib.urlopen(url)
        data = connection.read()
        headers = connection.info().dict

        fname = str(datetime.utcnow()).replace(':', '-').split('.')[:-1]
        fname = ''.join(fname) + ' query={}.json'.format(query)
        fh = open(fname , 'w')
        fh.write(data)
        print 'json file stored as ' + fname + '\n'

    def autoloop(self, query_list):

        while True:
            current_min = str(datetime.now().time()).split(':')[1]

            # If current minute is a multiple of 10, i.e., every 10 minutes
            if int(current_min) % 10 == 0:
                for query in query_list:
                    self.fetch_json(query)
                    time.sleep(540)

            time.sleep(1)



class Extractor(object):

    def json_generator(self):

        # os.walk() is a generator function
        # which yields a tuple (path, dirs, files) for each iteration

        # For each iteration os.walk() gets a folder as a path
        # and also gets a list of dirs (subfolders), and a list of files

        for path, dirs, files in os.walk('.'): # This is how to loop as a tuple for each iteration

            if not path == '.':
                continue

            for filename in files:

                if not filename[-5:] == '.json':
                    continue

                fullname = os.path.join(path, filename)
                str_data = open(fullname).read()

                yield json.loads(str_data)






if __name__ == '__main__':

    if True:
        twitter_search = TwitterSearch()
        twitter_search.autoloop(query_list=['#nodapl'])

    if False:
        print 'c'

        EXT = Extractor()

        str_output = ''

        for scrape in EXT.json_generator():
            for tweet in scrape['statuses']:

                str_output = str_output + tweet['text'].encode("utf-8") + '\n'

                if not tweet['place'] == None:
                    print tweet['place']['name']

                if not tweet['coordinates'] == None:
                    print tweet['coordinates']['coordinates']

        with open('nodapl_tweet_texts.txt', 'w') as fh:
            fh.write(str_output)






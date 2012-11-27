import copy
import requests
from tout_collection import ToutCollection

class ToutUser(object):
    def __init__(self, url_settings=None, access_token=None, uid=None, username=None, fullname=None, friendly_name=None, bio=None, location=None, verified=False, touts_count=0, followers_count=0, friends_count=0, following=False, followed_by=False):
        self.uid = uid
        self.username = username
        self.fullname = fullname
        self.friendly_name = friendly_name
        self.bio = bio
        self.location = location
        self.verified = verified
        self.touts_count = touts_count
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.following = following
        self.followed_by = followed_by

        self._touts_collection = None
        self._access_token = access_token
        self._headers = {'Authorization': 'Bearer %s' % access_token}

        if url_settings is not None:
            self._url_settings = url_settings
        else:
            self._url_settings = {'protocol': 'https', 'base_url': 'api.tout.com'}

        self._immutable_fields = ['verified', 'touts_count', 'followers_count', 'friends_count', 'following', 'followed_by']
    
    def __str__(self):
        return "@%s" % self.uid          

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, name):
        if name == 'touts':
            if self._touts_collection == None:
                self._touts_collection = self.get_touts()

            return self._touts_collection
        

    def __eq__(self, other):
        try:
            other.uid
            return self.uid == other.uid
        except AttributeError:
            return False
        
    def construct_url(self, api_method):
        url = "%s://%s/%s" % (self._url_settings['protocol'], self._url_settings['base_url'], api_method)

        return url

    def follow(self):
        url = self.construct_url('api/v1/users/%s/follows' % self.uid)

        r = requests.post(url, headers=self._headers)
        if r.status_code == 200:
            print 'Now following %s' % self.uid
            self.get_followers()
        else:
            print 'An error occured'

    def unfollow(self):
        url = self.construct_url('api/v1/users/%s/follows' % self.uid)

        r = requests.delete(url, headers=self._headers)
        if r.status_code == 200:
            print 'No longer following %s' % self.uid
            self.get_followers() 
        else:
            print 'An error occured'

    def get_touts(self):
        url = self.construct_url('api/v1/users/%s/touts' % self.uid)

        self.touts._collection = ToutCollection(base_url=url, access_token=self._access_token, coll_type='touts')

    def get_followers(self):
        url = self.construct_url('api/v1/users/%s/followers' % self.uid)
        
        self.followers = ToutCollection(base_url=url, access_token=self._access_token, coll_type='users')

    def get_following(self):
        url = self.construct_url('api/v1/users/%s/following' % self.uid)
        
        self.following = ToutCollection(base_url=url, access_token=self._access_token, coll_type='users')

    def get_likes(self):
        url = self.construct_url('api/v1/users/%s/likes' % self.uid)

        self.likes = ToutCollection(base_url=url, access_token=self._access_token, coll_type='touts')

    def get_participating_convos(self):
        pass

    def to_json(self):
        import simplejson as json
        
        user_info = copy.deepcopy(self.__dict__)

        del user_info['_access_token']
        del user_info['_headers']
        del user_info['_immutable_fields']
        del user_info['_url_settings']

        user = {'user': user_info} 
        return json.dumps(user)

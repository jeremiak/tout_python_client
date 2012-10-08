import requests
import simplejson as json

from tout_collection import ToutCollection
from tout_user import ToutUser
from tout_me import ToutMe
from tout_tout import Tout

class ToutClient(object):
    def __init__(self, access_token=None):
        self.protocol = 'https'
        self.base_url = 'api.tout.com'
        if access_token is not None:
            self.access_token = access_token
            self.headers = {'Authorization': 'Bearer %s' % self.access_token}
        else:
            print "API is worthless without an access_token. Set yours on the ToutAPIClient object with ToutAPIClient.access_token = XX"
    
    def get_me(self):
        url = "%s://%s/%s" % (self.protocol, self.base_url, 'api/v1/me')
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            u = r.json['user']
            me = ToutMe(access_token=self.access_token, uid=u['uid'], username=u['username'], fullname=u['fullname'], friendly_name=u['friendly_name'], bio=u['bio'], location=u['location'], verified=u['verified'], touts_count=u['touts_count'], followers_count=u['followers_count'], friends_count=u['friends_count'], following=u['following'], followed_by=u['followed_by'])
            
            return me
        else:
            return "An error occured"

    def get_user(self, uid='teamtout'):
        url = "%s://%s/%s" % (self.protocol, self.base_url, 'api/v1/users/%s' % uid)
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            u = r.json['user']
            user = ToutUser(access_token=self.access_token, uid=u['uid'], username=u['username'], fullname=u['fullname'], friendly_name=u['friendly_name'], bio=u['bio'], location=u['location'], verified=u['verified'], touts_count=u['touts_count'], followers_count=u['followers_count'], friends_count=u['friends_count'], following=u['following'], followed_by=u['followed_by'])
            
            return user
        else:
            return "An error occured"

    def get_tout(self, uid='7SuIRvWfU3K'):
        url = "%s://%s/%s" % (self.protocol, self.base_url, 'api/v1/touts/%s' % uid)
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            data = r.json['tout']
            u = data['user']
            user = ToutUser(uid=u['uid'], access_token=self.access_token, username=u['username'], fullname=u['fullname'], friendly_name=u['friendly_name'], bio=u['bio'], location=u['location'], verified=u['verified'], touts_count=u['touts_count'], followers_count=u['followers_count'], friends_count=u['friends_count'], following=u['following'], followed_by=u['followed_by'])
            tout = Tout(uid=data['uid'], access_token=self.access_token, text=data['text'], privacy=data['privacy'], recorded_at=data['recorded_at'], likes_count=data['likes_count'], replies_count=data['replies_count'], retouts_count=data['retouts_count'], user=user) 
            
            return tout

    def get_convo_touts(self, convo_id=None):
        if convo_id is not None:
            url = "%s://%s/%s" % (self.protocol, self.base_url, 'api/v1/conversations/%s/touts' % convo_id)
            r = requests.get(url, headers=self.headers)

            touts = ToutCollection(base_url=url, access_token=self.access_token)

            return touts

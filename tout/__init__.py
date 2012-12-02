import requests
import simplejson as json

from tout_collection import ToutCollection
from tout_user import ToutUser
from tout_me import ToutMe
from tout_tout import Tout

class ToutClient(object):
    """
    Main interaction point for interacting with the Tout API. Because the API requires authentication
    for all of the calls make sure to pass in either a client_id & client_secret pair or an access_token
    """
    def __init__(self, client_id=None, client_secret=None, access_token=None):
        self.protocol = 'https'
        self.base_url = 'api.tout.com'
        if access_token is not None:
            self.access_token = access_token
            self.token_type = 'user_credentials'
            self.headers = {'Authorization': 'Bearer %s' % self.access_token}
        elif client_id is not None and client_secret is not None and access_token is None:
            auth_url = 'www.tout.com/oauth/token'
            params = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials'}
            r = requests.post('%s://%s' % (self.protocol, auth_url), params=params)
            if r.status_code == 200:
                token = r.json['access_token']
                self.access_token = token
                self.token_type = 'client_credentials'
                self.headers = {'Authorization': 'Bearer %s' % self.access_token}
        else:
            print "API is worthless without an access_token. Set yours on the ToutAPIClient object with ToutAPIClient.access_token = XX"
    
    def get_me(self):
        """
        Return the authenticated user for the access_token.
        """
        if self.token_type == 'user_credentials':
            url = "%s://%s/%s" % (self.protocol, self.base_url, 'api/v1/me')
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                u = r.json['user']
                me = ToutMe(access_token=self.access_token, uid=u['uid'], username=u['username'], fullname=u['fullname'], friendly_name=u['friendly_name'], bio=u['bio'], location=u['location'], verified=u['verified'], touts_count=u['touts_count'], followers_count=u['followers_count'], friends_count=u['friends_count'], following=u['following'], followed_by=u['followed_by'])
                
                return me
            else:
                return "An error occured"
        else:
            return "There is no authenticated user context for this token"

    def return_user(self, u):
        """
        Return an instance of the ToutUser class; represents a Tout user
        """
        user = ToutUser(access_token=self.access_token, uid=u['uid'], username=u['username'], fullname=u['fullname'], friendly_name=u['friendly_name'], bio=u['bio'], location=u['location'], verified=u['verified'], touts_count=u['touts_count'], followers_count=u['followers_count'], friends_count=u['friends_count'], following=u.get('following', False), followed_by=u.get('followed_by', False))
        
        return user

    def get_user(self, uid='teamtout'):
        """
        Request the user by making an API call
        """
        url = "%s://%s/%s" % (self.protocol, self.base_url, 'api/v1/users/%s' % uid)
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            u = r.json['user']
            user = self.return_user(u)
            return user
        else:
            return "An error occured"

    def get_tout(self, uid='7SuIRvWfU3K'):
        """
        Return an instance of the Tout class; represents a Tout video
        """
        url = "%s://%s/%s" % (self.protocol, self.base_url, 'api/v1/touts/%s' % uid)
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            data = r.json['tout']
            u = data['user']
            user = self.return_user(u)            
            tout = Tout(uid=data['uid'], access_token=self.access_token, text=data['text'], privacy=data['privacy'], recorded_at=data['recorded_at'], likes_count=data['likes_count'], replies_count=data['replies_count'], retouts_count=data['retouts_count'], user=user) 
            
            return tout

    def get_stream(self, uid='c6i24c'):
        """
        Given a stream uid returns an instance of the ToutCollection class; represents a stream
        """
        url = "%s://%s/%s" % (self.protocol, self.base_url, 'api/v1/streams/%s/touts' % uid)

        stream = ToutCollection(base_url=url, access_token=self.access_token)

        return stream

    def get_stream_from_widget(self, uid='sim2ov'):
        """
        Given a widget uid returns an instance of the ToutCollection class; represents the widget's underlying stream
        """ 
        url = 'http://%s/%s' % (self.base_url, '/widgets/%s.json' % uid)
        r = requests.get(url)

        if r.status_code == 200:
            s_uid = r.json['widget']['stream_uid']
            stream = self.get_stream(uid=s_uid)

            return stream

    def get_latest_touts(self):
        """
        Return an instance of the ToutCollection class; represents the latest Touts
        """
        url = "%s://%s/%s" % (self.protocol, self.base_url, 'api/v1/latest')

        latest = ToutCollection(base_url=url, access_token=self.access_token)

        return latest

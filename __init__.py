import httplib, mimetypes, types, requests
import simplejson as json

from tout_collection import ToutCollection
from tout_user import ToutUser
from tout_me import ToutMe
from tout_tout import Tout

from utils import *

class ToutClient(object):
    def __init__(self, access_token=None):
        self.protocol = 'https'
        self.base_url = 'api.tout.com'
        if access_token is not None:
            self.access_token = access_token
            self.headers = {'Authorization': 'Bearer %s' % self.access_token}
        else:
            print "API is worthless without an access_token. Set yours on the ToutAPIClient object with ToutAPIClient.access_token = XX"

    def post_tout(self, tout_file=None):
        if self.access_token is None:
            return "Need a token"
        else:
            if type(tout_file) is types.FileType:
                content_type, body = encode_multipart_formdata([('access_token', self.access_token)], [('tout[data]', tout_file.name, tout_file.read())])
                tout_file.close()

                h = httplib.HTTPSConnection(self.base_url)
                headers = {
                    'User-Agent': 'tout-python-client',
                    'Content-Type': content_type
                    }
                h.request('POST', '/api/v1/touts.json', body, headers)
                res = h.getresponse()
                
                if res.status == 202:
                    data = json.loads(res.read())['tout']
                    u = data['user']
                    user = ToutUser(uid=u['uid'], username=u['username'], fullname=u['fullname'], friendly_name=u['friendly_name'], bio=u['bio'], location=u['location'], verified=u['verified'], touts_count=u['touts_count'], followers_count=u['followers_count'], friends_count=u['friends_count'], following=u['following'], followed_by=u['followed_by'])
                    tout = Tout(uid=data['uid'], text=data['text'], privacy=data['privacy'], recorded_at=data['recorded_at'], likes_count=data['likes_count'], replies_count=data['replies_count'], retouts_count=data['retouts_count'], user=user)
                    
                    return tout
            else:
                return "Please pass in a Tout video file"

    def get_me(self):
        url = "%s://%s/%s" % (self.protocol, self.base_url, 'api/v1/me')
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            u = r.json['user']
            me = ToutMe(access_token=self.access_token, uid=u['uid'], username=u['username'], fullname=u['fullname'], friendly_name=u['friendly_name'], bio=u['bio'], location=u['location'], verified=u['verified'], touts_count=u['touts_count'], followers_count=u['followers_count'], friends_count=u['friends_count'], following=u['following'], followed_by=u['followed_by'])
            
            return me
        else:
            return "An error occured"

    def get_convo_touts(self, convo_id=None):
        if convo_id is not None:
            url = "%s://%s/%s" % (self.protocol, self.base_url, 'api/v1/conversations/%s/touts' % convo_id)
            r = requests.get(url, headers=self.headers)

            touts = ToutCollection(base_url=url, access_token=self.access_token)

            return touts

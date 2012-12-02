from tout_collection import ToutCollection  
from tout_tout import Tout
from tout_user import ToutUser

from types import FileType
from utils import *

import simplejson as json

class ToutMe(ToutUser):
    def change_attribute(self, attribute_key, new_value):
        if self.__dict__.has_key(attribute_key):
            if attribute_key not in self.immutable_fields: 
                self.__setattr__(attribute_key, new_value)
            else:
                return "%s is not a mutable attribute" % attribute_key
        else:
            return "%s does not have attribute %s" % (self, attribute_key)
    
    def post_tout(self, tout_file=None, tout_text=None, tout_privacy='public'):
        """
        Only way to add Touts to the tout platform. Pass in a FileType and this will handle the multipart/form POST
        """
        if self._access_token is None:
            return "Need a token"
        else:
            if type(tout_file) is FileType:
                content_type, body = encode_multipart_formdata([('access_token', self._access_token)], [('tout[data]', tout_file.name, tout_file.read())])
                tout_file.close()

                h = httplib.HTTPSConnection(self._url_settings['base_url'])
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

    def get_updates(self):
        """
        Return an instance of the ToutCollection class; represents the authenticated user's feed of Tout videos from the other users he/she follows
        """
        url = self.construct_url('api/v1/users/%s/updates' % self.uid)

        self.updates = ToutCollection(base_url=url, access_token=self._access_token, coll_type='touts')

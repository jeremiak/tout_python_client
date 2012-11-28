from dateutil.parser import parse
import requests

class Tout(object):
    def __init__(self, url_settings=None, access_token=None, uid=None, text=None, privacy=None, recorded_at=None, created_at=None, likes_count=0, replies_count=0, retouts_count=0, liked=False, image=None, video=None, retouted_tout=None, replied_to_tout=None, user=None, conversation=None):
        self.uid = uid
        self.text = text
        self.privacy = privacy
        self.recorded_at = parse(recorded_at) if recorded_at != None else None
        self.created_at = parse(created_at) if created_at != None else None
        self.likes_count = likes_count
        self.replies_count = replies_count
        self.liked = liked
        self.image = image
        self.video = video
        self.retouted_tout = retouted_tout
        self.replied_to_tout = replied_to_tout
        self.user = user
        self.conversation = conversation

        if url_settings is not None:
            self._url_settings = url_settings
        else:
            self._url_settings = {'protocol': 'https', 'base_url': 'api.tout.com'}

        self._changed = False
        self._headers = {'Authorization': 'Bearer %s' % access_token}
    
    def __repr__(self):
        return "Tout %s" % self.uid

    def generate_url(self, **kwargs):
        endpoint = kwargs.get('endpoint', '')

        url = '%s://%s/api/v1/touts/%s/%s' % (self._url_settings['protocol'], self._url_settings['base_url'], self.uid, endpoint)

        return url

    def like(self):
        url = self.generate_url(endpoint='likes')

        r = requests.post(url, headers=self._headers)

        print 'Tout %s liked' % self.uid
        
        return r

    def unlike(self):
        url = self.generate_url(endpoint='likes')

        r = requests.delete(url, headers=self._headers)

        print 'Tout %s unliked' % self.uid

        return r

    def update_tout(self, text=None, privacy=None):
        if text is None and privacy is None:
            print "Update either text or privacy of this Tout"
        else:
            if text is not None:
                self.text = text
            elif privacy is not None:
                self.privacy = privacy

            self._changed = True

    def save(self):
        if self._changed is False:
            return
        else:
            protocol = self._url_settings['protocol']
            base_url = self._url_settings['base_url']
            
            params = {'tout[text]': self.text} 
            
            r = requests.put("%s://%s/api/v1/touts/%s" % (protocol, base_url, self.uid), headers=self._headers, params=params)

            if r.status_code == 200:
                print "Tout successfully saved"
                self._changed = False
            elif r.status_code == 401:
                print "You are not able to save this Tout because it does not belong to you"

    def delete(self, confirm=False):
        if confirm == False:
            print "Please confirm that you would like to delete this Tout\nUse delete(confirm=True) to do so"
        else:
            protocol = self._url_settings['protocol']
            base_url = self._url_settings['base_url']
            
            r = requests.delete("%s://%s/api/v1/touts/%s" % (protocol, base_url, self.uid), headers=self._headers)
            
            if r.status_code == 200:
                print "Tout successfully deleted"
                self.__dict__ = {}
            elif r.status_code == 403:
                print "You are not able to delete this Tout because it does not belong to you"


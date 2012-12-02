import requests
import math

class ToutCollection(object):
    def __init__(self, base_url=None, access_token=None, current_page=1, per_page=50, total_entries=None, coll_type='touts'):
        self._pagination = {
                'current_page': current_page,
                'per_page': per_page,
                'total_entries': total_entries,
                'total_pages': 0
                }
        self._base_url = base_url
        self._headers = {'Authorization': 'Bearer %s' % access_token}
        self._type = coll_type
        
        if current_page == 1:
            self.exact_page(page=1)
        else:
            self.exact_page(page=current_page)

    def __repr__(self):
        cur_page = self._pagination['current_page']
        tot_pages = self._pagination['total_pages']
        tot_entries = self._pagination['total_entries']
        repr_string = "Collection of %s - page %d of %d" % (self._type.title(), cur_page, tot_pages)
        repr_string += "\nThere are a total of %d items in this collection" % tot_entries
        repr_string += '\nUse prev_page() and next_page() methods to paginate'

        return repr_string

    def set_collection(self, url):
        print url
        
        r = requests.get(url, headers=self._headers)
        
        if r.status_code == 200:
            keys = r.json.keys()
            
            total_entries = r.json['pagination']['total_entries'] 
            self._pagination['total_entries'] = total_entries
            self._pagination['total_pages'] = int(math.ceil(total_entries / (self._pagination['per_page'] * 1.00)))
            keys.remove('pagination')
            
            collection = []
            
            print len(r.json[keys[0]])

            for item in r.json[keys[0]]:
                from tout_user import ToutUser
                token = self._headers['Authorization'].split(' ')[1]
                if self._type == 'touts':
                    from tout_tout import Tout

                    data = item['tout']
                    u = data['user']
                    user = ToutUser(uid=u['uid'], access_token=token, username=u['username'], fullname=u['fullname'], friendly_name=u['friendly_name'], bio=u['bio'], location=u['location'], verified=u['verified'], touts_count=u['touts_count'], followers_count=u['followers_count'], friends_count=u['friends_count'], following=u['following'], followed_by=u['followed_by'])
                    tout = Tout(uid=data['uid'], access_token=token, text=data['text'], privacy=data['privacy'], recorded_at=data['recorded_at'], likes_count=data['likes_count'], replies_count=data['replies_count'], retouts_count=data['retouts_count'], image=data['image'], video=data['video'], user=user) 
                
                    collection.append(tout)
                else:
                    u = item['user']
                    user = ToutUser(uid=u['uid'], access_token=token, username=u['username'], fullname=u['fullname'], friendly_name=u['friendly_name'], bio=u['bio'], location=u['location'], verified=u['verified'], touts_count=u['touts_count'], followers_count=u['followers_count'], friends_count=u['friends_count'], following=u['following'], followed_by=u['followed_by'])

                    collection.append(user)

            self.collection = collection

    def different_page(self, difference=0):
        url = '%s?per_page=%d&page=%d' % (self._base_url, self._pagination['per_page'], (self._pagination['current_page'] + difference))
        self.set_collection(url)        

        self._pagination['current_page'] += difference

    def next_page(self):
        """
        Set the collection attribute on this object to the data of the next page of Tout results
        """
        if (self._pagination['current_page'] < self._pagination['total_pages']):
            self.different_page(difference=1)
        else:
            print "Reached the end of the collection"

    def prev_page(self):
        """
        Set the collection attribute on this object to the data of the previous page of Tout results
        """
        if (self._pagination['current_page'] > 1):
            self.different_page(difference=-1)
        else:
            print "Reached the beginning of the collection"
        

    def exact_page(self, page=1):
        """
        Set the collection attribute on this object to the data of an exact page of Tout results
        """
        url = '%s?per_page=%d&page=%d' % (self._base_url, self._pagination['per_page'], page)

        self.set_collection(url)

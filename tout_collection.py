from tout_tout import Tout

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
        repr_string = "Collection of %s - page %d of %d" % (self._type.title(), cur_page, tot_pages)
        repr_string += '\nUse prev_page() and next_page() methods to paginate'

        return repr_string

    def set_collection(self, url):
        r = requests.get(url, headers=self._headers)
        
        if r.status_code == 200:
            keys = r.json.keys()
            
            total_entries = r.json['pagination']['total_entries'] 
            self._pagination['total_entries'] = total_entries
            self._pagination['total_pages'] = int(math.ceil(total_entries / (self._pagination['per_page'] * 1.00)))
            keys.remove('pagination')
            
            collection = []
            
            for item in r.json[keys[0]]:
                if self._type = 'touts':
                    data = item['tout']
                    user = data['user']
                    token = self._headers['Authorization'].split(' ')[1]
                    tout = Tout(uid=data['uid'], access_token=token, text=data['text'], privacy=data['privacy'], recorded_at=data['recorded_at'], likes_count=data['likes_count'], replies_count=data['replies_count'], retouts_count=data['retouts_count'], user=user) 
                
                    collection.append(tout)
                else:
                    collection.append(item)

            self.collection = collection

    def different_page(self, difference=0):
        url = '%s?per_page=%d&page=%d' % (self._base_url, self._pagination['per_page'], (self._pagination['current_page'] + difference))
        self.set_collection(url)        

        self._pagination['current_page'] += difference

    def next_page(self):
        if (self._pagination['current_page'] < self._pagination['total_pages']):
            self.different_page(difference=1)
        else:
            print "Reached the end of the collection"

    def prev_page(self):
        if (self._pagination['current_page'] > 1):
            self.different_page(difference=-1)
        else:
            print "Reached the beginning of the collection"
        

    def exact_page(self, page=1):
        url = '%s?per_page=%d&page=%d' % (self._base_url, self._pagination['per_page'], page)

        self.set_collection(url)

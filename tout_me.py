from tout_user import ToutUser
from tout_collection import ToutCollection

class ToutMe(ToutUser):
    def change_attribute(self, attribute_key, new_value):
        if self.__dict__.has_key(attribute_key):
            if attribute_key not in self.immutable_fields: 
                self.__setattr__(attribute_key, new_value)
            else:
                return "%s is not a mutable attribute" % attribute_key
        else:
            return "%s does not have attribute %s" % (self, attribute_key)

    def get_updates(self):
        url = self.construct_url('api/v1/users/%s/updates' % self.uid)

        self.updates = ToutCollection(base_url=url, access_token=self._access_token, coll_type='touts')

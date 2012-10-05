from tout_user import ToutUser

class ToutMe(ToutUser):
    def __str__(self):
        return "@%s" % self.uid

    def change_attribute(self, attribute_key, new_value):
        if self.__dict__.has_key(attribute_key):
            if attribute_key not in self.immutable_fields: 
                self.__setattr__(attribute_key, new_value)
            else:
                return "%s is not a mutable attribute" % attribute_key
        else:
            return "%s does not have attribute %s" % (self, attribute_key)     

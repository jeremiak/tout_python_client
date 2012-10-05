class ToutUser(object):
    def __init__(self, uid=None, username=None, fullname=None, friendly_name=None, bio=None, location=None, verified=False, touts_count=0, followers_count=0, friends_count=0, following=False, followed_by=False):
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
        
        self.immutable_fields = ['verified', 'touts_count', 'followers_count', 'friends_count', 'following', 'followed_by']

    def to_json(self):
        import simplejson as json
        
        user = {'user': self.__dict__} 
        return json.dumps(user)

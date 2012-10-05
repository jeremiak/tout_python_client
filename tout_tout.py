from dateutil.parser import parse

class Tout(object):
    def __init__(self, uid=None, text=None, privacy=None, recorded_at=None, created_at=None, likes_count=0, replies_count=0, retouts_count=0, liked=False, image=None, video=None, retouted_tout=None, replied_to_tout=None, user=None, conversation=None):
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

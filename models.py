class Post:
    def __init__(self, post_id, text, likes_count, reposts_count,
                 views_count):
        self.post_id = post_id
        self.text = text
        self.likes_count = likes_count
        self.reposts_count = reposts_count
        self.views_count = views_count
        self.comments = []


class Comment:
    def __init__(self, text, likes_count):
        self.text = text
        self.likes_count = likes_count
